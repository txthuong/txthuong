# Test Name                                Description
# A_BX_EmbeddedSW_SRBCSMARTSTART_0004      Check +SRBCSMARTSTART with remote server does not support BC Smart Data
#
# Requirement
#   2 Euler module
#
# Author: txthuong
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(uart_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    dut_bluetooth_address = resp.split('"')[1]

    print "\nGet BLE configure"
    SagSendAT(uart_com, "AT+SRBLE?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    dut_bt_name = resp.split('"')[1]
    dut_max_mtu = resp.split(',')[1]

    # AUX1 Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, "AT+FMM\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, "ATI3\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(aux1_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    aux1_bluetooth_address = resp.split('"')[1]

    print "\nGet BLE configure"
    SagSendAT(aux1_com, "AT+SRBLE?\r")
    resp = SagWaitResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    aux1_bt_name = resp.split('"')[1]
    aux1_max_mtu = resp.split(',')[1]

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRBCSMARTSTART_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRBCSMARTSTART_0004"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check +SRBCSMARTSTART with remote server does not support BC Smart Data" % test_ID
    print "***********************************************************************************************************************"

    print '\nOn AUX1...'
    print 'Step 1: Disable BC Smart profile support'
    SagSendAT(aux1_com, 'AT+SRBLE="%s",%s,0,0\r' % (aux1_bt_name, aux1_max_mtu))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 2: Reset to apply BLE configure'
    SagSendAT(aux1_com, 'AT+RST\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Query BLE configure'
    SagSendAT(aux1_com, "AT+SRBLE?\r")
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE: "%s",%s,0,0\r\n' % (aux1_bt_name, aux1_max_mtu)], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)

    print '\nStep 4: Start BLE advertising'
    SagSendAT(aux1_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 5: Configure an BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",%s\r\n' % (aux1_bluetooth_address, dut_max_mtu)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    mtu = min (aux1_max_mtu, dut_max_mtu)

    print '\nStep 6: Active BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,%s\r\n+SRBCSMART: 1,0,0\r\n' % mtu,'+SRBCSMART: 1,0,0\r\n+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",%s\r\n' % (dut_bluetooth_address, mtu)], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)

    data = 'Test GATT Role .....'
    print '\nStep 7: Send data to AUX1 with GATT server role'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,0\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nCONNECT\r\n'], 2000):
        print '----> Problem: Module did not go to data mode properly!!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)
    else:
        SagSendAT(uart_com, '%s' % data)
        SagSendAT(uart_com, '+++')
        resp = SagWaitResp(aux1_com, [''], 5000)
        if '+SRBCSMARTRECV: 1,1' in resp:
            print '----> Problem: AUX1 still receive data from DUT without BC Smart Profile support !!!'
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
            print '----> Problem: Module did not escape data mode properly !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 8: Send data to AUX1 with GATT client role'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nCONNECT\r\n'], 2000):
        print '----> Problem: Module did not go to data mode properly!!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)
    else:
        SagSendAT(uart_com, '%s' % data)
        SagSendAT(uart_com, '+++')
        resp = SagWaitResp(aux1_com, [''], 5000)
        if '+SRBCSMARTRECV: 1,0' in resp:
            print '----> Problem: AUX1 still receive data from DUT without BC Smart Profile support !!!'
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 10000):
            print '----> Problem: Module did not escape data mode properly !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 9: Close BLE connection'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECLOSE=1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0,19\r\n'], 2000)

    print '\nStep 10: Delete BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 11: Query BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

print '\nSetting BLE configure to default'
SagSendAT(uart_com, 'AT+SRBLE="%s",23,1,0\r' % dut_bt_name)
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(uart_com, 'AT+RST\r')
SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

print '\nSetting AUX1 configure to default'
SagSendAT(aux1_com, 'AT+SRBLE="%s",23,1,0\r' % aux1_bt_name)
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, 'AT+RST\r')
SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)