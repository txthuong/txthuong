# Test Name                                     Description
# A_BX_BT_SRA2DPMEDIACTRL_0001                  Check syntax for AT+SRA2DPMEDIACTRL command
# 
# Requirement
# 1 BX modules + 1 Mobile phone
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
# A_BX_BT_SRA2DPMEDIACTRL_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRA2DPMEDIACTRL_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRA2DPMEDIACTRL command" % test_ID
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
    
    print "\nStep 5: Active A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOCFG: 0,44100\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",A2DP\r\n' %smartphone_bt_addr], 5000)
    
    print "\nStep 6: Check test command\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Check syntax of +SRA2DPMEDIACTRL read command\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8: Check syntax of +SRA2DPMEDIACTRL execute command\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 9: Check +SRA2DPMEDIACTRL write command with valid parameters: session_id = 1 and control = 0, 1, 2\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOSTATE: 2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOSTATE: 0\r\n'], 2000)
    
    for i in ('1','2'):
        SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 10: Check +SRA2DPMEDIACTRL write command with not-configured and out-range session\n"
    for i in ('0','2','65','999'):
        SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=%s,0\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 11: Check +SRA2DPMEDIACTRL write command with invalid session_id\n"
    for i in ('-1','a','&','*','#'):
        SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=%s,0\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 12: Check +SRA2DPMEDIACTRL write command with invalid control\n"
    for i in ('-1','a','&','*','#'):
        SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=%s,0\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 13: Check +SRA2DPMEDIACTRL write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=1,0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 14: Check +SRA2DPMEDIACTRL write command with missing parameter control\n"
    SagSendAT(uart_com, 'AT+SRA2DPMEDIACTRL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 15: Close A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",A2DP\r\n' %smartphone_bt_addr], 2000)

    print "\nStep 16: Delete A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 17: Query A2DP configure\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
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