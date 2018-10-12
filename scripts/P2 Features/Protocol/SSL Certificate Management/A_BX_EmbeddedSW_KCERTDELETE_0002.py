# Test Name                             Description
# A_BX_EmbeddedSW_KCERTDELETE_0002      Check that certificate can be delete properly
#
# Requirement
#   1 Euler module
#
# Author: txthuong
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

strValidCert1 = """-----BEGIN CERTIFICATE-----
MIIDIjCCAougAwIBAgIJAN9xGzmGzA4+MA0GCSqGSIb3DQEBBAUAMGoxCzAJBgNV
BAYTAkZSMRcwFQYDVQQIEw5IYXV0cyBkZSBTZWluZTEcMBoGA1UEBxMTSXNzeS1s
ZXMtTW91bGluZWF1eDETMBEGA1UEChMKV2F2ZWNvbSBTQTEPMA0GA1UEAxMGd2lw
c3NsMB4XDTA2MTIxNDE2MzAwOFoXDTE2MTIxMTE2MzAwOFowajELMAkGA1UEBhMC
RlIxFzAVBgNVBAgTDkhhdXRzIGRlIFNlaW5lMRwwGgYDVQQHExNJc3N5LWxlcy1N
b3VsaW5lYXV4MRMwEQYDVQQKEwpXYXZlY29tIFNBMQ8wDQYDVQQDEwZ3aXBzc2ww
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALrLrMLZTchpAM9oMzCXCf//ivW7
BoZ9bXoF8eISkf+ddDf2dpUmR5lbqwVAbHDm0i71PcVX7TZOWgkO0A0nN00dHy4J
0D6w6Ge7H2te2KBH7XWodPOwMhR00jle9E7XU7n5mFjotbsk3fQ4fqYZH9M/UJPE
4eMz+odgNobMtqOnAgMBAAGjgc8wgcwwHQYDVR0OBBYEFPL9xIwppGPnZ4yV4BNS
W4Lb4LtzMIGcBgNVHSMEgZQwgZGAFPL9xIwppGPnZ4yV4BNSW4Lb4LtzoW6kbDBq
MQswCQYDVQQGEwJGUjEXMBUGA1UECBMOSGF1dHMgZGUgU2VpbmUxHDAaBgNVBAcT
E0lzc3ktbGVzLU1vdWxpbmVhdXgxEzARBgNVBAoTCldhdmVjb20gU0ExDzANBgNV
BAMTBndpcHNzbIIJAN9xGzmGzA4+MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEE
BQADgYEAbm5j3kXs25Le+20SsPbhw7bX5lc8cNDMCRal9YcVCLG71rUxXdmcxZb4
yEDMHRDZ+JcA5WUUTjG3W+jgAdVP7ppExiuRwgFUpUIa1uexA1WY/a/Mv0f91GXA
+u6o+tMIFr6hsngw2qeDzuwfnsqvfTRdEWxqXXNSMsk/K+Nf4uk=
-----END CERTIFICATE-----
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
# A_BX_EmbeddedSW_KCERTDELETE_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KCERTDELETE_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check that certificate can be delete properly" % test_ID
    print "***********************************************************************************************************************"

    print '\nStep 1: Check default certificate'
    SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStore the cert with <NbData> ...'
    print '\nStep 2: Store root CA'
    SagSendAT(uart_com, 'AT+KCERTSTORE=0,%s\r' % len(strValidCert1)) 
    if SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 3000):
        SagSendAT(uart_com, strValidCert1)
        send_escape(uart_com)
    SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['root_cert,0,%s\r\n' % len(strValidCert1)], 2000)
    SagWaitnMatchResp(uart_com, ['%s\r\n' % strValidCert1], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Delete the stored cert'
    SagSendAT(uart_com, 'AT+KCERTDELETE=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    for index in [0, 1, 2]:
        print '\nStep 4: Store local certificate'
        SagSendAT(uart_com, 'AT+KCERTSTORE=1,%s,%s\r' % (len(strValidCert1), index))
        if SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 3000):
            SagSendAT(uart_com, strValidCert1)
            send_escape(uart_com)
        SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
        SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['local_cert,%s,%s\r\n' % (index, len(strValidCert1))], 2000)
        SagWaitnMatchResp(uart_com, ['%s\r\n' % strValidCert1], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nStep 5: Delete the stored cert'
        SagSendAT(uart_com, 'AT+KCERTDELETE=1,%s\r' % index)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
        SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 6: Query stored cert'
    SagSendAT(uart_com, 'AT+KCERTSTORE?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+KCERTSTORE\r\n\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: Certs were not deleted properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg:
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
