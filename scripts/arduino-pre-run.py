from pyduino import *

print '\nThis is pre-run script to check COM ports!!!\n'

# Check DUT COM port
UART = SagOpen(uart_com, 115200, 8, "N", 1, "None")

for count in range(10):
    SagSendAT(UART, "AT\r")
    resp = SagWaitResp(UART, [''], 5000)
    if 'OK' not in resp:
        SagSendAT(UART, "+++")
        SagWaitResp(UART, [''], 2000)
        SagSendAT(UART, "AT\r")
        resp = SagWaitResp(UART, [''], 5000)
        if SagMatchResp(resp, ['\r\nOK\r\n', '\r\nERROR\r\n']):
            SagSendAT(UART, "AT&F\r")
            resp = SagWaitResp(UART, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' % uart_com
                print '**********************************************************************\n'
                break
        else:
            SagClose(UART)
            print 'Open Arduino COM ...'
            board = Arduino(serial_port= control_com)
            SagSleep(2000)
            print 'Change PIN %s to OUTPUT ...' % control_pin
            board.set_pin_mode(control_pin,'O')
            SagSleep(2000)
            print 'Change PIN %s level to LOW ...' % control_pin
            board.digital_write(control_pin,0)
            SagSleep(2000)
            print 'Change PIN %s level to HIGH ...' % control_pin
            board.digital_write(control_pin,1)
            SagSleep(2000)
            print 'Close Arduino COM ...'
            board.close()
            SagSleep(30000)
            UART = SagOpen(uart_com, 115200, 8, "N", 1, "None")
            SagSendAT(UART, "AT&F\r")
            resp = SagWaitResp(UART, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' % uart_com
                print '**********************************************************************\n'
                break
    elif 'OK' in resp:
        print '\n**********************************************************************'
        print 'Check %s is done!!!' % uart_com
        print '**********************************************************************\n'
        break

# Check AUX1 COM port
AUX1 = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

for count in range(10):
    SagSendAT(AUX1, "AT\r")
    resp = SagWaitResp(AUX1, [''], 5000)
    if 'OK' not in resp:
        SagSendAT(AUX1, "+++")
        SagWaitResp(AUX1, [''], 2000)
        SagSendAT(AUX1, "AT\r")
        resp = SagWaitResp(AUX1, [''], 5000)
        if SagMatchResp(resp, ['\r\nOK\r\n', '\r\nERROR\r\n']):
            SagSendAT(AUX1, "AT&F\r")
            resp = SagWaitResp(AUX1, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' % aux1_com
                print '**********************************************************************\n'
                break
        else:
            SagClose(AUX1)
            print 'Open Arduino COM ...'
            board = Arduino(serial_port= control_com)
            SagSleep(2000)
            print 'Change PIN %s to OUTPUT ...' % control_pin
            board.set_pin_mode(control_pin,'O')
            SagSleep(2000)
            print 'Change PIN %s level to LOW ...' % control_pin
            board.digital_write(control_pin,0)
            SagSleep(2000)
            print 'Change PIN %s level to HIGH ...' % control_pin
            board.digital_write(control_pin,1)
            SagSleep(2000)
            print 'Close Arduino COM ...'
            board.close()
            SagSleep(30000)
            AUX1 = SagOpen(aux1_com, 115200, 8, "N", 1, "None")
            SagSendAT(AUX1, "AT&F\r")
            resp = SagWaitResp(AUX1, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' % aux1_com
                print '**********************************************************************\n'
                break
    elif 'OK' in resp:
        print '\n**********************************************************************'
        print 'Check %s is done!!!' % aux1_com
        print '**********************************************************************\n'
        break

# Close UART
SagClose(UART)
SagClose(AUX1)
SagSleep(120000)