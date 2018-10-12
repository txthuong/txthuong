# Test Name                                     Description
# A_BX_EmbeddedSW_SPP_0019                      Verify behavior of module when it is in SPP connection timeout
# 
# Requirement
# 2 Euler modules
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
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
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
# A_BX_EmbeddedSW_SPP_0019
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SPP_0019"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Verify behavior of module when it is in SPP connection timeout" % test_ID
    print "*****************************************************************************************************************"
    
    invalid_bluetooth_addr = '20:fa:bb:20:0a:ec'
    
    print "\nStep 1: DUT: Configure SPP connection with invalid Bluetooth address\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %invalid_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %invalid_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: DUT: Change Bluetooth state\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: DUT: Try to activate SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPP_ERROR: 1\r\n'], 8000)

    print "\nStep 4: AUX: Query Bluetooth address\n"
    SagSendAT(aux1_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTADDR: "%s"\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: AUX: Change Bluetooth state\n"
    SagSendAT(aux1_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: DUT: Configure SPP connection to AUX\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",SPP,0\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: DUT: Activate connection to AUX with valid value\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %aux1_bluetooth_address], 5000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 2,1,*\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %dut_bluetooth_address], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %dut_bluetooth_address], 5000)
    SagWaitnMatchResp(aux1_com, ['+SRSPPCNX: 1,1,*\r\n'], 5000)
    
    print "\nStep 8: DUT: Close SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 2,0\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 5000)
    
    print "\nStep 9: Delete SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    SagSendAT(aux1_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 5000)
    
    print "\nStep 10: Query SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nTest Steps completed\n"
  
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
# Clear paired list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore BT state to default
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nAUX: Disable subsystem\n"
SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)