# Test Name                                     Description
# A_BX_BLE_SRBLEADDSERV_0001                    Check syntax for AT+SRBLEADDSERV command
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
# A_BX_BLE_SRBLEADDSERV_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDSERV_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRBLEADDSERV command" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 3: Check +SRBLEADDSERV test command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check +SRBLEADDSERV execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check +SRBLEADDSERV read command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Check +SRBLEADDSERV write command with valid parameters\n"
    for service_uuid in ('1234','abcd','1234ffff'):
        SagSendAT(uart_com, 'AT+SRBLEADDSERV=%s\r' %service_uuid)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: *\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Check +SRBLEADDSERV write command with valid parameters\n"
    for primary in ('0','1'):
        SagSendAT(uart_com, 'AT+SRBLEADDSERV=180D,%s\r' %primary)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: *\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Check +SRBLEADDSERV write command with invalid parameters: <service uuid> = ["", ', /, G, 180FF, 0123456789]\n"
    for service_uuid in ('"','@','%','#','123456789','180fffff'):
        SagSendAT(uart_com, 'AT+SRBLEADDSERV=%s\r' %service_uuid)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 9: Check +SRBLEADDSERV write command with invalid parameters: <is_primary> = [-1, 2, a, *, /]\n"
    for primary in ('-1','2','a','*','/'):
        SagSendAT(uart_com, 'AT+SRBLEADDSERV=180D,%s\r' %primary)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 10: Check +SRBLEADDSERV write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 11: Check +SRBLEADDSERV write command with extra parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=180D,0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 12: Delete service\n"
    for ser in ('50','150','250','350'):
        SagSendAT(uart_com, 'AT+SRBLEDELSERV=%s\r' %ser)
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