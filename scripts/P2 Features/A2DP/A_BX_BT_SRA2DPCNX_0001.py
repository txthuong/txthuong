# Test Name                                     Description
# A_BX_BT_SRA2DPCNX_0001                        Check syntax of +SRA2DPCNX command with valid values, invalid values and values out of range
# 
# Requirement
# 1 modules + 1 remote device
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
# A_BX_BT_SRA2DPCNX_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRA2DPCNX_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:  Check syntax of +SRA2DPCNX command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    smartphone_bt_addr = 'ec:f3:42:09:96:78'
    
    print "\nStep 1: Configure I2S with the default values\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configure BTC to be discoverable and connectable\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Enable BTC A2DP profile and use the codec of the dev kit\n"
    SagSendAT(uart_com, 'AT+SRA2DPSTATE=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Configure an A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=%s\r'%smartphone_bt_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",A2DP\r\n' %smartphone_bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query A2DP configure\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",A2DP\r\n' %smartphone_bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Check syntax of +SRA2DPCNX test command\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Check syntax of +SRA2DPCNX read command\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8: Check syntax of +SRA2DPCNX execute command\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 9: Check write command +SRA2DPCNX with not configred and out-range session session_id = 0, 2, 65\n"
    for i in ('0','2','65'):
        SagSendAT(uart_com, 'AT+SRA2DPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 10: Check write command +SRA2DPCNX with invalid parameter session_id = a, *, %, "", '', \\n"
    for i in ('-1','a','*','%','#'):
        SagSendAT(uart_com, 'AT+SRA2DPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 11: Check write command +SRA2DPCNX with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Check write command +SRA2DPCNX with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 13: Check write command +SRA2DPCNX with valid parameter\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOCFG: 0,44100\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",A2DP\r\n' %smartphone_bt_addr], 5000)

    print "\nStep 14: Close A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",A2DP\r\n' %smartphone_bt_addr], 2000)

    print "\nStep 15: Delete A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPDEL=1\r')
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

# Restore BT state to default
SagSendAT(uart_com, "AT+KI2SCFG=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, "AT+SRA2DPSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)