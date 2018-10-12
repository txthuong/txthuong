# Test Name                                     Description
# A_BX_BLE_SRBLEADDCHARDESCRDESCR_0001               Check syntax for AT+SRBLEADDCHARDESCRDESCR command
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initialization ----------------------------------
import string
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
    
    #Get bluetooth address
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    dut_bluetooth_addr = res.split ('"')[1]
    print dut_bluetooth_addr
    
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
# A_BX_BLE_SRBLEADDCHARDESCRDESCR_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDCHARDESCRDESCR_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRBLEADDCHARDESCRDESCR command" % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Check +SRBLEADDCHARDESCR test command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check +SRBLEADDCHARDESCR execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check +SRBLEADDCHARDESCR read command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Add a characteristic into the service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHAR: 52\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: Check +SRBLEADDCHARDESCR write command valid parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", 17\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHARDESCR: 53\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Check +SRBLEADDCHARDESCR write command with <service handle> out range and not existing = [-50, 0, 150, 250, 999]\n"
    for i in ('-50','0','150','250','999'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=%s, "2902", 17\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Check +SRBLEADDCHARDESCR write command with invalid parameter: <service handle> = [A, 1F, *, /, ?]\n"
    for i in ('A','*','/','@','#'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=%s, "2902", 17\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 8: Check +SRBLEADDCHARDESCR write command with invalid parameter: <characteristic descriptor uuid> = [A, 1F, *, /, ?]\n"
    for i in ('A','*','/','@','#'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "%s", 17\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 9: Check +SRBLEADDCHARDESCR write command with out range parameter: <permissions> = [-1, 0, 512, 1024]\n"
    for i in ('-1','0','512','1024'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", %s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 10: Check +SRBLEADDCHARDESCR write command with invalid parameter: <permissions> = [A, 1F, *, /, '', ""]\n"
    for i in ('A','*','/','@','#'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", %s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 11: Check +SRBLEADDCHARDESCR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Check +SRBLEADDCHARDESCR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50,\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Check +SRBLEADDCHARDESCR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 14: Check +SRBLEADDCHARDESCR write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2A37", 17,10, 2, "\\02\\01", 1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 15: Delete service\n"
    SagSendAT(uart_com, 'AT+SRBLEDELSERV=50\r')
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)