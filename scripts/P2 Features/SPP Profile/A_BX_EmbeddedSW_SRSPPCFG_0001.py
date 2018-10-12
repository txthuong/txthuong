# Test Name                                     Description
# A_BX_EmbeddedSW_SRSPPCFG_0001                 Check if can configure 2 SPP session with same bluetooth address
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
# A_BX_EmbeddedSW_SRSPPCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRSPPCFG_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check if can configure 2 SPP session with same bluetooth address" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configure a SPP session\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=20:fa:bb:20:08:da\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"20:fa:bb:20:08:da",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"20:fa:bb:20:08:da",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 4: Configure an addition SPP session with same BT address in step 3\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=20:fa:bb:20:08:da\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 933\r\n'], 2000)
    
    print "\nStep 5: Delete the SPP session\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 6: Re-configure SPP session with same BT address in step 2\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=20:fa:bb:20:08:da\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"20:fa:bb:20:08:da",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Configure an addition SPP session with other BT address\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=20:fa:bb:20:08:db\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"20:fa:bb:20:08:db",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Configure an addition SPP session with same BT address in step 7\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=20:fa:bb:20:08:db\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 933\r\n'], 2000)
    
    print "\nStep 9: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"20:fa:bb:20:08:da",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 2,0,"20:fa:bb:20:08:db",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Delete the SPP session\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    SagSendAT(uart_com, 'AT+SRSPPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
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

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART,AUX1
SagClose(uart_com)