# Test Name                                     Description
# A_BX_EmbeddedSW_SPP_0013                      Check the module can establish SPP connection to Huawei android smartphone
# 
# Requirement
# 1 module, Huawei smartphone that is installed MelodyClassic
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initialization ----------------------------------

test_environment_ready = "Ready"

try:

    print "\n------------Test Environment check: Begin------------"
    # UART Initialization
    print "\nOpen AT Command port"
    uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SPP_0013
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SPP_0013"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check the module can establish SPP connection to Huawei android smartphone" % test_ID
    print "*****************************************************************************************************************"
    
    smartphone_bluetooth_address = "ec:f3:42:09:96:78"
    
    print "\nStep 1: DUT: Query Bluetooth address\n"
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTADDR: "%s"\r\n' %dut_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: DUT: Change Bluetooth state\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Use MelodyClassic to connect to module\n"
    wx.MessageBox('Connect to module then click "OK"', 'Info',wx.OK)
    
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %smartphone_bluetooth_address], 5000)
    SagWaitnMatchResp(uart_com, ['+SRSPPCNX: 1,1,*\r\n'], 5000)
    
    print "\nStep 4: Use MelodyClassic to send data to module: hello from smartphone\n"
    wx.MessageBox('Use MelodyClassic to send data then click "OK"', 'Info',wx.OK)
    SagWaitnMatchResp(uart_com, ['+SRSPP_DATA: 1,21,hello from smartphone\r\n'], 2000)
    
    print "\nStep 5: Disconnect SPP connection from MelodyClassic app and Make MelodyClassic app in discoverable mode\n"
    wx.MessageBox('Disconnect SPP connection from MelodyClassic app and Make MelodyClassic app in discoverable mode then click "OK"', 'Info',wx.OK)
    
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    
    print "\nStep 6: DUT: Activate SPP connection to smartphone \n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)

    print "\nStep 7: DUT: Send data to smartphone\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=1, "Hello from Euler"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Check data on the screen of MelodySmart app\n"
    wx.MessageBox('Check data on the screen: Hello from Euler then click "OK"', 'Info',wx.OK)
    
    print "\nStep 9: DUT: Try to close SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: DUT: Try to delete SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART,AUX1
SagClose(uart_com)
