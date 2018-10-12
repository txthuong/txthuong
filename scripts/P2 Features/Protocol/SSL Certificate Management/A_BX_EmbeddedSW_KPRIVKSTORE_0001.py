# Test Name                             Description
# A_BX_EmbeddedSW_KPRIVKSTORE_0001      Check syntax for AT+KPRIVKSTORE command
#
# Requirement
#   1 Euler module
#
# Author: txthuong
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

strValidKey = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDX7FDBP5jK7yOW63Ewo+EDQPv/7qPM9CyJk5m1n2cj0gyWSLjP
3w9tjqO1/G8j7sAJDY4TP6fI7bWF5JPTFJVzuoZeW0Gs5JN2sxto085eBPRF/XxP
MgDr6lNzGULUGLykResTUo6yaQLpCedF0EHo+p8ycDiADVmxca8T39mm8wIDAQAB
AoGAen1KynYDfYvvypvB2G//I9NnoaaFMa2K3njnB8tnvUBZd5/Fh9bob6QtZv3P
Jrk4I2qXIIBJ9Ig1I8GpwmK47KQ6Ky2zBHTBcbGzhaDnECJOwTlqZe2Iv2IO96zo
sKy7kCFVooQeOeeS21E98ko0aBsVPZ/ZFLANbXQ9qQv2V4ECQQD//ZbWoYln0kNv
g5+nwWW9Q214hPOPYdz7f/P+bYGDrrQD+fua1GrH0AW2SMYmnDdSoIJFbpNl5IdN
fJZtwSBhAkEA1+5ZUZm4UYM5mtdftNNGBmTC0G/nuGO5WcmjTCIPi8/kPhnilq88
HjZFCQ0S71qtkdA3y8YUFpDna5vnE4tX0wJARSAUODb8pLVpklZHqYQW1gm8KNw1
7NTvWFaP63dkjsuBPsWlRITxpK0ura9vGoP6iGxhYSBf2xbf1nO7Jz4MYQJBAMxn
5geYA+Kt3V8V2JSdl2FACyczd+CWDoTPmxTb/Wl1n/Oln1jTg456AzoBNVZ9uWcZ
+2ecF7IQ8/FrAQEAXF8CQQDhhz0SB3zWEQASOoUJ3y3cVrISm4FAW9KOGy/0NNGq
grgMzLppMep4drFbLoC/VUBPPuIH/FO/+R/JDfuadGmR
-----END RSA PRIVATE KEY-----
"""
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

def send_escape(uart_com):
    SagSleep(1500)
    SagSendAT(uart_com, '+++')
    SagSleep(1500)
    resp = SagWaitResp(uart_com, ['\r\nOK\r\n', '*\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 5000)
    if not SagMatchResp(resp, ['\r\nOK\r\n']):
        if not SagMatchResp(resp, ['*\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n']):
            SagSendAT(uart_com, 'AT\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '*\r\nERROR\r\n', "\r\n+CME ERROR: *\r\n"], 5000, update_result="not_critical")

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KPRIVKSTORE_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KPRIVKSTORE_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check syntax of command AT+KPRIVKSTORE" % test_ID
    print "***********************************************************************************************************************"

    print '\nStep 1: Check +KPRIVKSTORE test command'
    SagSendAT(uart_com, 'AT+KPRIVKSTORE=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print '\nStep 2: Check +KPRIVKSTORE execute command'
    SagSendAT(uart_com, 'AT+KPRIVKSTORE\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print '\nStep 3: Check +KPRIVKSTORE read command'
    SagSendAT(uart_com, 'AT+KPRIVKSTORE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KPRIVKSTORE\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print '\nStep 4: Check +KPRIVKSTORE write command with invalid parameter <index>'
    for index in [-1, 3, 'a', 'A', '#', '$']:
        SagSendAT(uart_com, 'AT+KPRIVKSTORE=%s,30\r' % index)
        if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000):
            send_escape(uart_com)

    print '\nStep 5: Check +KPRIVKSTORE write command with invalid parameter <NbData>'
    for nbdata in [-1, 0, 3001, 'a', 'A', '#', '$']:
        SagSendAT(uart_com, 'AT+KPRIVKSTORE=0,%s\r' % nbdata)
        if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000):
            send_escape(uart_com)

    print '\nStep 6: Check +KPRIVKSTORE write command with missing parameters'
    SagSendAT(uart_com, 'AT+KPRIVKSTORE=\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000):
        send_escape(uart_com)
    SagSendAT(uart_com, 'AT+KPRIVKSTORE=1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000):
        send_escape(uart_com)

    print '\nStep 7: Check +KPRIVKSTORE write command with extra parameter'
    SagSendAT(uart_com, 'AT+KPRIVKSTORE=0,100,1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000):
        send_escape(uart_com)

    print '\nStep 8: Check +KPRIVKSTORE write command with valid parameters'
    for index in [0, 1, 2]:
        SagSendAT(uart_com, 'AT+KPRIVKSTORE=%s,%s\r' % (index, len(strValidKey)))
        if SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 3000):
            SagSendAT(uart_com, strValidKey)
            send_escape(uart_com)

    print "\nTest Steps completed"

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

# Close UART
SagClose(uart_com)
