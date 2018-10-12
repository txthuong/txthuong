# Test Name                                     Description
# A_BX_BLE_SRBLEADDCHAR_0001                    Check syntax for AT+SRBLEADDCHAR command
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
# A_BX_BLE_SRBLEADDCHAR_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDCHAR_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRBLEADDCHAR command" % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: On DUT: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Check +SRBLEADDCHAR test command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check +SRBLEADDCHAR execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check +SRBLEADDCHAR read command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check +SRBLEADDCHAR write command valid parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHAR: 52\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Check +SRBLEADDCHAR write command valid parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11, 10, 2, "\\02\\01", 1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHAR: 54\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Check +SRBLEADDCHAR write command with out range and not existing : <service handle> = [-50, 0, 150, 250, 999]\n"
    for i in ('-50','0','150','250','999'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=%s, "2A37", 10, 11\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8: Check +SRBLEADDCHAR write command with out range and not existing : <service handle> = 'A','*','/','\n"
    for i in ('A','*','/','@','#'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=%s, "2A37", 10, 11\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 9: Check +SRBLEADDCHAR write command with out range and not existing : <characteristic uuid> = [G, FFFFF, ' ', " ", /, *]\n"
    for i in ('K', '/', '*','#','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "%s", 10, 11\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 10: Check +SRBLEADDCHAR write command with out range and not existing : <properties> = [-1, 0, 256, 1024]\n"
    for i in ('0','256','1024'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", %s, 11\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 11: Check +SRBLEADDCHAR write command with out range and not existing : <properties> = [A, 1F, *, /, '', ""]\n"
    for i in ('A','*','/','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", %s, 11\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 12: Check +SRBLEADDCHAR write command with out range parameter: <permissions> = [-1, 0, 512, 1024]\n"
    for i in ('0', '512', '1024'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, %s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 13: Check +SRBLEADDCHAR write command with out range and not existing : <permissions> = [A, 1F, *, /,]\n"
    for i in ('A','*','/','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, %s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 14: Check +SRBLEADDCHAR write command with out range and not existing :  <maximum attribute length>  = [A, 1F, *, /, '', ""]\n"
    for i in ('A','*','/','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11,%s, 2, "\\02\\01", 1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 15: Check +SRBLEADDCHAR write command with out range and not existing :  <attribute length>  = [A, 1F, *, /, '', ""]\n"
    for i in ('A','*','/','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11,10, %s, "\\02\\01", 1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 16: Check +SRBLEADDCHAR write command with out range and not existing : <attribute value> = ,""\n"
    for i in ('',','):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11,10, 2, "%s", 1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 17: Check +SRBLEADDCHAR write command with out range and not existing : <attribute control policy>  = [-1, 2, A, *, /, ' ', " "]\n"
    for i in ('-1','2','A','*','/','@'):
        SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11,10, 2, "\\02\\01", %s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 18: Check +SRBLEADDCHAR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 19: Check +SRBLEADDCHAR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50,\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 20: Check +SRBLEADDCHAR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 21: Check +SRBLEADDCHAR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37",10\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 22: Check +SRBLEADDCHAR write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11, 10, 2, "\\02\\01", 1, 1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 23: Delete service\n"
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