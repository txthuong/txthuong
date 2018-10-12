# Test Name                                     Description
# A_BX_BT_COMMON_SRBTNAME_0003                  Check that +SRBTNAME write command has effect on both BT Classic and BLE
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

    print "\nGet BlueTooth address"
    SagSendAT(uart_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    dut_bluetooth_address = resp.split('"')[1]
    
    # AUX1 Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, "AT+FMM\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, "ATI3\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_BT_COMMON_SRBTNAME_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_COMMON_SRBTNAME_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check that +SRBTNAME write command has effect on both BT Classic and BLE" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    default_name = res.split('"')[1]
    print default_name
    
    print "\nStep 2: Read BLE configuration\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "%s",23,1,0\r\n' %default_name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    name = 'BX310x_DUT'
    print "\nStep 3: Change the BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME=%s\r' %name)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTNAME: "%s"\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Set module to discoverable mode\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: On AUX: Execute inquiry to find if BT name is correct\n"
    SagSendAT(aux1_com, 'AT+SRBTINQ=10,1,0\r')
    res = SagWaitResp(aux1_com, [''], 40000)
    if name not in res:
        print "name not in res"
        VarGlobal.statOfItem = "NOK"
    
    print "\nStep 8: Read BLE configuration\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "%s",23,1,0\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 9: Start BLE advertising\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: On AUX: Scan device in the area to find if BT name is correct\n"
    SagSendAT(aux1_com, 'AT+SRBLESCAN=5,0\r')
    res = SagWaitResp(aux1_com, [''], 40000)
    if name not in res:
        print "name not in res"
        VarGlobal.statOfItem = "NOK"

    name = 'BX310x_New_Name'
    print "\nStep 11: Change the BT name by +SRBLE\n"
    SagSendAT(uart_com, 'AT+SRBLE="%s",23,1\r' %name)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Read BT name\n"
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTNAME: "%s"\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Set module to discoverable mode\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: On AUX: Execute inquiry to find if BT name is correct\n"
    SagSendAT(aux1_com, 'AT+SRBTINQ=10,1,0\r')
    res = SagWaitResp(aux1_com, [''], 40000)
    if name not in res:
        print "name not in res"
        VarGlobal.statOfItem = "NOK"
    
    print "\nStep 8: Read BLE configuration\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "%s",23,1,0\r\n' %name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 9: Start BLE advertising\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: On AUX: Scan device in the area to find if BT name is correct\n"
    SagSendAT(aux1_com, 'AT+SRBLESCAN=5,0\r')
    res = SagWaitResp(aux1_com, [''], 40000)
    if name not in res:
        print "name not in res"
        VarGlobal.statOfItem = "NOK"
    
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
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

#Restore name to default
SagSendAT(uart_com, 'AT+SRBTNAME=%s\r' %default_name)
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
