#include <SoftwareSerial.h>
#include <Adafruit_VC0706.h>
#include <Adafruit_CC3000.h>
#include <ccspi.h>
#include <SPI.h>
#include <string.h>
#include "utility/debug.h"
#include<stdlib.h>

// Software serial
SoftwareSerial cameraconnection = SoftwareSerial(2, 4);
Adafruit_VC0706 cam = Adafruit_VC0706(&cameraconnection);
// Define CC3000 chip pins
#define ADAFRUIT_CC3000_IRQ   3
#define ADAFRUIT_CC3000_VBAT  5
#define ADAFRUIT_CC3000_CS    10

// WiFi network (change with your settings !)
#define WLAN_SSID       "your-ssid"        // cannot be longer than 32 characters!
#define WLAN_PASS       "your-password"
#define WLAN_SECURITY   WLAN_SEC_WPA2 // This can be WLAN_SEC_UNSEC, WLAN_SEC_WEP, WLAN_SEC_WPA or WLAN_SEC_WPA2

// Create CC3000 instances
Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
SPI_CLOCK_DIV2);

// Local server IP, port, and repository (change with your settings !)
uint32_t ip = cc3000.IP2U32(192,168,1,98);
int port = 5859;

int count = 0;

void setup() {

  Serial.begin(9600);
  
  // Try to locate the camera
  if (cam.begin()) {
    Serial.println("VC0706 Camera has been initalized successfully!");
  } 
  else {
    Serial.println("Camera not connected properly!");
    return;
  }

  // Set picture size
  cam.setImageSize(VC0706_640x480);

  // Initialise the module
  Serial.println(F("\nConfiguring Wifi module..."));
  if (!cc3000.begin())
  {
    Serial.println(F("Couldn't begin()! Check your wiring?"));
    while(1);
  }

  // Connect to  Wifi network
  Serial.println(F("\nEstablishing a connection with access point"));
  cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY);

  // Display connection details
  Serial.println(F("DHCP request..."));
  while (!cc3000.checkDHCP())
  {
    delay(100); // ToDo: Insert a DHCP timeout!
  }

  Serial.println("\n");
  cc3000.printIPdotsRev(ip);
  Serial.println("\n");
  
  //  Motion detection system can alert you when the camera 'sees' motion!
  cam.setMotionDetect(true);           // turn it on
  //cam.setMotionDetect(false);        // turn it off   (default)

  Serial.print("Motion detection is ");
  if (cam.getMotionDetect()) 
    Serial.println("ON");
  else 
    Serial.println("OFF");
}

void loop() {
  if (cam.motionDetected()) {
   Serial.println("Motion!");   
   cam.setMotionDetect(false);
  
//    if (!cam.takePicture()) 
//      Serial.println("No picture taken!");
//    else 
//      Serial.println("Picture taken!");
    cam.takePicture();
    
    // Get the size of the image (frame) taken  
    uint16_t jpglen = cam.frameLength();
    //Serial.print("Storing ");
    //Serial.print(jpglen, DEC);
    //Serial.print(" byte image.");
  
    // Prepare request
    String start_request = "";
    String end_request = "";
    start_request = start_request + "\r\n--arduinoToRaspberryPi\r\nContent-Disposition: form-data; name=\"image\"; filename=\"snapshot" + count + ".jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";  
    end_request = end_request + "--arduinoToRaspberryPi--\r\n";
  
    uint16_t extra_length;
    extra_length = start_request.length() + end_request.length();
    Serial.println("Extra length:");
    Serial.println(extra_length);
  
    uint16_t len = jpglen + extra_length;
  
    Serial.println(F("PART headers:"));
    Serial.print(start_request);
    Serial.print("binary data");
    Serial.print(end_request);
  
    String connectionMsg = "Starting connection to server ...";
    
    //Serial.println(connectionMsg);
    Adafruit_CC3000_Client client = cc3000.connectTCP(ip, port);
  
    // Connect to the server, please change your IP address !
    if (client.connected()) {
      //Serial.println(F("Connected !"));
      client.println(F("POST /upload HTTP/1.1"));
      client.println(F("Host: 192.168.1.98:5859"));
      client.println(F("Content-Type: multipart/form-data; boundary=arduinoToRaspberryPi"));
      client.print(F("Content-Length: "));
      client.println(len);
      client.print(start_request);
  
      // Read all the data up to # bytes!
      byte wCount = 0; // For counting # of writes
      while (jpglen > 0) {
        uint8_t *buffer;
        uint8_t bytesToRead = min(32, jpglen); // change 32 to 64 for a speedup but may not work with all setups!
  
        buffer = cam.readPicture(bytesToRead);
        client.write(buffer, bytesToRead);
  
        if(++wCount >= 64) { // Every 2K, give a little feedback so it doesn't appear locked up
          Serial.print('.');
          wCount = 0;
        }
        jpglen -= bytesToRead;
        delay(10); 
      }
  
      client.print(end_request);
      client.println();
  
      Serial.println("Image sent successfully!");
    } 
  
    else {
      Serial.println(F("Connection failed"));    
    }
    
    cam.resumeVideo();
    cam.setMotionDetect(true);
    count++;
  }
}