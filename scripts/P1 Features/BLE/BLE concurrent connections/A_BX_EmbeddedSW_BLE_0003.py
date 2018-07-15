# Test Name                       Description
# A_BX_EmbeddedSW_BLE_0003        Verify module can connect/receive to/form 3 BLE devices at the same time
#
# Requirement
#   4 Euler module
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

    # AUX2 Initialization
    print "\nOpen AT Command port"
    aux2_com = SagOpen(aux2_com, 115200, 8, "N", 1, "None")

    # Display AUX2 information
    print "\nDisplay AUX2 information"
    print "\nGet model information"
    SagSendAT(aux2_com, "AT+FMM\r")
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux2_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux2_com, "ATI3\r")
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(aux2_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(aux2_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    aux2_bluetooth_address = resp.split('"')[1]

    # AUX3 Initialization
    print "\nOpen AT Command port"
    aux3_com = SagOpen(aux3_com, 115200, 8, "N", 1, "None")

    # Display AUX3 information
    print "\nDisplay AUX3 information"
    print "\nGet model information"
    SagSendAT(aux3_com, "AT+FMM\r")
    SagWaitnMatchResp(aux3_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux3_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux3_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux3_com, "ATI3\r")
    SagWaitnMatchResp(aux3_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(aux3_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(aux3_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    aux3_bluetooth_address = resp.split('"')[1]

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_BLE_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_BLE_0003"
VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Verify module can connect/receive to/form 3 BLE devices at the same time" % test_ID
    print "***********************************************************************************************************************"

    print '\nOn AUX1...'
    print 'Step 1: Start BLE advertising'
    SagSendAT(aux1_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn AUX2...'
    print 'Step 2: Start BLE advertising'
    SagSendAT(aux2_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print '\nOn AUX3...'
    print 'Step 3: Configure a BLE connection to DUT'
    SagSendAT(aux3_com, 'AT+SRBLECFG=%s\r' % dut_bluetooth_address)
    SagWaitnMatchResp(aux3_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux3_com, ['OK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 4: Configure an BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' % aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print 'Step 5: Configure an BLE connection to AUX2'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux2_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 2,0,"%s",23\r\n' % aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print '\nStep 6: Active BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n\r\n+SRBCSMART: 1,1,1\r\n','\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n\r\n+SRBCSMART: 1,1,1\r\n','\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,23\r\n'], 2000)

    print '\nStep 7: Active BLE connection to AUX2'
    SagSendAT(uart_com, 'AT+SRBLECNX=2\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 2,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX2 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 2,23\r\n\r\n+SRBCSMART: 2,1,1\r\n','\r\n+SRBCSMART: 2,1,1\r\n+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 1,23\r\n\r\n+SRBCSMART: 1,1,1\r\n','\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,23\r\n'], 2000)

    print '\nStep 8: Start BLE advertising'
    SagSendAT(uart_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)

    print '\nOn AUX3...'
    print 'Step 9: Active BLE connection to DUT'
    SagSendAT(aux3_com, 'AT+SRBLECNX=1\r')
    if not SagWaitnMatchResp(aux3_com, ['\r\n+SRBLE_IND: 1,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: AUX2 cannot connect to DUT properly !!!")
    SagWaitnMatchResp(aux3_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux3_com, ['+SRBLEMTU: 1,23\r\n\r\n+SRBCSMART: 1,1,1\r\n','\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 3,0,"%s",23\r\n' % aux3_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLE_IND: 3,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 3,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 3,23\r\n\r\n+SRBCSMART: 3,1,1\r\n','\r\n+SRBCSMART: 3,1,1\r\n+SRBLEMTU: 3,23\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 10: Query BLE current connection'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,1,"%s",23' % aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 2,1,"%s",23' % aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 3,1,"%s",23' % aux3_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 11: Close all BLE connection'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECLOSE=1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLECLOSE=2\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLE_IND: 1,0\r\n'], 2000)
    print 'On AUX3...'
    SagSendAT(aux3_com, "AT+SRBLECLOSE=1\r")
    SagWaitnMatchResp(aux3_com, ['\r\n+SRBLE_IND: 1,0\r\n'], 2000)
    SagWaitnMatchResp(aux3_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 3,0\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 12: Query BLE current connection'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",23' % aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 2,0,"%s",23' % aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 3,0,"%s",23' % aux3_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 13: Delete all BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLEDEL=2\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLEDEL=3\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX2...'
    SagSendAT(aux2_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX3...'
    SagSendAT(aux3_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(aux3_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 14: Query BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print 'On AUX2...'
    SagSendAT(aux2_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print 'On AUX3...'
    SagSendAT(aux3_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux3_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux2_com, 'AT&F\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux3_com, 'AT&F\r')
    SagWaitnMatchResp(aux3_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
# Close AUX2
SagClose(aux2_com)
# Close AUX3
SagClose(aux3_com)