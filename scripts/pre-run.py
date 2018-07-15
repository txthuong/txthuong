print '\nThis is pre-run script to check COM ports!!!\n'

uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")
aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

# Check DUT COM port
for count in range(10):
    SagSendAT(uart_com, "AT\r")
    resp = SagWaitResp(uart_com, [''], 5000)
    if 'OK' not in resp:
        SagSendAT(uart_com, "+++")
        SagSendAT(uart_com, "AT\r")
        resp = SagWaitResp(uart_com, [''], 5000)
        if 'OK' in resp:
            break
        else:
            time.sleep(300)
            SagSendAT(uart_com, "AT&F\r")
            resp = SagWaitResp(uart_com, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' %os.environ['UART_COM']
                print '**********************************************************************\n'
                break
    elif 'OK' in resp:
        print '\n**********************************************************************'
        print 'Check %s is done!!!' %os.environ['UART_COM']
        print '**********************************************************************\n'
        break
        
# Check AUX1 COM port
for count in range(10):
    SagSendAT(aux1_com, "AT\r")
    resp = SagWaitResp(aux1_com, [''], 5000)
    if 'OK' not in resp:
        SagSendAT(aux1_com, "+++")
        SagSendAT(aux1_com, "AT\r")
        resp = SagWaitResp(aux1_com, [''], 5000)
        if 'OK' in resp:
            break
        else:
            time.sleep(300)
            SagSendAT(aux1_com, "AT&F\r")
            resp = SagWaitResp(aux1_com, [''], 5000)
            if 'READY' in resp:
                print '\n**********************************************************************'
                print 'Check %s is done!!!' %os.environ['UART_COM']
                print '**********************************************************************\n'
                break
    elif 'OK' in resp:
        print '\n**********************************************************************'
        print 'Check %s is done!!!' %os.environ['AUX1_COM']
        print '**********************************************************************\n'
        break