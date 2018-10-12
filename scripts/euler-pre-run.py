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
            print 'Open Control COM ...'
            UART_CTRL = SagOpen(control_com, 115200, 8, "N", 1, "None")
            SagSleep(2000)
            print 'Change PIN %s to OUTPUT ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIOCFG=%s,0,1\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Change PIN %s level to LOW ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIO=%s,0\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Change PIN %s level to HIGH ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIO=%s,1\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Close Control COM ...'
            SagClose(UART_CTRL)
            SagSleep(15000)
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
            print 'Open Control COM ...'
            UART_CTRL = SagOpen(control_com, 115200, 8, "N", 1, "None")
            SagSleep(2000)
            print 'Change PIN %s to OUTPUT ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIOCFG=%s,0,1\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Change PIN %s level to LOW ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIO=%s,0\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Change PIN %s level to HIGH ...' % control_pin
            SagSendAT(UART_CTRL, "AT+KGPIO=%s,1\r" % control_pin)
            SagWaitnMatchResp(UART_CTRL, ['\r\nOK\r\n'], 2000)
            SagSleep(2000)
            print 'Close Control COM ...'
            SagClose(UART_CTRL)
            SagSleep(15000)
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