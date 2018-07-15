# Test Name                                Description
# A_BX_EmbeddedSW_SRBCSMARTCMD_0002        Verify command +SRBCSMARTCMD has <session_id>  support range 1-64
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
    dut_max_mtu = int(resp.split(',')[1])

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
    aux1_max_mtu = int(resp.split(',')[1])

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRBCSMARTCMD_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRBCSMARTCMD_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Verify command +SRBCSMARTCMD has <session_id>  support range 1-64" % test_ID
    print "***********************************************************************************************************************"

    print '\nOn DUT...'
    print 'Step 1: Query BLE configure'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    for session in range (1, 65):
        print '\nStep 2: Configure a BLE connections to AUX1'
        SagSendAT(uart_com, 'AT+SRBLECFG="%s"\r' % aux1_bluetooth_address)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: %s,0,"%s",%s' % (session, aux1_bluetooth_address, dut_max_mtu)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1...'
        print 'Step 3: Start BLE advertising'
        SagSendAT(aux1_com, "AT+SRBLEADV=1\r")
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        mtu = min(aux1_max_mtu, dut_max_mtu)

        print '\nOn DUT...'
        print 'Step 4: Active BLE connection to AUX1'
        SagSendAT(uart_com, 'AT+SRBLECNX=%s\r' % session)
        if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: %s,1\r\nOK\r\n' % session], 5000):
            raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
        SagWaitnMatchResp(uart_com, ['+SRBLEMTU: %s,%s\r\n' % (session, mtu)], 2000)
        SagWaitnMatchResp(uart_com, ['+SRBLEMTU: %s,%s\r\n\r\n+SRBCSMART: %s,1,1\r\n' % (session, mtu, session),'\r\n+SRBCSMART: %s,1,1\r\n+SRBLEMTU: %s,%s\r\n' % (session, session, mtu)], 2000)
        SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",%s\r\n' % (dut_bluetooth_address, mtu)], 2000)
        SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
        SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
        SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n\r\n+SRBCSMART: 1,1,1\r\n' % mtu,'\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,%s\r\n' % mtu], 2000)

        print '\nOn AUX1...'
        print 'Step 5: Enable remote control'
        SagSendAT(aux1_com, 'AT+SRREMCTRL=1\r')
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        command = 'AT+FMM'
        expect_response = ['\r\nBX310x\r\n\r\nOK\r\n']

        print '\nOn DUT...'
        print 'Step 6: Execute AT command on remote BC Smart server'
        SagSendRemoteAT(uart_com, session, command, mtu)
        SagWaitnMatchResp(aux1_com, ['+SRREMCMD: "%s"\r' % command.replace('"', '\\22')], 2000)
        SagWaitnMatchResp(aux1_com, expect_response, 2000)
        SagWaitnMatchRemoteResp(uart_com, session, expect_response, 5000)

        print '\nOn AUX1...'
        print 'Step 7: Disable remote control'
        SagSendAT(aux1_com, 'AT+SRREMCTRL=0\r')
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nStep 8: Close BLE connection'
        SagSendAT(uart_com, "AT+SRBLECLOSE=%s\r" % session)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: %s,0\r\n' % session], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
        SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0\r\n'], 2000)

        print '\nStep 9: Delete BLE configuration'
        print 'On DUT...'
        SagSendAT(uart_com, "AT+SRBLEDEL=%s\r" % session)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        print 'On AUX1...'
        SagSendAT(aux1_com, "AT+SRBLEDEL=1\r")
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nStep 10: Configure a BLE configuration with dummy BT Mac Address'
        if session < 10:
            bt_mac_address = 'aa:bb:cc:33:22:0%s' % session
        else:
            bt_mac_address = 'aa:bb:cc:33:22:%s' % session
        SagSendAT(uart_com, 'AT+SRBLECFG="%s"\r' % bt_mac_address)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: %s,0,"%s",23' % (session, bt_mac_address)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 11: Query BLE configure'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    for session in range (1, 65):
        if session < 10:
            bt_mac_address = 'aa:bb:cc:33:22:0%s' % session
        else:
            bt_mac_address = 'aa:bb:cc:33:22:%s' % session
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: %s,0,"%s",23' % (session, bt_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 12: Configure one more BLE connections'
    SagSendAT(uart_com, 'AT+SRBLECFG="aa:bb:cc:33:22:65"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 912\r\n'], 2000)

    print '\nStep 13: Delete 64th session'
    for session in range (1, 65):
        SagSendAT(uart_com, "AT+SRBLEDEL=%s\r" % session)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 14: Query BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg:
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

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
