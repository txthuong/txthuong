# Test Name                                     Description
# A_BX_EmbeddedSW_SPP_0006                      Check Syntax of write +SRSPPCFG command with valid values, invalid values and values out of range
# 
# Requirement
# 3 Euler modules
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
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux2_com = SagOpen(aux2_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux2_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux2_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux2_com, 'ATI3\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux2_com, 'AT\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX2: Enable subsystem\n"
    SagSendAT(aux2_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SPP_0006
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SPP_0006"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check Syntax of write +SRSPPCFG command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: DUT: Configure Bluetooth connection with invalid value (the Bluetooth address below is sample one\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=aabbccddeeff\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 2: DUT: Configure Bluetooth connection with invalid value (the Bluetooth address below is sample one)\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG="aa-bb-cc-dd-ee-ff"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 3: DUT: Configure Bluetooth connection with invalid value - lacking one character (the Bluetooth address below is sample one)\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG="aa:bb:cc:dd:ee:f"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 4: AUX1: Change Bluetooth state\n"
    SagSendAT(aux1_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: DUT: Configure Bluetooth connection with valid value (the Bluetooth address below is sample one)\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: DUT: Activate connection to AUX with valid value\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %aux1_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 4000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 3000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %dut_bluetooth_address], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %dut_bluetooth_address], 4000)
    SagWaitnMatchResp(aux1_com, ['+SRSPPCNX: 1,1,*\r\n'], 4000)
    
    print "\nStep 7: DUT: Query current SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",SPP,*\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: DUT: Configure second Bluetooth connection with valid value\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux2_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",SPP,0\r\n' %aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 9: DUT: Query current SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",SPP,*\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 2,0,"%s",SPP,*\r\n' %aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
   
    print "\nStep 10: DUT, AUX: Close SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
   
    print "\nStep 10: DUT, AUX1, AUX2: Delete SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+SRSPPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nTest Steps completed\n"

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

# Clear paired list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux2_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Restore BT state to default
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux2_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

print "\nAUX: Disable subsystem\n"
SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(aux2_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Close UART,AUX1,AUX2
SagClose(uart_com)
SagClose(aux1_com)
SagClose(aux2_com)

