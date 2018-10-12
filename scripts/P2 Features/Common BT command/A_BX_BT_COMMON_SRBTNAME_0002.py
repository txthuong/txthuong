# Test Name                                     Description
# A_BX_BT_COMMON_SRBTNAME_0002                  Check that BT name is persistent after AT+RST and return to default after factory reset
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT InitializAT+SYSRAMon ----------------------------------

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
# A_BX_BT_COMMON_SRBTNAME_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_COMMON_SRBTNAME_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check syntax and input range for the AT command +SRBTNAME" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    default_name = res.split('"')[1]
    print default_name
    
    name = 'BX310x_DUT'
    print "\nStep 2: Change the BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME=%s\r' %name)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTNAME: "%s"\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Perform AT+RST\n"
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 5000)
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTNAME: "%s"\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Perform AT&F\n"
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 5000)
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    time.sleep(5)
    
    print "\nStep 5: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTNAME: "%s"\r\n' %default_name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
