# Test Name                                     Description
# A_BX_BT_SRA2DPCFG_0003                        When disabling the profile, if A2DP sessions are created but not running, they will be deleted
# 
# Requirement
# 1 Euler module
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
# A_BX_BT_SRA2DPCFG_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRA2DPCFG_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:  When disabling the profile, if A2DP sessions are created but not running, they will be deleted" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Query A2DP configure. No configure exist\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configure I2S with the default values\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Configure BTC to be discoverable and connectable\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Enable BTC A2DP profile and use the codec of the dev kit\n"
    SagSendAT(uart_com, 'AT+SRA2DPSTATE=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Create some A2DP sessions\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=FF:FF:FF:FF:FF:00\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:ff:ff:00",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+SRA2DPCFG=FF:FF:FF:FF:FF:11\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"ff:ff:ff:ff:ff:11",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+SRA2DPCFG=FF:FF:FF:FF:FF:22\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 3,0,"ff:ff:ff:ff:ff:22",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:ff:ff:00",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 2,0,"ff:ff:ff:ff:ff:11",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 3,0,"ff:ff:ff:ff:ff:22",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Disable A2DP profile\n"
    SagSendAT(uart_com, 'AT+SRA2DPSTATE=0,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
   
    print "\nStep 9: Create an addition A2DP sessions\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=FF:FF:FF:FF:FF:FF\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
   
    print "\nStep 10: Query A2DP sessions\n"
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)