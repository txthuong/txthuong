# Test Name                                     Description
# A_BX_EmbeddedSW_SRSPPCFG_0002                 Check that module supports 64 SPP sessions
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
# A_BX_EmbeddedSW_SRSPPCFG_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRSPPCFG_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check that module supports 64 SPP sessions" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configure a SPP session\n"
    for session in range (1, 65):
        if session >= 10:
            bt_hex_addr = 'ff:ff:ff:33:22:%s' % session
        else:
            bt_hex_addr = 'ff:ff:ff:33:22:0%s' % session
            
        SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %bt_hex_addr)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: %s,0,"%s",SPP,0\r\n' %(session, bt_hex_addr)], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:33:22:01",SPP,0'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"ff:ff:ff:33:22:64",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 4: Configure an addition SPP session\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG="ff:ff:ff:33:22:64"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 933\r\n'], 2000)
    
    print "\nStep 5: Delete the 64th SPP session\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=64\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 6: Re-configure SPP session with same BT address in step 4\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG="ff:ff:ff:33:22:64"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 64,0,"ff:ff:ff:33:22:64",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Query SPP configure\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:33:22:01",SPP,0'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"ff:ff:ff:33:22:64",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Delete the SPP session\n"
    for i in range (1,65):
        SagSendAT(uart_com, 'AT+SRSPPDEL=%s\r' %i)
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

# Clear paired list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore BT state to default
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)