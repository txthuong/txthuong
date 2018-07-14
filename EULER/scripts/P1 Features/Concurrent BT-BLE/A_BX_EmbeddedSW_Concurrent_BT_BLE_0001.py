# Test Name                                     Description
# A_BX_EmbeddedSW_Concurrent_BT_BLE_0001        Verify module can concurrently connect to BT classic devices and BLE devices
#
# Requirement
#   3 Euler module
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_Concurrent_BT_BLE_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_Concurrent_BT_BLE_0001"
VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Verify module can concurrently connect to BT classic devices and BLE devices" % test_ID
    print "***********************************************************************************************************************"

    print '\nOn AUX1...'
    print 'Step 1: Change Bluetooth state to connectable mode'
    SagSendAT(aux1_com, "AT+SRBTSTATE=1,2,1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn AUX2...'
    print 'Step 2: Change Bluetooth state to connectable mode'
    SagSendAT(aux2_com, "AT+SRBTSTATE=1,2,1\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 3: Change Bluetooth state to connectable mode'
    SagSendAT(uart_com, "AT+SRBTSTATE=1,2,1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 4: Configure a BT classic connection to AUX1'
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' % aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0' % aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 5: Configure a BT classic connection to AUX2'
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' % aux2_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",SPP,0' % aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 6: Active SPP connection to AUX1'
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' % aux1_bluetooth_address], 5000)
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 10000):
        raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTPAIR: "%s",1\r\n' % dut_bluetooth_address], 5000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 10000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)

    print '\nStep 7: Active SPP connection to AUX2'
    SagSendAT(uart_com, 'AT+SRSPPCNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' % aux2_bluetooth_address], 5000)
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 2,1,*\r\n'], 10000):
        raise Exception("---->Problem: DUT cannot connect to AUX2 properly !!!")
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBTPAIR: "%s",1\r\n' % dut_bluetooth_address], 5000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 10000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)

    message_aux1 = 'Hello AUX1'
    print '\nStep 8: Send data to AUX1'
    SagSendAT(uart_com, 'AT+SRSPPSND=1,"%s"\r' % message_aux1)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRSPP_DATA: 1,%d,%s\r\n' % (len(message_aux1), message_aux1)], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)

    message_aux2 = 'Hello AUX2'
    print '\nStep 9: Send data to AUX2'
    SagSendAT(uart_com, 'AT+SRSPPSND=2,"%s"\r' % message_aux2)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRSPP_DATA: 1,%d,%s\r\n' % (len(message_aux2), message_aux2)], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)

    print '\nOn AUX1...'
    print 'Step 10: Start BLE advertising'
    SagSendAT(aux1_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn AUX2...'
    print 'Step 11: Start BLE advertising'
    SagSendAT(aux2_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 12: Configure an BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 3,0,"%s",23\r\n' % aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print 'Step 13: Configure an BLE connection to AUX2'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux2_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 4,0,"%s",23\r\n' % aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print '\nStep 14: Active BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECNX=3\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 3,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 3,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 3,23\r\n\r\n+SRBCSMART: 3,1,1\r\n','\r\n+SRBCSMART: 3,1,1\r\n+SRBLEMTU: 3,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 2,0,"%s",23\r\n' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 2,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 2,23\r\n\r\n+SRBCSMART: 2,1,1\r\n','\r\n+SRBCSMART: 2,1,1\r\n+SRBLEMTU: 2,23\r\n'], 2000)

    print '\nStep 15: Active BLE connection to AUX2'
    SagSendAT(uart_com, 'AT+SRBLECNX=4\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 4,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX2 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 4,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 4,23\r\n\r\n+SRBCSMART: 4,1,1\r\n','\r\n+SRBCSMART: 4,1,1\r\n+SRBLEMTU: 4,23\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLECFG: 2,0,"%s",23\r\n' % dut_bluetooth_address], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLE_IND: 2,1\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 2,23\r\n\r\n+SRBCSMART: 2,1,1\r\n','\r\n+SRBCSMART: 2,1,1\r\n+SRBLEMTU: 2,23\r\n'], 2000)

    print '\nStep 16: Discover service on AUX1'
    SagSendAT(uart_com, "AT+SRBLEDISCSERV=3\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEDISCSERV: 3,"1801",1,1,5\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print '\nStep 17: Discover service on AUX2'
    SagSendAT(uart_com, "AT+SRBLEDISCSERV=4\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEDISCSERV: 4,"1801",1,1,5\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print '\nStep 18: Close all BT connection'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECLOSE=3\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 2,0\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLECLOSE=4\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 4,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLE_IND: 2,0\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRSPPCLOSE=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    print 'On AUX2...'
    SagSendAT(aux2_com, "AT+SRSPPCLOSE=1\r")
    SagWaitnMatchResp(aux2_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print '\nStep 19: Delete all BT configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRSPPDEL=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRSPPDEL=2\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLEDEL=3\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLEDEL=4\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRSPPDEL=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, "AT+SRBLEDEL=2\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX2...'
    SagSendAT(aux2_com, "AT+SRSPPDEL=1\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux2_com, "AT+SRBLEDEL=2\r")
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 20: Query BT configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRSPPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRSPPCFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    SagSendAT(aux1_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print 'On AUX2...'
    SagSendAT(aux2_com, "AT+SRSPPCFG?\r")
    if not SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    SagSendAT(aux2_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BT configure was not closed and delete properly !!!")
    print "\nTest Steps completed"

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

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Clear pair list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux2_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
# Close AUX2
SagClose(aux2_com)