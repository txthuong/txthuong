# Test Name                                     Description
# A_BX_BLE_SRBLEADDINCSERV_0002                 Check if can implement a service to a non-primary service
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
# A_BX_BLE_SRBLEADDINCSERV_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDINCSERV_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check if can implement a service to a non-primary service" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Add a non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1001,0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1002,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 150\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Add a non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1003,0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 250\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Implement the service to the non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,150\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Implement the service to the non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,250\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1004,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 350\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Implement the service to the non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,150\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Implement the service to the non-primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,250\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Delete a primary service\n"
    for i in ('50','150','250','350'):
        SagSendAT(uart_com, 'AT+SRBLEDELSERV=%s\r' %i)
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