# Test Name                                     Description
# A_BX_BT_SRA2DPDEL_0003                        To check +SRA2DPDEL command incase the <session_id> is configured and connected
# 
# Requirement
# 1 module
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
# A_BX_BT_SRA2DPDEL_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRA2DPDEL_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check +SRA2DPDEL command incase the <session_id> is configured and connected" % test_ID
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
    
    print "\nStep 4: Configure 64 A2DP session\n"
    for session in range (1, 65):
        if session >= 10:
            bt_hex_addr = 'aa:bb:cc:22:11:%s' % session
        else:
            bt_hex_addr = 'aa:bb:cc:22:11:0%s' % session
            
        SagSendAT(uart_com, 'AT+SRA2DPCFG=%s\r' %bt_hex_addr)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: %s,0,"%s",A2DP\r\n' %(session, bt_hex_addr)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"aa:bb:cc:22:11:01",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"aa:bb:cc:22:11:64",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Delete 64th A2DP configure: <session_id>=[64]\n"
    SagSendAT(uart_com, 'AT+SRA2DPDEL=64\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"aa:bb:cc:22:11:01",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 63,0,"aa:bb:cc:22:11:63",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Re-addition 64th A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=AA:BB:CC:22:11:3F\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 64,0,"aa:bb:cc:22:11:3f",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"aa:bb:cc:22:11:01",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"aa:bb:cc:22:11:3f",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Delete all A2DP configure\n"
    for i in range (1,65):
        SagSendAT(uart_com, 'AT+SRA2DPDEL=%s\r'%i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Checking +SRA2DPCFG\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 12: Re-addition an A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=aa:bb:cc:22:11:3f\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"aa:bb:cc:22:11:3f",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 13: Query A2DP configure\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"aa:bb:cc:22:11:3f",A2DP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 14: Delete the re-addition A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 15: Query A2DP configure\n"
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