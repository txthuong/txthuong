import sys
sys.path.append(".\oneclick\AppModule")
import os
import sys
import subprocess
import shutil
import re
import signal
from time import sleep, time
import win32com
import win32com.client
from tempfile import mkstemp
from subprocess import Popen
from makehtml import myLog2Html
from log2html import log2html_converter
from win32com.client import Dispatch
import traceback
import shutil
from suds.client import Client
from datetime import datetime
import threading
import telnetlib
import ConfigParser
import serial
#import visa
import serial.tools.list_ports
import psutil
import os.path
import string
import pprint
# from PowerSuppy import POWERSUPPLY

import pprint
import os

#*******************************************************************


def Load():
    ##        autotest_pids = get_pids()
    # print '----getting pid of autotest.py ----\n'
    # print autotest_pids
    # for each_pid in autotest_pids:
    # try:
    ##                p_temp = psutil.Process(each_pid)
    # p_temp.terminate()
    # except Exception,e:
    # print type(e)
    # print e
    # return
    pass


def SendAT(comPort, commands):
    print 'debug : comPort %s' % str(comPort)
    
    ser = serial.Serial(str(comPort))
    ser.baudrate = '115200'
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.timeout = 2
    # ser.rtscts = True
    # ser.dsrdtr  = True

    ser.write(commands)
    print "%s => %s" % (comPort, commands.replace('\r', '<CR>').replace('\n', '<LF>'))
    sleep(1)
    output = ''
    while ser.inWaiting() > 0:
        output += ser.read(1)

    sleep(0.1)
    while ser.inWaiting() > 0:
        output += ser.read(1)
    ser.close()
    if output != '':
        print "%s <= %s" % (comPort, output.replace('\r', '<CR>').replace('\n', '<LF>'))
    return output

#-----------------------------------------------------------------------


def getScriptRev(script_name):
    revision = 'Unknow'
    try:
        import svn.local
        print "svn local client at %s" % (r"%s\scripts" % os.environ['WORKSPACE'])
        r = svn.local.LocalClient(r"%s\scripts" % os.environ['WORKSPACE'])
        info = r.info("%s" % script_name)
        revision = info['commit#revision']
        print revision
    except Exception, e:
        print e
        traceback.print_exc()
        print "\n---->Problem: exception come out when check script revision for %s !!!\n" % script_name

    return revision


#-----------------------------------------------------------------------


def update_file(file_path, pattern, subst):
    regex = re.compile(pattern, re.IGNORECASE)
    fh, abs_path = mkstemp()
    with open(abs_path, 'wb') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                #new_file.write(line.replace(pattern, subst))
                new_file.write(regex.sub(subst, line))
    os.close(fh)
    # Remove original file
    os.remove(file_path)
    # Move new file
    shutil.move(abs_path, file_path)


def get_version_from_log(log_path):
    temp = 'Unkown Version'
    try:
        with open(log_path, "rb") as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                if "AT+CGMR" in lines[i]:
                    temp = lines[i + 1].split("<CR><LF>")[1]
                    break
    except:
        print "---->Problem: exception when search firmware verion in %s" % log_path
    return temp


#-------------------------------------------------------------------------
def calculate_how_long(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


print '\n\n'
print "*************************************************************************************************************"
print "                                       One Click Test System Start"
print "                                           %s" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
print "*************************************************************************************************************"
print '\n\n'


#-------------------------------------------------------------------------
def check_enviroment():
    print "---------Begin of Test Enviroment Creation---------\n"

    print 'create working directory:'
    for loop in range(1, int(os.environ['Loop'])+1):
        if not os.path.exists(r"%s\loop%s" % (log_path, str(loop))):
            os.makedirs(r"%s\loop%s" % (log_path, str(loop)))
            print r"%s\loop%s is created." % (log_path, str(loop))

    # if 'STT_USBPORT1' in debug_environ.keys():
        # # -1 to disable
        # if debug_environ['STT_USBPORT1'] == '-1':
            # pass
        # else:
            # for loop in range(1, 5 + 1):
                # if not os.path.exists(r"%s\loop%s" % (sSTT_TracePath, str(loop))):
                    # os.makedirs(r"%s\loop%s" % (sSTT_TracePath, str(loop)))
                    # print r"%s\loop%s is created." % (sSTT_TracePath, str(loop))

    if not os.path.isfile(autotest_plus_path):
        print "---->Problem: %s is missing !!!" % autotest_plus_path
    if not os.path.exists(cfg_path):
        os.makedirs(cfg_path)
        print "%s is created." % cfg_path
    print '---------------------------------'+report_path
        
    if not os.path.exists(report_path):
        os.makedirs(report_path)
        print "%s is created." % report_path

    for loop in range(1, int(os.environ['Loop'])+1):
        if not os.path.exists(r"%s\loop%s" % (log_path_html, str(loop))):
            os.makedirs(r"%s\loop%s" % (log_path_html, str(loop)))
            print "%s\loop%s is created." % (log_path_html, str(loop))

    if os.path.isfile(cfg_file_with_path):
        os.remove(cfg_file_with_path)
        print "\n%s is deleted " % cfg_file_with_path

    sleep(3)

    if not os.path.isfile(cfg_file_with_path):
        print r"Copy sample.cfg from %s\configuration_file\sample.cfg." %os.environ['WORKSPACE']
        # shutil.copyfile(r"C:\AutoTestLibrary\sample\sample.cfg",cfg_file_with_path)
        shutil.copyfile(r"%s\configuration_file\sample.cfg" %
                        os.environ['WORKSPACE'], cfg_file_with_path)
        print "%s is created." % cfg_file_with_path
    print "\n---------End of Test Enviroment Creation---------\n"

#-------------------------------------------------------------------------


def update_cfg():
    for field in ["UART_COM", "AUX1_COM", "AUX2_COM", "WIFI_SSID", "WIFI_MAC_ADDR", "WIFI_PASSWORD", "HTTP_SERVER", "HTTP_SERVER_IP_ADDRESS", "HTTPS_SERVER", "HTTPS_SERVER_IP_ADDRESS", "MQTT_SERVER", "TCP_SERVER","TCP_PORT", "UDP_SERVER","UDP_PORT", "DUT_MAC_ADDRESS", "AUX1_MAC_ADDRESS", "AUX2_MAC_ADDRESS", "DUT_BLUETOOTH_ADDRESS", "AUX1_BLUETOOTH_ADDRESS", "AUX2_BLUETOOTH_ADDRESS", "DUT_MAC_ADDRESS_STA", "AUX1_MAC_ADDRESS_STA", "HTTP_USER", "HTTP_PASSWORD", "HTTP_SERVER2", "HTTPS_SERVER2", "AVMS", "HTTPS_PORT", "WIFI_DHCP_GATEWAY", "WIFI_DHCP_SUBNET_MASK"]:
        try:
            if (field in os.environ) and ('AVMS' in field):
                update_file(cfg_file_with_path, "^%s\s*=\s*\d*" %
                            field, "%s = {%s}" % (field.lower(), os.environ[field]))
                print "%s = %s" % (field, os.environ[field])
                
            elif field in os.environ:
                update_file(cfg_file_with_path, "^%s\s*=\s*\d*" %
                            field, "%s = '%s'" % (field.lower(), os.environ[field]))
                print "%s = %s" % (field, os.environ[field])
                
        except Exception, e:
            print e
            traceback.print_exc()
            print "---->Exception comes when update %s !!!" % field
    # for field in ["HARD_INI", "SOFT_INI", "NETWORK_INI", "SIM_INI", "AUX_SIM_INI", "AVMS_INI", "AVMS_LOCAL_DELTA", "AVMS_LOCAL_DELTA_FALLBACK", "PowerSupply", "CMW_USB_PORT"]:
        # try:
            # if field in os.environ:
                # # print str(os.environ[field])
                # new_value = "r'%s'" % os.environ[field]
                # if os.environ[field] in [None, 'None']:
                    # new_value = "r''"
                # update_file(cfg_file_with_path, "^%s\s*=\s*\S*" %
                            # field, "%s = %s" % (field, new_value))
                # print "%s = %s" % (field, new_value)
        # except Exception, e:
            # print e
            # traceback.print_exc()
            # print "---->Exception comes when update %s !!!" % field

#-------------------------------------------------------------------------


def update_TestLab_OneClick(qc_path, qc_campaign, one_click_filter, test_number):
    qc_d = {}
    try:
        qcServer = r"http://10.40.11.70:8080/qcbin/"
        qcUser = "oneclick"
        qcPassword = "sierra_211"
        qcDomain = "DEFAULT"
        qcProject = "Validation"

        print "\n---------Update 1-Click Field in TestLab---------\n"

        print "QC login ..."
        t = win32com.client.Dispatch("TDApiOle80.TDConnection")
        t.InitConnectionEx(qcServer)
        t.Login(qcUser, qcPassword)
        t.Connect(qcDomain, qcProject)

        print "QC Logged in"

        mg = t.TreeManager
        npath = qc_path  # r"Root\AT\INTEL\HL75xx_Beatles"
        tsFolder = t.TestSetTreeManager.NodeByPath(npath)

        tfactory = tsFolder.TestSetFactory
        td_tsff = tfactory.Filter  # ('TS_USER_21')
        td_testset = td_tsff.NewList()

        tsList = tsFolder.FindTestSets(qc_campaign)  # ("AT_HL7518_Beatles")
        otest = tsList.Item(1)
        td_TSTestSetFactory = otest.TSTestFactory
        tetsFilter = td_TSTestSetFactory.Filter
        tetsFilter.SetFilter('TS_NAME', test_number)
        tetsFilter.SetFilter('TC_USER_16', one_click_filter)  # rtn
        td_tstsff = td_TSTestSetFactory.NewList(tetsFilter.Text)

        for otestitem in td_tstsff:
            otestitem.SetField('TC_USER_16', "")
            otestitem.Post()
            print "Run me in 1-Click field of %s has been removed " % otestitem.Field("TS_NAME")

        t.Logout()
        print "\nQC log out\n"
        print "\n---------End of Update 1-Click Field in TestLab---------\n"
    except:
        print "\n---->Problem : Fail to remove Run me in 1-Click field of %s !!!" % test_number

    return qc_d
#-------------------------------------------------------------------------


def update_TestLab_Field(qc_path, qc_campaign, filed_name, test_number, message):
    qc_d = {}
    try:
        qcServer = r"http://10.40.11.70:8080/qcbin/"
        qcUser = "oneclick"
        qcPassword = "sierra_211"
        qcDomain = "DEFAULT"
        qcProject = "Validation"

        print "\n---------Update %s Field in TestLab---------\n" % filed_name

        d_field = {'Comment': 'TC_USER_01'}

        print "QC login ..."
        t = win32com.client.Dispatch("TDApiOle80.TDConnection")
        t.InitConnectionEx(qcServer)
        t.Login(qcUser, qcPassword)
        t.Connect(qcDomain, qcProject)

        print "QC Logged in"

        mg = t.TreeManager
        npath = qc_path  # r"Root\AT\INTEL\HL75xx_Beatles"
        tsFolder = t.TestSetTreeManager.NodeByPath(npath)

        tfactory = tsFolder.TestSetFactory
        td_tsff = tfactory.Filter  # ('TS_USER_21')
        td_testset = td_tsff.NewList()

        tsList = tsFolder.FindTestSets(qc_campaign)  # ("AT_HL7518_Beatles")
        otest = tsList.Item(1)
        td_TSTestSetFactory = otest.TSTestFactory
        tetsFilter = td_TSTestSetFactory.Filter
        tetsFilter.SetFilter('TS_NAME', test_number)
        td_tstsff = td_TSTestSetFactory.NewList(tetsFilter.Text)

        for otestitem in td_tstsff:
            otestitem.SetField(d_field[filed_name], message)
            otestitem.Post()
            print "\n%s field of %s has been updated to %s " % (filed_name, test_number, message)

        t.Logout()
        print "\nQC log out\n"
        print "\n---------End of Update Field in TestLab---------\n"
    except Exception, e:
        print e
        traceback.print_exc()
        print "\n---->Problem : Fail to update %s field of %s !!!" % (filed_name, test_number)

    return qc_d
#-------------------------------------------------------------------------


def import_Result_ToQC(qc_path, qc_campaign, test_number, d_result):
    qc_d = {}
    # print d_result
    
    try:
        qcServer = r"http://10.40.11.70:8080/qcbin/"
        qcUser = "oneclick"
        qcPassword = "sierra_211"
        qcDomain = "DEFAULT"
        qcProject = "Validation"

        print "\n---------Import result of %s in %s/%s ---------\n" % (test_number, qc_path, qc_campaign)

        print "QC login ..."
        t = win32com.client.Dispatch("TDApiOle80.TDConnection")
        t.InitConnectionEx(qcServer)
        t.Login(qcUser, qcPassword)
        t.Connect(qcDomain, qcProject)

        print "QC Logged in"

        mg = t.TreeManager
        npath = qc_path  # r"Root\AT\INTEL\HL75xx_Beatles"
        tsFolder = t.TestSetTreeManager.NodeByPath(npath)

        tfactory = tsFolder.TestSetFactory
        td_tsff = tfactory.Filter  # ('TS_USER_21')
        td_testset = td_tsff.NewList()

        tsList = tsFolder.FindTestSets(qc_campaign)  # ("AT_HL7518_Beatles")
        otest = tsList.Item(1)
        td_TSTestSetFactory = otest.TSTestFactory
        tetsFilter = td_TSTestSetFactory.Filter
        tetsFilter.SetFilter('TS_NAME', test_number)
        td_tstsff = td_TSTestSetFactory.NewList(tetsFilter.Text)

        for otestitem in td_tstsff:
            td_RunFactory = otestitem.RunFactory
            for i in range(1, 5 + 1):
                if d_result[test_number]['result']['loop%s' % str(i)]['status'] in ['Passed', 'Failed']:
                    obj_theRun = td_RunFactory.AddItem(
                        "Run_" + datetime.now().strftime("%m-%d_%H-%M-%S"))
                    obj_theRun.Status = d_result[test_number][
                        'result']['loop%s' % str(i)]['status']
                    obj_theRun.SetField('RN_USER_01', d_result[test_number][
                                        'FW version'])  # VersionSoft
                    obj_theRun.SetField('RN_USER_02', "N/A")  # Flash Tyep
                    obj_theRun.SetField('RN_USER_03', os.environ[
                                        'Module_Type'])  # Module Tyep
                    obj_theRun.SetField('RN_USER_04', os.environ[
                                        'Module_Ref'])  # Module Ref
                    obj_theRun.SetField('RN_USER_05', "Platform: %s, Build: %s, Loop: %s" % (d_result[
                                        test_number]['job_name'], d_result[test_number]['build_number'], str(i)))  # Comment
                    obj_theRun.SetField('RN_USER_08', os.environ[
                                        'SIM_INI'].split('\\')[-1].split('.')[0])  # SIM
                    obj_theRun.SetField(
                        'RN_USER_09', "1-click")  # Test Equipment
                    obj_theRun.SetField(
                        'RN_USER_17', "1-Click checking only")  # Issue ID
                    obj_theRun.SetField('RN_TESTER_NAME', "oneclick")  # Tester

                    otestitem.SetField('TC_USER_02', d_result[test_number][
                                       'FW version'])  # VersionSoft
                    otestitem.SetField('TC_USER_03', os.environ[
                                       'Module_Type'])  # Module Type
                    otestitem.SetField('TC_USER_04', "N/A")  # Flash Type
                    otestitem.SetField('TC_USER_05', os.environ[
                                       'Module_Ref'])  # Module Ref
                    otestitem.SetField('TC_USER_06', os.environ[
                                       'SIM_INI'].split('\\')[-1].split('.')[0])  # sim
                    # Test Equipment
                    otestitem.SetField('TC_USER_08', "1-click")
                    otestitem.SetField(
                        'TC_USER_11', "Not Applicable")  # Plugin
                    otestitem.SetField('TC_ACTUAL_TESTER', d_result[
                                       test_number]['Feature_Owner'])  # Tester
                    otestitem.Status = d_result[test_number][
                        'result']['loop%s' % str(i)]['status']

                    obj_theRun.Post()
                    otestitem.Post()
                    print "\n%s import done " % test_number,

        t.Logout()
        print "\nQC log out\n"
        print "\n--------- End of Import Result to QC ---------\n"
    except Exception, e:
        print e
        traceback.print_exc()
        print "\n---->Problem : Fail to import result to QC !!!"
    
    return qc_d
#-------------------------------------------------------------------------


def checkSBM(issueid):
    result = 'CheckFailed'
    try:
        SBM_USERNAME = "hk_validation"
        SBM_PASSWORD = "sierra_211"
        SBM_WSDL = "http://frilm-sbm02/gsoap/sbmappservices72.wsdl"
        SBM_ENDPOINT = "http://frilm-sbm02/gsoap/gsoap_ssl.dll?sbmappservices72"
        ### attaches a given file to a specified SCR in SBM ###
        client = Client(url=SBM_WSDL, location=SBM_ENDPOINT)
        auth = client.factory.create('ae:Auth')
        auth.userId = SBM_USERNAME
        auth.password = SBM_PASSWORD
        print "ISSUE ID : %s" % issueid

        table = client.factory.create('ae:TableIdentifier')
        table.dbName = "TTT_WM_SW"
        where = "TS_ISSUEID = '%s'" % (issueid)

        answer = client.service.GetItemsByQuery(auth, table, where)
        ### Get the status for item ###
        status = answer.item[0].activeInactive

        if status == "true":
            result = 'Active'
            print "Item ID: " + issueid + " Status: Active\n"
        elif status == "false":
            result = 'Inactive'
            print "Item ID: " + issueid + " Status: Inactive\n"
        else:
            print "Item not found"
    except Exception, e:
        print e
        traceback.print_exc()
        print "\n---->Problem: Fail to check %s in SBM !!!\n" % issueid

    return result

#-------------------------------------------------------------------------


def get_TestNumber_From_QC(qc_path, qc_campaign, filter_text,
                           one_click_filter="Not Use",
                           status_filter="Not Use",
                           tester_filter="Not Use",
                           test_name_filter="Not Use",
                           test_carrier_filter="Not Use",
                           test_conditions_filter="Not Use",
                           test_feature_filter="Not Use",
                           test_category_filter="Not Use",
                           test_Execution_Status="Not Use"
                           ):
    qc_d = {}

    try:
        print "\n---------Extrieve Test Case from QC---------\n"

        # NOTE llaw, disable print out for unmecessary
        # print "Now we are going to %s:%s under with below filter:" %
        # (qc_path, qc_campaign)

        print "QC path                : %s" % qc_path
        print "QC campaign            : %s" % qc_campaign
        print "TestPlatform           : %s" % filter_text
        print "one_click_filter       : %s" % one_click_filter
        print "status_filter          : %s" % status_filter
        print "tester_filter          : %s" % tester_filter
        print "test_name_filter Name  : %s" % test_name_filter
        print "test_carrier_filter    : %s" % test_carrier_filter
        print "test_conditions_filter : %s" % test_conditions_filter
        print "test_feature_filter    : %s" % test_feature_filter
        print "test_category_filter   : %s" % test_category_filter
        print "test_Execution_Status  : %s" % test_Execution_Status
        print "\n"

        print "QC login ..."
        t = win32com.client.Dispatch("TDApiOle80.TDConnection")
        t.InitConnectionEx(qcServer)
        t.Login(qcUser, qcPassword)
        t.Connect(qcDomain, qcProject)

        print "QC Logged in"

        mg = t.TreeManager
        npath = qc_path  # r"Root\AT\INTEL\HL75xx_Beatles"
        tsFolder = t.TestSetTreeManager.NodeByPath(npath)

        tfactory = tsFolder.TestSetFactory
        td_tsff = tfactory.Filter  # ('TS_USER_21')
        td_testset = td_tsff.NewList()

        tfactory = tsFolder.TestSetFactory
        td_tsff = tfactory.Filter  # ('TS_USER_21')
        td_testset = td_tsff.NewList()

        tsList = tsFolder.FindTestSets(qc_campaign)  # ("AT_HL7518_Beatles")
        # tsList = tsFolder.NodeById(12547) #("AT_HL7518_Beatles")

        otest = tsList.Item(1)
        print otest.Name

        td_TSTestSetFactory = otest.TSTestFactory
        tetsFilter = td_TSTestSetFactory.Filter
        tetsFilter.SetFilter('TS_USER_21', filter_text)
        if one_click_filter != "Not Use":
            tetsFilter.SetFilter('TC_USER_16', one_click_filter)  # run me
        if status_filter != "Not Use":
            tetsFilter.SetFilter('TC_STATUS', status_filter)  # replay
        if tester_filter != "Not Use":
            tetsFilter.SetFilter('TC_ACTUAL_TESTER', tester_filter)  # rtn

        if test_name_filter == "Not Use":
            tetsFilter.SetFilter('TS_NAME', "*")  # test name
        else:
            tetsFilter.SetFilter('TS_NAME', test_name_filter)  # test name

        if test_carrier_filter != "Not Use":
            tetsFilter.SetFilter('TS_USER_14', test_carrier_filter)  # Carrier
        if test_conditions_filter != "Not Use":
            tetsFilter.SetFilter( 'TS_USER_01', test_conditions_filter)  # Conditions
        if test_feature_filter != "Not Use":
            tetsFilter.SetFilter('TS_USER_13', test_feature_filter)  # Feature
            # print one_click_filter

        # NOTE llaw, add for selecting non-stress testcase
        if test_category_filter != "Not Use":
            tetsFilter.SetFilter(  'TS_USER_18', test_category_filter)  # test:category
        # NOTE llaw, add for selecting non-stress testcase

        # NOTE llaw, add for selecting periodic testcase
        if test_Execution_Status != "Not Use":
            # test:Execution status
            tetsFilter.SetFilter('TS_EXEC_STATUS', test_Execution_Status)
        # NOTE llaw, add for selecting periodic testcase

        td_tstsff = td_TSTestSetFactory.NewList(tetsFilter.Text)

        print "\nBelow test case shall be run:"

        for otestitem in td_tstsff:
            TestNameInstance = "%s%s" % (otestitem.Field("TC_NAME").split(" ")[
                                         1], otestitem.Field("TC_NAME").split(" ")[0])
            qc_d[otestitem.Field("TS_NAME")] = {'LastStatus': otestitem.Field("TC_STATUS"),
                                                'IssueID': otestitem.Field("TC_USER_19"),
                                                'Script': otestitem.Field("TS_USER_05").strip(),
                                                'Instance': TestNameInstance,
                                                # 'EstimatedTime': otestitem.Field("TS_ESTIMATE_DEVTIME"),
                                                # 'TestID': otestitem.Field("TSC_TEST_ID"),
                                                'ResponsibleTester': otestitem.Field("TC_TESTER_NAME"),
                                                'Feature_Owner': otestitem.Field("TC_ACTUAL_TESTER"),
                                                'Catetory(TS_USER_18)': otestitem.Field("TS_USER_18"),
                                                'TestPlatform(TS_EXEC_STATUS)': otestitem.Field("TS_USER_21"),
                                                'TestExectutionStatus(TS_EXEC_STATUS)': otestitem.Field("TS_EXEC_STATUS")
                                                #'VersionSoft':otestitem.Field("TC_USER_02")

                                                }
            print "%s" % otestitem.Field("TS_NAME")
            # print "%s" % otestitem.Field("TS_USER_05")
            # print "\n"

        temp = {}

        print "\n\nNow we are checking the run history..."
        try:
            for i in range(1, td_tstsff.Count + 1):
                try:
                    ts_instance = td_tstsff.Item(i)
                    ts_run_factory = ts_instance.RunFactory
                    runs = ts_run_factory.NewList("")

                    if len(runs) != 0:
                        run_status = 'Unknow'
                        run_version = 'Unknow'

                        for run in runs:
                            if run.Field("RN_STATUS") != 'Replay':
                                run_status = run.Field("RN_STATUS")
                                #run_version = run.Field("RN_USER_01")
                                break

                        temp[run.Field("TS_NAME")] = {'LastStatus': run_status,
                                                      #'VersionSoft':run_version,
                                                      'IssueID': ts_instance.Field("TC_USER_19")
                                                      }

                        print "%s result of last run: %s, Issue ID: %s" % (run.Field("TS_NAME"), temp[run.Field("TS_NAME")]['LastStatus'], temp[run.Field("TS_NAME")]['IssueID'])
                except Exception, e:
                    print e
                    traceback.print_exc()
                    print "\n---->Problem : Fail to scan run history for one test case !!!!\n"

            for tc in qc_d.keys():
                if qc_d[tc]['LastStatus'] == 'Replay':
                    qc_d[tc]['LastStatus'] = temp[tc]['LastStatus']
                    #qc_d[tc]['VersionSoft'] = temp[tc]['VersionSoft']
                    print "%s resulst is replay, replaced with run history data : %s" % (tc, temp[tc]['LastStatus'])

        except Exception, e:
            print e
            traceback.print_exc()
            print "\n---->Problem : Fail to scan run history !!!!\n"

        t.Logout()
        print "\nQC log out\n"
        print "\n---------End of Extrieve Test Case from QC---------\n"

        print "--------- Now check each issue ID state in SBM ---------\n"

        for tc in qc_d.keys():
            if qc_d[tc]['IssueID'] is None:
                continue
            m = re.findall('(ANO|CUS|DEV)(\d{5,6})', qc_d[
                           tc]['IssueID'], re.DOTALL)
            temp = ''
            if bool(m):
                try:
                    for each in m:
                        print "%s%s is checking in SBM " % (each[0], each[1])
                        temp += "%s%s" % (each[0], each[1])
                        temp += '-'
                        temp += checkSBM(each[1])
                        temp += '; '
                except:
                    print "\n---->Problem: when check %s%s in SBM" % (each[0], each[1])
                temp = temp.rstrip()
                if temp.endswith(";"):
                    temp = temp[:-1]
                qc_d[tc]['IssueID'] = temp

    except Exception, e:
        # NOTE llaw, remove me after done.
        print e
        traceback.print_exc()
        print "\n---->Problem : Fail to pickup selected test case from QC !!!!\n"
    return qc_d

#-------------------------------------------------------------------------


def kill_SubProcess(p, pids):
    p.terminate()
    p.wait()

    for each_pid in pids:
        try:
            p_temp = psutil.Process(each_pid)
            p_temp.terminate()
        except Exception, e:
            print type(e)
            print e

# except psutil.NoSuchProcess:
#-------------------------------------------------------------------------
def get_pids(app="autotest.py"):
    pids = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo['name'] == app:
                print pinfo
                pids.append(pinfo['pid'])
    return pids
#-------------------------------------------------------------------------


def download_Firmware(power_supply_addr):
    result = True

    # NOTE temporary disable for debug.
    global bEnableDownloadFirmware
    if bEnableDownloadFirmware:
        if os.path.isfile(os.environ['Firmware_Under_Tested']):
            try:
                print "\nNow going to download the firmware: \n%s\n" % os.environ['Firmware_Under_Tested']
                myPower = POWERSUPPLY(ip_addr=power_supply_addr)
                myPower.off()
                sleep(10)
                print "%s : module switch off" % datetime.now().strftime("%y/%m/%d %H:%M:%S")

                print "\nCopy %s to local C driver ..." % os.environ['Firmware_Under_Tested']
                temp_firmware_name = "temp.exe"
                try:
                    temp_firmware_name = os.environ[
                        'Firmware_Under_Tested'].split("\\")[-1]
                except Exception, e:
                    print e
                    print "Firmware renamed to temp.exe\n"

                if os.path.isfile(r"C:\%s" % temp_firmware_name):
                    print "%s already is there, no need to copy." % temp_firmware_name
                else:
                    shutil.copyfile(
                        os.environ['Firmware_Under_Tested'], r"C:\%s" % temp_firmware_name)

                p = subprocess.Popen(r"C:\%s" %
                                     temp_firmware_name, shell=False)
                sleep(20)
                pids = []
                pids.append(p.pid)
                myPower.on()
                print "%s : module switch on" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                t = threading.Timer(60.0, kill_SubProcess, args=(p, pids))
                t.start()
                print t
                print "\n%s : A 60s timer is started to monitor the FW downloading" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                p.wait()
                try:
                    if t is not None:
                        if t.isAlive():
                            print "\nTerminate the monitoring process"
                            t.cancel()
                            print "%s : Timer is cancelled" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                        else:
                            print "\nMonitoring process expired, script is killed"
                    else:
                        print "Timer expired ???"
                except Exception, e:
                    result = False
                    print e
                    traceback.print_exc()
                    print "---->Problem when terminating mornitor process !!!"
                sleep(20)

                # print "\nDelete the temp firmware %s" % temp_firmware_name
                #os.remove(r"C:\%s" % temp_firmware_name)

            except Exception, e:
                print e
                traceback.print_exc()
                print "\n---->Problem : Fail to download the firmware !!!!\n"
        else:
            print "\n---->Problem: %s is not a file !!!\n" % os.environ['Firmware_Under_Tested']
    return result


def run(test_case_pool_dict):

    print "\n\n-----------------------------------------------------------------------------------------------"
    print "    Begin to Run Script"
    print "-----------------------------------------------------------------------------------------------\n\n"

    # NOTE STT log path define
    dSTT_Trace_File = {}

    # input
    # NOTE check for input
    if not bool(test_case_pool_dict):
        print "\n\nThere is no any script to run !!!"
        print "***************End of Run***************"
        return False
    
    # process
    # output

    # NOTE 1. download firmware uart_com -> AUX_COM

    try:
        # print 'debug: turn off all power before start'
        # NOTE turn off all power supply before run test.
        # TODO put me into library

        # NOTE remove me
        # if 0:
            # if 'PowerSupply' in os.environ:
                # p = re.compile("APC\d*_\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}_\d")
                # if p.match(os.environ['PowerSupply']) is not None:
                    # ip_addr = os.environ['PowerSupply']
                    # ip = ip_addr.split("_")[1]
                    # outletPort = ip_addr.split("_")[2]
                    # print "Power Suppy IP Addr = " + ip
                    # print "Outlet of Power Supply = " + outletPort
                    # tn = telnetlib.Telnet(ip, "23")
                    # tn.read_until("er Name :", 10)
                    # tn.write("apc\r\n")
                    # tn.read_until("assword  :", 10)
                    # tn.write("sf2sogo-c\r\n")
                    # # time.sleep(1)
                    # print tn.read_until("C>")
                    # tn.write("off 5\r\n")
                    # sleep(5)
                # #    print  tn.read_until("C>")
                # #    print  tn.write("on "+outletPort+"\r\n")
                    # print tn.read_until("C>")
                    # print tn.write("quit\r\n")
                    # tn.close()
                    # sleep(10)

        # if "OBNF" in os.environ['QC_Path_Test_Campaign'].lower():
            # print "\nThis is a bootcore test campaign, can not download firmware by windows exe\n"
        # else:
            # if not download_Firmware(os.environ['PowerSupply']):
                # print "\n---->Problem: Fail to download firmware, exit run to save time !!!"
                # return False
            # try:
                # if 'PowerSupply_Tester' in os.environ:
                    # if not download_Firmware(os.environ['PowerSupply_Tester']):
                        # print "\n---->Problem: Fail to download firmware for tester module, exit run to save time !!!"
                        # return False
                # elif "AUX_SIM_INI" in os.environ:
                    # print "\n\n\n---->WARN : Tester Moudle is defined but PowerSupply Address not defined for Tester, can Not download fimrware for Tester Module !!!\n\n"
                # else:
                    # print "\n---->No need download firmware for tester module."
            # except Exception, e:
                # print type(e)
                # print e
                # return False

        # print "\nNow update the version in %s\n" % os.environ['SOFT_INI']
        # scan_count = 0
        port_list = []

        # print 'debug serial.tools.list_ports.comports() start'
        # print serial.tools.list_ports.comports()
        # print 'debug serial.tools.list_ports.comports() end'

        for each_port in serial.tools.list_ports.comports():
            port_list.append(each_port[0])
        # print "\n"
        print port_list
        # print "\n"
        
        while '%s' % str(os.environ['uart_com']) not in port_list:
            print "%s is lost" % str(os.environ['uart_com'])
            print "Wait 10s..."
            sleep(10)
            scan_count += 1
            if scan_count == 5:
                break

        resp = SendAT(os.environ['uart_com'], "AT\r")
        sleep(5)
        resp = SendAT(os.environ['uart_com'], "AT+CGMR\r")
        this_firmware_version = resp.split("\r\n")[1]
        print "\nCurrent FW version : %s\n" % this_firmware_version

        # config = ConfigParser.RawConfigParser()
        # config.optionxform = str
        # config.read(os.environ['SOFT_INI'])
        # config.set('Soft', 'Version', this_firmware_version)
        # with open(os.environ['SOFT_INI'], 'wb') as configfile:
            # config.write(configfile)
        
        total_test_number = 0

        # NOTE llaw: don't touch test_case_pool_dict
        for tc in test_case_pool_dict.keys():
            for root, dirs, files in os.walk(r"%s\scripts" % os.environ['WORKSPACE']):
                for temp_file in files:
                    if test_case_pool_dict[tc]['Script'].upper() == temp_file.upper():
                        sTraceFileName = temp_file.replace(
                            '.py', '.istp').replace('.PY', '.istp')
                        dSTT_Trace_File[os.path.join(root, temp_file).replace(
                            '\\', '/')] = sTraceFileName

        # NOTE llaw: don't touch test_case_pool_dict

        for tc in test_case_pool_dict.keys():
            total_test_number += 1
            for root, dirs, files in os.walk(r"%s\scripts" % os.environ['WORKSPACE']):
                for temp_file in files:
                    if test_case_pool_dict[tc]['Script'].upper() == temp_file.upper():
                        test_case_pool_dict[tc]['Script'] = "\"%s\"" %os.path.join(root, temp_file)

        timer = {}
        versions = {}
        memo_ver = 'Unknown'
        memo_number_tc = 0
        duration_for_qc = {}
        duration_for_qc_temp = {}
        script_already_run = []
        # print test_case_pool_dict
        duration_by_script = {}

        # import pprint
        # pprint.pprint(test_case_pool_dict)

        # NOTE llaw: function this please ---
        lsSortedTCName = []
        lsExpandedByLastNum = []
        lsSortTCName = test_case_pool_dict.keys()
        for sSortTCName in lsSortTCName:
            sExpandedByLastNum = sSortTCName[-4::] + '@@' + sSortTCName
            lsExpandedByLastNum.append(sExpandedByLastNum)

        for sExpandedByLastNum in sorted(lsExpandedByLastNum):
            lsSortedTCName.append(sExpandedByLastNum.split('@@')[1])

        pprint.pprint(lsSortedTCName)
        # NOTE llaw: function this please ---

        # NOTE llaw: tc means testcase name here.
        # for tc in test_case_pool_dict.keys():
        for tc in lsSortedTCName:
            start_time = time()
            memo_number_tc = memo_number_tc + 1
            versions[tc] = ''
            no_run_to_re_run = 0

            duration_for_qc_temp[tc] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            print "\n+-----------------------------------------+"
            print "   Remaining test case number : %s" % str(total_test_number)
            print "+-----------------------------------------+"

            # TODO retry times
            # for loop in range(1,3+1):
            
            os.environ['WORKSPACE']
            #for loop in range(1, 5 + 1):
            for loop in range(1, int(os.environ['Loop']) + 1):
                try:
                    # NOTE: debug me
                    # TODO: remove me
                    # import subprocess
                    # try:
                        # subprocess.check_output(['tasklist.exe'])
                        # # subprocess.check_output(['taskkill.exe','/f','/im','python.exe','/t'])
                        # subprocess.check_output(
                            # ['taskkill.exe', '/f', '/im', 'autotest.py', '/t'])
                    # except Exception as e:
                        # pass

                    print "\n--------------------------------------------------------------------------------------------------------\n"
                    print "%s %s : loop %s\n" % (datetime.now().strftime("%y/%m/%d %H:%M:%S"), tc, str(loop))

                    #----------------------------------------------------------
                    # TODO TROUBLESHOOT ME
                    # NOTE suspect for the UART occupied.
                    # if 0:
                        # try:
                            # print "\nNow we check the COM%s is in windows device or not" % str(os.environ['uart_com'])
                            # scan_count = 0
                            # port_list = []
                            # print serial.tools.list_ports.comports()
                            # for each_port in serial.tools.list_ports.comports():
                                # port_list.append(each_port[0])
                            # print "\n"
                            # print port_list
                            # print "\n"
                            # while '%s' % str(os.environ['uart_com']) not in port_list:
                                # print "%s is lost" % str(os.environ['uart_com'])
                                # print "Wait 30s..."
                                # sleep(30)
                                # scan_count += 1
                                # if scan_count == 5:
                                    # print "Now have to do a hard reset:\n"
                                    # myPower = POWERSUPPLY(
                                        # ip_addr=os.environ['PowerSupply'])
                                    # myPower.off()
                                    # sleep(30)
                                    # myPower.on()
                                    # sleep(30)
                                # if (scan_count == 7) and ("OBNF" not in os.environ['QC_Path_Test_Campaign'].lower()):
                                    # print "\nNow we have to download firmware:"
                                    # download_Firmware(
                                        # os.environ['PowerSupply'])
                                    # sleep(30)
                                # if scan_count == 8:
                                    # print "We give up, Com Port is lost"
                                    # break
                                # port_list = []
                                # for each_port in serial.tools.list_ports.comports():
                                    # port_list.append(each_port[0])
                                # print port_list

                        # except Exception, e:
                            # print type(e)
                            # print e
                            # traceback.print_exc()
                    # #----------------------------------------------------------
                    # # TODO: TROUBLESHOOT me
                    # # NOTE: suspect for the UART occupied.
                    # if 0:
                        # print "\nNow we test the serial port is working:"
                        # serial_port_not_work = True
                        # serial_port_check = 1
                        # while serial_port_not_work:
                            # try:
                                # serial_port_check += 1
                                # if serial_port_check == 5:
                                    # break
                                # resp = SendAT(
                                    # int(os.environ['uart_com']), "ATE0\r")
                                # serial_port_not_work = False
                            # except Exception, e:
                                # print type(e)
                                # print e
                                # print "\nNow we have to download firmware:"
                                # download_Firmware(os.environ['PowerSupply'])
                                # sleep(60)
                                # traceback.print_exc()

                    # #----------------------------------------------------------

                    # if 0:
                        # if 'AVMS_INI' in os.environ:
                            # config.read(os.environ['AVMS_INI'])
                            # bad_firmware_list = []
                            # AVMS_FW_Reverse = config.get(
                                # 'Package', 'AVMS_FW_Reverse').strip()
                            # AVMS_FW_NoReverse = config.get(
                                # 'Package', 'AVMS_FW_NoReverse').strip()
                            # bad_firmware_list.append(AVMS_FW_Reverse)
                            # bad_firmware_list.append(AVMS_FW_NoReverse)

                            # resp = SendAT(
                                # int(os.environ['uart_com']), "ATE0\r")
                            # resp = SendAT(
                                # int(os.environ['uart_com']), "AT+CGMR\r")
                            # this_firmware_version_now = resp.split("\r\n")[1]

                            # print "Now firmware version : %s\n" % this_firmware_version_now
                            # if this_firmware_version_now in bad_firmware_list:
                                # print "\nNow we have to download firmware again"
                                # if "OBNF" not in os.environ['QC_Path_Test_Campaign'].lower():
                                    # download_Firmware(
                                        # os.environ['PowerSupply'])
                                    # sleep(20)
                                # else:
                                    # print "\nThis is a bootcore test campaign, can not download firmware !!!\n"
                            # pass

                    if test_case_pool_dict[tc]['Script'] not in script_already_run:
                        # NOTE procedure 1, pre-run script
                        if os.environ['PRE_RUN'] != "Not Use":
                            print "\n-->Pre-run script start<--\n"
                            print "%s will be launched first" % os.environ['PRE_RUN']
                            print "\n%s\n" % command % (cfg_file_with_path, r"%s\loop%s" % (log_path, str(loop)), r"%s\scripts\%s" % (os.environ['WORKSPACE'], os.environ['PRE_RUN']))
                            # p = Popen(command % (cfg_file_with_path, r"%s\loop%s" % (
                                # log_path, str(loop)), os.environ['PRE_RUN']), shell=False)
                            p = Popen(command % (cfg_file_with_path, r"%s\loop%s" % (
                                log_path, str(loop)), r"%s\scripts\%s" % (os.environ['WORKSPACE'], os.environ['PRE_RUN'])), shell=False)
                                
                                
                                
                            sleep(15)
                            autotest_pids = get_pids()
                            t = threading.Timer(
                                180.0, kill_SubProcess, args=(p, autotest_pids,))
                            t.start()
                            print "\n%s : A 180s timer is started to monitor the pre-run script" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            p.wait()
                            try:
                                if t.isAlive():
                                    print "\nTerminate the monitoring process"
                                    t.cancel()
                                    print "%s : Timer is cancelled\n" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                else:
                                    print "\nMonitoring process expired, script is killed\n"
                            except Exception, e:
                                print e
                                traceback.print_exc()
                                print "---->Problem when terminating mornitor process !!!\n"

                        sleep(10)
                        print "\n-->Pre-run script end<--\n"
                        import subprocess
                        try:
                            subprocess.check_output(['tasklist.exe'])
                            # subprocess.check_output(['taskkill.exe','/f','/im','python.exe','/t'])
                            subprocess.check_output(
                                ['taskkill.exe', '/f', '/im', 'autotest.py', '/t'])
                        except Exception as e:
                            pass

                        #------------------------------------------------------
                        print "\n%s\n" % command % (cfg_file_with_path, r"%s\loop%s" % (log_path, str(loop)), test_case_pool_dict[tc]['Script'])
                        # print "\nEstimated Duration: %s min" % test_case_pool_dict[tc]['EstimatedTime']

                        # print "Test ID : %s" % test_case_pool_dict[tc]['TestID']

                        # NOTE procedure 2, run test script
                        start_temp = time()
                        sPathRunScript =  test_case_pool_dict[tc]['Script']
                        if 'STT_USBPORT1' in debug_environ.keys():
                            # -1 to disable
                            if debug_environ['STT_USBPORT1'] == '-1':
                                pass
                            else:
                                sSTT_TraceFile = r"%s\loop%s\%s" % (sSTT_TracePath, str(
                                    loop), dSTT_Trace_File[test_case_pool_dict[tc]['Script']])
                                cmdSTT = r'%s %s %s %s' % (
                                    sSTT_ExePath, sSTT_USBPort1, sSTT_TraceFile, sSTT_FileSize)
                                print 'cmdSTT :%s' % cmdSTT
                                print 'sSTT_TraceFile :%s' % sSTT_TraceFile

                                try:
                                    subprocess.check_output(
                                        ['taskkill.exe', '/f', '/im', 'stt.exe', '/t'])
                                    subprocess.check_output(
                                        ['taskkill.exe', '/f', '/im', 'oneclick_stt.exe', '/t'])
                                    pass
                                except Exception as e:
                                    pass
                                else:
                                    pass

                                # NOTE procedure 2.2 llaw, execute
                                # oneclick_stt.exe/stt.exe
                                pSTT = Popen(cmdSTT, shell=False)
                        
                        # NOTE run the testsript
                        p = Popen(command % (cfg_file_with_path, r"%s\loop%s" % (
                            log_path, str(loop)), sPathRunScript), shell=False)
                        # cmdAutoTest = command % (cfg_file_with_path,r"%s\loop%s" % (log_path, str(loop)), test_case_pool_dict[tc]['Script'])
                        # p = Popen((cmdAutoTest, sPathRunScript), shell=False)

                        # time_monitor = test_case_pool_dict[tc]['EstimatedTime']
                        time_monitor = 0
                        if time_monitor in [0, '', None, 'None', '0']:
                            time_monitor = 60

                        #t = threading.Timer(int(time_monitor) * 60.0 * int(loop), kill_SubProcess, args=(p,))
                        sleep(10)
                        autotest_pids = get_pids()
                        #t = threading.Timer(20.0, kill_SubProcess, args=(p,autotest_pids,))

                        # NOTE: created for handling AVMS long duration case
                        # TODO: remove 600 timeout hardcode
                        if '__TIMEOUT' in os.environ:
                            iTimeOut = int(os.environ['__TIMEOUT'])
                        else:
                            iTimeOut = min(int(time_monitor) *
                                           60.0 * int(loop), 600)

                        t = threading.Timer(
                            iTimeOut, kill_SubProcess, args=(p, autotest_pids,))
                        t.start()
                        print "\n%s : A %s second timer is started to monitor the script run" % (datetime.now().strftime("%y/%m/%d %H:%M:%S"), iTimeOut)
                        p.wait()
                        try:
                            if t.isAlive():
                                print "\nTerminate the monitoring process\n"
                                t.cancel()
                                print "%s : Timer is cancelled\n" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            else:
                                print "\nMonitoring process expired, script is killed !!!\n"
                        except Exception, e:
                            print e
                            traceback.print_exc()
                            print "\n---->Problem when terminating mornitor process !!!\n"

                        sleep(3)
                        end_temp = time()
                        duration_for_qc_temp[tc][loop] = int(
                            (end_temp - start_time) * 2 / 60)
                    else:
                        print "%s already run, skip it." % test_case_pool_dict[tc]['Script']
                        print "There are more than one test case in this script."

                        # NOTE Check for run type -> offical run ?
                        # 1-Click-Checking ?
                    # if "done" in os.environ['QC_Filter'] or "Done" in os.environ['QC_Filter']:
                        # print "\nThis is an official run for test campaign, now we check : This Run VS Last Run"
                        # p = re.compile("Status\s+%s\s*:\s*(\S+)" % tc)
                        # temp_result = ''
                        # with open(r"%s\loop%s\%s" % (log_path, str(loop), test_case_pool_dict[tc]['Script'].split('/')[-1].replace(".py", ".log").replace(".PY", ".log"))) as f:
                            # for line in f.readlines():
                                # k = p.search(line)
                                # if k is not None:
                                    # temp_result = k.group(1)

                        # temp_ver = get_version_from_log(r"%s\loop%s\%s" % (log_path, str(
                            # loop), test_case_pool_dict[tc]['Script'].split('/')[-1].replace(".py", ".log")))
                        # if versions[tc] == '' or versions[tc] == 'Unkown Version':
                            # versions[tc] = temp_ver
                            # memo_ver = temp_ver

                        # print "\nThis script run under firmware version : %s" % temp_ver
                        # print "%s This Run: %s VS Last Run: %s\n" % (tc, temp_result, test_case_pool_dict[tc]['LastStatus'])

                        # if temp_result == str(test_case_pool_dict[tc]['LastStatus']).upper():
                            # break
                        # elif temp_result in ['PASSED', 'Passed']:
                            # break
                        # # elif test_case_pool_dict[tc]['LastStatus'] == "No
                        # # Run":
                        # else:
                            # print "This Run != Last Run, we decide to re-run this script."
                            # print "Does not rerun"
                            # break
                            # no_run_to_re_run += 1
                            # if no_run_to_re_run == 3:
                                # print "Already run three times, no need to re-run now.\n"
                                # break

                    # elif "hecking" in os.environ['QC_Filter']:
                        # #p = re.compile("Status\s+\S+_\d{4}\s*:\s*(\S+)")
                        # p = re.compile("Status\s+%s\s*:\s*(\S+)" % tc)
                        # temp_result = ''
                        # # print r"%s\loop%s\%s" % (log_path,
                        # # str(loop),test_case_pool_dict[tc]['Script'].split('/')[-1].replace(".py",".log"))
                        # with open(r"%s\loop%s\%s" % (log_path, str(loop), test_case_pool_dict[tc]['Script'].split('/')[-1].replace(".py", ".log").replace(".PY", ".log"))) as f:
                            # for line in f.readlines():
                                # k = p.search(line)
                                # if k is not None:
                                    # temp_result = k.group(1)

                        # print "\n%s : %s\n" % (tc, temp_result)

                        # temp_ver = get_version_from_log(r"%s\loop%s\%s" % (log_path, str(loop), test_case_pool_dict[
                                                        # tc]['Script'].split('/')[-1].replace(".py", ".log").replace(".PY", ".log")))
                        # if versions[tc] == '' or versions[tc] == 'Unkown Version':
                            # versions[tc] = temp_ver
                            # memo_ver = temp_ver
                        # continue

                except Exception, e:
                    print e
                    traceback.print_exc()
                    print "---->Problem: except comes up when running %s" % test_case_pool_dict[tc]['Script']
                finally:
                    try:
                        print 'try killing process for test end.'
                        subprocess.check_output(['tasklist.exe'])
                        subprocess.check_output(
                            ['taskkill.exe', '/f', '/im', 'autotest.py', '/t'])
                        subprocess.check_output(
                            ['taskkill.exe', '/f', '/im', 'stt.exe', '/t'])
                        subprocess.check_output(
                            ['taskkill.exe', '/f', '/im', 'oneclick_stt.exe', '/t'])
                        pass
                    except Exception as e:
                        # NOTE handle if no stt.exe found
                        # handle if no autotest.py found
                        pass
                    else:
                        pass
                    pass

            timer[tc] = calculate_how_long(start_time, time())

            if test_case_pool_dict[tc]['Script'] not in duration_by_script.keys():
                duration_by_script[test_case_pool_dict[tc]['Script']] = max(duration_for_qc_temp[tc][1], duration_for_qc_temp[
                                                                            tc][2], duration_for_qc_temp[tc][3], duration_for_qc_temp[tc][4], duration_for_qc_temp[tc][5])

            #duration_for_qc[tc] = max(duration_for_qc_temp[tc][1],duration_for_qc_temp[tc][2],duration_for_qc_temp[tc][3],duration_for_qc_temp[tc][4],duration_for_qc_temp[tc][5])
            duration_for_qc[tc] = duration_by_script[
                test_case_pool_dict[tc]['Script']]
            if duration_for_qc[tc] < 30:
                duration_for_qc[tc] = 30
                print "- The minimum duration is 30 min -"

            print "Caculated duration: %s" % str(duration_for_qc[tc])

            script_already_run.append(test_case_pool_dict[tc]['Script'])

            total_test_number = total_test_number - 1

            # if os.environ['QC_1_Click_TestLab_Filter'] == "Run me":
                # update_TestLab_OneClick(os.environ['QC_Path_Test_Campaign'].split(
                    # ":")[0], os.environ['QC_Path_Test_Campaign'].split(":")[1], '"Run me"', tc)

    finally:
        pass

# def make_html_log():

    print "\n\n----------------------------------------------------------------"
    print "    Generate HTML report"
    print "----------------------------------------------------------------\n\n"

    try:

        # NOTE llaw: function this please ---
        lsSortedTCName = []
        lsExpandedByLastNum = []
        lsSortTCName = test_case_pool_dict.keys()
        for sSortTCName in lsSortTCName:
            sExpandedByLastNum = sSortTCName[-4::] + '@@' + sSortTCName
            lsExpandedByLastNum.append(sExpandedByLastNum)

        for sExpandedByLastNum in sorted(lsExpandedByLastNum):
            lsSortedTCName.append(sExpandedByLastNum.split('@@')[1])

        pprint.pprint(lsSortedTCName)
        # NOTE llaw: function this please ---

        d = {}
        # for tc in test_case_pool_dict.keys():
        for tc in lsSortedTCName:
            d[tc] = {'script': test_case_pool_dict[tc]['Script'].split('/')[-1],
                     'ref_result': 'Not Use',
                     'job_name': os.environ['JOB_NAME'],
                     'build_number': os.environ['BUILD_NUMBER'],
                     'result': {'loop1': {'status': '', 'link': ''},
                                'loop2': {'status': '', 'link': ''},
                                'loop3': {'status': '', 'link': ''},
                                'loop4': {'status': '', 'link': ''},
                                'loop5': {'status': '', 'link': ''}
                                },
                     'elapse_time': timer[tc],
                     # 'IssueID': test_case_pool_dict[tc]['IssueID'],
                     'IssueID': 'Not Use',
                     'FW version': versions[tc],
                     # 'Instance': test_case_pool_dict[tc]['Instance'],
                     'Instance': 'Not Use',
                     # 'ResponsibleTester': test_case_pool_dict[tc]['ResponsibleTester'],
                     'ResponsibleTester': 'vhoang',
                     # 'Feature_Owner': test_case_pool_dict[tc]['Feature_Owner']
                     'Feature_Owner': 'vhoang'
                     }
        # for tc in test_case_pool_dict.keys():
        for loop in range(1, int(os.environ['Loop'])+1):
            log_file_list = []
            # print loop
            print log_file_list

            for root, dirs, files in os.walk(r"%s\loop%s" % (log_path, str(loop))):
                for each_log in files:
                    log_file_list.append(os.path.join(root, each_log))

            p = re.compile("A_\S*_\w{4}.log")
            # print len(log_file_list)
            xx = 1
            for each_log in log_file_list:
                print
                # print xx
                print "\nchecking for %s" % each_log
                xx = xx + 1
                if not (p.search(each_log) is not None):
                    os.remove(each_log)
                    sleep(1)
                    if os.path.isfile(each_log):
                        print "---->Warn: Fail to delete %s" % each_log
                    log_file_list.remove(each_log)
                    print "%s is deleted" % each_log

            #    NOTE ??
            sleep(3)

            for each_log in log_file_list:
                log2html_converter(each_log, r"%s\loop%s" %
                                   (log_path_html, str(loop)))

        print "\nHTML format log generation done\n"

        print "\n***Search Result for each Test Case***\n"

        for tc in test_case_pool_dict.keys():
            for loop in range(1, int(os.environ['Loop'])+1):
                log_file_list = []

                for root, dirs, files in os.walk(r"%s\loop%s" % (log_path, str(loop))):
                    for each_log in files:
                        log_file_list.append(os.path.join(root, each_log))
                # p = re.compile("Status\s*%s\s*:\s*(\S+)" % tc)
                p = re.compile("Status\s%s:\s(\S+)" %tc)
                print "\nSearch result for %s in loop %s" % (tc, str(loop))

                tc_not_found = True
                tc_log_not_found = True
                masterUrl = os.environ['BUILD_URL'].replace(os.environ['BUILD_NUMBER'] + '/','') + \
                    'ws/html/%s/loop%s/%s.html'
                for each_log in log_file_list:
                    if test_case_pool_dict[tc]['Script'].split('\\')[-1].replace('.py', '.log').replace(".PY", ".log").strip('"') in each_log:
                        tc_log_not_found = False
                        print "\n%s is being scanned..." % each_log
                        print "%s is opened\n" % each_log
                        with open(each_log) as f:
                            for line in f.readlines():
                                k = p.search(line)
                                if k is not None:
                                    tc_not_found = False
                                    test_case_pool_dict[tc]['result']['loop%s' % str(loop)][
                                        'status'] = k.group(1).capitalize()
                                    print "\n%s : %s\n" % (tc, k.group(1).capitalize())
                                    test_case_pool_dict[tc]['result']['loop%s' % str(loop)]['link'] = masterUrl % (
                                        os.environ['BUILD_NUMBER'], str(loop), test_case_pool_dict[tc]['Script'].split(".")[0].split('\\')[-1].strip('"'))
                                else:
                                    pass
                        if tc_not_found:
                            test_case_pool_dict[tc]['result']['loop%s' %
                                            str(loop)]['status'] = "NoTC"
                            test_case_pool_dict[tc]['result']['loop%s' % str(loop)]['link'] = masterUrl % (
                                os.environ['BUILD_NUMBER'], str(loop), test_case_pool_dict[tc]['Script'].split(".")[0])
        myLog2Html(report_path, test_case_pool_dict)
    except Exception, e:
        traceback.print_exc()
        print "\n---->Problem : Fail to generate HTML report !!!\n"

    # print d

    # print "\n\n------------------------------------------------------------------------------------------------------------------"
    # print "Copy Log Files to : %s" % r"\\cnhkg-nv-fl01\file\RD_Product_Enhancement\Common\Validation_APAC\Tests_HK\LOG\1click"
    # print "------------------------------------------------------------------------------------------------------------------\n\n"
    # try:
        # temp_ver = 'balalba'
        # for tc in d.keys():
            # temp_ver = d[tc]['FW version']
            # if temp_ver != '':
                # break
        # print temp_ver
        # # print os.environ['Log_File_Path_This_Run']

        # p = re.compile("(A_\S+\.log)")

        # temp_path = r"C:\Log1click"
        # #temp_path = os.environ['Log_File_Path_This_Run']
        # print "\n---->Comment: all log files will be copied to %s\n" % temp_path
        # for loop in range(1, 5 + 1):
            # log_file_list = []
            # for root, dirs, files in os.walk(r"%s\loop%s" % (log_path, str(loop))):
                # for each_log in files:
                    # log_file_list.append(os.path.join(root, each_log))
            # for each_log in log_file_list:
                # dest_path = "%s/%s/Build%s/Loop%s" % (
                    # temp_path, os.environ['JOB_NAME'], str(os.environ['BUILD_NUMBER']), str(loop))
                # if not os.path.exists(dest_path):
                    # pass
                    # #os.makedirs(dest_path)
                # print "Copy %s" % each_log
                # k = p.search(each_log)
                # if k is not None:
                    # #print "To   %s/%s" % (dest_path, k.group(1))
                    # #shutil.copyfile(each_log, "%s/%s" % (dest_path, k.group(1)))
                    # temp_path2 = r"C:\Log1click\test.log"
                    # shutil.copyfile(each_log, "%s" % (temp_path2))
                    # print "\n%s copy done\n" % temp_path2
                # else:
                    # print "---->Problem: No log file to copy !!!\n"

    # except Exception, e:
        # traceback.print_exc()
        # print "\n---->Proble: exception comes up when copying log file !!!\n"

    # print "\n\n----------------------------------------------------------------"
    # print "    This Part is for 1-Click Checing Only"
    # print "----------------------------------------------------------------\n\n"
    # try:
        # # print d
        # if "hecking" in os.environ['QC_Filter']:
            # for tc in d.keys():
                # import_Result_ToQC(os.environ['QC_Path_Test_Campaign'].split(
                    # ":")[0], os.environ['QC_Path_Test_Campaign'].split(":")[1], tc, d)
                # if d[tc]['result']['loop1']['status'] == d[tc]['result']['loop2']['status'] == d[tc]['result']['loop3']['status'] == d[tc]['result']['loop4']['status'] == d[tc]['result']['loop5']['status'] == 'Passed':
                    # update_TestLab_Field(os.environ['QC_Path_Test_Campaign'].split(":")[0], os.environ['QC_Path_Test_Campaign'].split(":")[
                                         # 1], 'Comment', tc, "1-Click: Done, Platform: %s, Build: %s" % (os.environ['JOB_NAME'], str(os.environ['BUILD_NUMBER'])))

                # else:
                    # update_TestLab_Field(os.environ['QC_Path_Test_Campaign'].split(":")[0], os.environ['QC_Path_Test_Campaign'].split(":")[
                                         # 1], 'Comment', tc, "1-Click: Need Check, Platform: %s, Build: %s" % (os.environ['JOB_NAME'], str(os.environ['BUILD_NUMBER'])))

    # except Exception, e:
        # traceback.print_exc()
        # print "\n---->Problem: exception comes up when doing 1-click checking !!!\n"

    # try:
        # if "hecking" in os.environ['QC_Filter']:
            # print "\nNow we are going to update the Expected Duration in Test Plan:"
            # from QC_Update_TestPlan import QcTestPlan
            # myQC = QcTestPlan('oneclick', 'sierra_211')
            # for tc in test_case_pool_dict.keys():
                # print "Update %s Expected Duration = %s min" % (tc, str(duration_for_qc[tc]))
                # myQC.updateField2(test_case_pool_dict[tc][
                                  # 'TestID'], 'TS_ESTIMATE_DEVTIME', '%s' % str(duration_for_qc[tc]))
    # except Exception, e:
        # traceback.print_exc()
        # print "\n---->Proble: exception comes up when update Expected Duration field in Test Plan !!!\n"

    # #    NOTE excel generate report start
    # print "\n\n----------------------------------------------------------------"
    # print "    Generate Excel report"
    # print "----------------------------------------------------------------\n\n"
    # try:
        # xlApp = Dispatch("Excel.Application")
        # xlApp.Visible = True
        # wb = xlApp.Workbooks.Add()
        # sh = wb.sheets["Sheet1"]

        # col_testName = 1
        # col_scriptName = 2
        # col_owner = 3
        # col_thisRun_1 = 4
        # col_thisRun_2 = 5
        # col_thisRun_3 = 6
        # col_thisRun_4 = 7
        # col_thisRun_5 = 8

        # sh.Cells(1, col_testName).Value = "Test Name"
        # sh.Cells(1, col_instance).Value = "Name"
        # sh.Cells(1, col_scriptName).Value = "Script Name"
        # sh.Cells(1, col_owner).Value = "Feature Owner"
        # sh.Cells(1, col_QcLastRun).Value = "Last Run"
        # sh.Cells(1, col_QcIssueId).Value = "Issue ID"
        # sh.Cells(1, col_Platform).Value = "PlatForm"
        # sh.Cells(1, col_FwVersion).Value = "FW version"
        # sh.Cells(1, col_ModuleType).Value = "ModuleType"
        # sh.Cells(1, col_ModulRef).Value = "ModuleRef"
        # sh.Cells(1, col_thisRun_1).Value = "Loop 1"
        # sh.Cells(1, col_thisRun_2).Value = "Loop 2"
        # sh.Cells(1, col_thisRun_3).Value = "Loop 3"
        # sh.Cells(1, col_thisRun_4).Value = "Loop 4"
        # sh.Cells(1, col_thisRun_5).Value = "Loop 5"
        # sh.Cells(1, col_build).Value = "Build Number"
        # sh.Cells(1, col_ResponsbileTester).Value = "Responsible Tester"
        # sh.Cells(1, col_ScriptRev).Value = "Script Revision"

        # row = 2

        # link = r"%s/ws/html/%s/%s.html"

        # module_type = os.environ['Module_Type']
        # module_ref = os.environ['Module_Ref']
        # sim = os.environ['SIM_INI'].split('\\')[-1].split('.')[0]
        # if 'AUX_SIM_INI' in os.environ:
            # sim += ', '
            # sim += os.environ['AUX_SIM_INI'].split('\\')[-1].split('.')[0]
        # if 'AUX2_SIM_INI' in os.environ:
            # sim += ', '
            # sim += os.environ['AUX2_SIM_INI'].split('\\')[-1].split('.')[0]

        # for tc in d.keys():
            # sh.Cells(row, col_testName).Value = tc
            # sh.Cells(row, col_instance).Value = d[tc]['Instance']
            # sh.Cells(row, col_scriptName).Value = d[tc]['script']
            # if "hecking" in os.environ['QC_Filter']:
                # sh.Cells(row, col_owner).Value = d[tc]['Feature_Owner']
            # else:
                # sh.Cells(row, col_owner).Value = "Not Used"
            # sh.Cells(row, col_QcLastRun).Value = d[tc]['ref_result']
            # sh.Cells(row, col_QcIssueId).Value = d[tc]['IssueID']
            # sh.Cells(row, col_Platform).Value = os.environ['JOB_NAME']
            # sh.Cells(row, col_FwVersion).Value = d[tc]['FW version']
            # sh.Cells(row, col_ModuleType).Value = module_type
            # sh.Cells(row, col_ModulRef).Value = module_ref
            # sh.Cells(row, col_SIM).Value = sim

            # sh.Cells(row, col_thisRun_1).Value = d[
                # tc]['result']['loop1']['status']
            # if d[tc]['result']['loop1']['link'] != '':
                # sh.Hyperlinks.Add(Anchor=sh.Range(sh.Cells(row, col_thisRun_1).Address),
                                  # Address=d[tc]['result']['loop1']['link'])

            # sh.Cells(row, col_thisRun_2).Value = d[
                # tc]['result']['loop2']['status']
            # if d[tc]['result']['loop2']['link'] != '':
                # sh.Hyperlinks.Add(Anchor=sh.Range(sh.Cells(row, col_thisRun_2).Address),
                                  # Address=d[tc]['result']['loop2']['link'])

            # sh.Cells(row, col_thisRun_3).Value = d[
                # tc]['result']['loop3']['status']
            # if d[tc]['result']['loop3']['link'] != '':
                # sh.Hyperlinks.Add(Anchor=sh.Range(sh.Cells(row, col_thisRun_3).Address),
                                  # Address=d[tc]['result']['loop3']['link'])

            # sh.Cells(row, col_thisRun_4).Value = d[
                # tc]['result']['loop4']['status']
            # if d[tc]['result']['loop4']['link'] != '':
                # sh.Hyperlinks.Add(Anchor=sh.Range(sh.Cells(row, col_thisRun_4).Address),
                                  # Address=d[tc]['result']['loop4']['link'])

            # sh.Cells(row, col_thisRun_5).Value = d[
                # tc]['result']['loop5']['status']
            # if d[tc]['result']['loop5']['link'] != '':
                # sh.Hyperlinks.Add(Anchor=sh.Range(sh.Cells(row, col_thisRun_5).Address),
                                  # Address=d[tc]['result']['loop5']['link'])

            # sh.Cells(row, col_build).Value = os.environ['BUILD_NUMBER']
            # sh.Cells(row, col_ResponsbileTester).Value = d[
                # tc]['ResponsibleTester']
            # #sh.Cells(row, col_ScriptRev).Value = getScriptRev(d[tc]['script'])
            # sh.Cells(row, col_ScriptRev).Value = "1111"

            # row += 1
        # print 'Report file'+report_path
        # #wb.SaveAs(r"%s\Report_%s_Build_%s.xlsx" % (
            # #report_path, os.environ['JOB_NAME'], os.environ['BUILD_NUMBER']))
        # print debug_environ['JOB_NAME']
        # print debug_environ['BUILD_NUMBER']
        
        
       
     
     
        # wb.SaveAs(r"%s\Report_%s_Build_%s.xlsx" % (report_path, debug_environ['JOB_NAME'], debug_environ['BUILD_NUMBER']))
        
        # wb.Close()
        # # xlApp.Close()
        # if xlApp.Workbooks.Count == 0:
            # xlApp.Quit()
        # del xlApp
    # except Exception, e:
        # traceback.print_exc()
        # print "\n---->Problem: Fail to generate excel report !!!\n"

       # #NOTE excel generate report end

    try:
        temp_firmware_name = os.environ[
            'Firmware_Under_Tested'].split("\\")[-1]
        print "\nDelete the temp firmware %s" % temp_firmware_name
        os.remove(r"C:\%s" % temp_firmware_name)
    except Exception, e:
        print e
        traceback.print_exc()
        print "---->Problem: fail to delete FW\n"

    if "Done" in os.environ['QC_Filter']:
        memo_purpose = "Official "
    else:
        memo_purpose = "1-Click-Checking"

    print "\n\n*********************************************************************************************************************"
    print "                           One Click Test System End"
    print "\n"
    # print "[Memo] %s for %s, %s TC in Campaign [%s] are executed" % (memo_ver, memo_purpose, str(memo_number_tc), os.environ['QC_Path_Test_Campaign'].split(":")[1])
    print "\n"
    print "                               %s" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
    print "\n*********************************************************************************************************************\n\n"

    return True


##########################################################################


def main():

    # input
    # process
    # output

    Load()

    # 1. Test Enviroment Creation
    check_enviroment()
    update_cfg()

    # NOTE 1-click checking = QC_Path_Test_Campaign or QC_Filter
    # QC_Path_Test_Campaign => 1-click checking Campaign
    # QC_Filter => 1-Click-Checking

    # NOTE checking campaign -> checking / Done in filter
    # NOTE Formal campaign -> cannot exist checking in filter.

    # if "hecking" not in debug_environ['QC_Path_Test_Campaign'] and "hecking" in debug_environ['QC_Filter']:
        # print "----->Error: wrong parameter !!!!!"
        # print "Test Campaign %s is offical, but 1-click filter %s is for 1-click checking" % (debug_environ['QC_Path_Test_Campaign'], debug_environ['QC_Filter'])
        # print "[Memo] Bad building"
        # sys.exit()

    # NOTE llaw, print for selecting non-stress testcase
    # if 'QC_test_category' in os.environ:
        # pass
    # else:
        # os.environ['QC_test_category'] = 'Not Use'
    # print "info: QC_test_category:%s" % os.environ['QC_test_category']

    # # NOTE llaw, print for selecting non-stress testcase
    # if 'QC_test_Execution_Status' in os.environ:
        # pass
    # else:
        # os.environ['QC_test_Execution_Status'] = 'Not Use'
    # print "info: QC_test_Execution_Status:%s" % os.environ['QC_test_Execution_Status']

    # test_case_pool_dict = get_TestNumber_From_QC(
        # os.environ['QC_Path_Test_Campaign'] .split(":")[0],
        # os.environ['QC_Path_Test_Campaign'] .split(":")[1],
        # os.environ['QC_Filter'],
        # os.environ['QC_1_Click_TestLab_Filter'],
        # os.environ['QC_status_filter'],
        # os.environ['QC_tester_filter'],
        # os.environ['Test_Cases'],
        # os.environ['QC_Carrier_Filter'],
        # os.environ['QC_TestPlan_Conditions_filter'],
        # os.environ['QC_TestPlan_Feature_filter'],
        # os.environ['QC_test_category'],
        # os.environ['QC_test_Execution_Status']
    # )
    
    
    
    
    #### vhoang ####################################################################################
    Test_Cases = os.environ['Test_Cases']
    test_case_pool_dict = {}
    if ' or ' in Test_Cases or ' OR ' in Test_Cases:
        if ' or ' in Test_Cases:
            test_case_list = Test_Cases.split(' or ')
        if ' OR ' in Test_Cases:
            test_case_list = Test_Cases.split(' OR ')
        test_case_pool_dict['%s' %test_case_list[0]] = {'Script':'%s.py' %test_case_list[0], 'result':{'loop1':{'status': '','link':''},'loop2':{'status': '','link':''},'loop3':{'status': '','link':''},'loop4':{'status': '','link':''},'loop5':{'status': '','link':''}}}
        test_case_list = iter(test_case_list)
        next(test_case_list)
        for test_case in test_case_list: 
            test_case_pool_dict['%s' %test_case] = {'Script':'%s.py' %test_case, 'result':{'loop1':{'status': '','link':''},'loop2':{'status': '','link':''},'loop3':{'status': '','link':''},'loop4':{'status': '','link':''},'loop5':{'status': '','link':''}}}
    elif' or ' not in Test_Cases or ' OR ' not in Test_Cases:
        test_case_list = Test_Cases
        test_case_pool_dict = {'%s' %test_case_list: {'Script':'%s.py' %test_case_list, 'result':{'loop1':{'status': '','link':''},'loop2':{'status': '','link':''},'loop3':{'status': '','link':''},'loop4':{'status': '','link':''},'loop5':{'status': '','link':''}}}}
    else:
        print '\nTest_Cases is not correct!!!\n'
                                
    ################################################################################################
    
    
    

    # print "debug: test_case_pool_dict"
    # pprint.pprint(test_case_pool_dict)

    # NOTE execute testscript
    run(test_case_pool_dict)

    # NOTE Process log
    # make_html_log()

    # NOTE archive log


if __name__ == u'__main__':

    debug_environ = os.environ
    # NOTE configuration
    qcServer = r"http://10.40.11.70:8080/qcbin/"
    qcUser = "oneclick"
    qcPassword = "sierra_211"
    qcDomain = "DEFAULT"
    qcProject = "Validation"
    # qc_path = os.environ['QC_Path_Test_Campaign'].split(":")[0]
    # qc_campaign = os.environ['QC_Path_Test_Campaign'].split(":")[1]

    log_path = r".\log\%s" %debug_environ['BUILD_NUMBER']
    log_path_html = r".\html\%s" %debug_environ['BUILD_NUMBER']
    cfg_path = r".\configuration_file"
    report_path = r".\report\%s" %debug_environ['BUILD_NUMBER']
    cfg_file_with_path = cfg_path + "\%s.cfg" %debug_environ['JOB_NAME']
    autotest_plus_path = r".\oneclick\autotest.py"

    if 'STT_USBPORT1' in debug_environ.keys():
        if debug_environ['STT_USBPORT1'] == '-1':
            pass
        else:
            # NOTE configuration for STT
            print 'STT environment:'
            sSTT_BasePath = r'%s\oneclick\tools\HL_tools\stt_exe_20151211b' % (debug_environ[
                                                                               'WORKSPACE'])
            sSTT_ExePath = r'%s\oneclick_stt.exe' % sSTT_BasePath
            sSTT_TracePath = r"%s\_trace\%s" % (
                debug_environ['WORKSPACE'], debug_environ['BUILD_NUMBER'])

            sSTT_USBPort1 = 'COM%s' % debug_environ['STT_USBPORT1']

            sSTT_FileSize = ''
            if 'STT_FILESIZE' in debug_environ.keys():
                sSTT_FileSize = debug_environ['STT_FILESIZE']

            # NOTE finialize STT configuration
            print 'sSTT_BasePath  :%s ' % sSTT_BasePath
            print 'sSTT_ExePath   :%s ' % sSTT_ExePath
            print 'sSTT_TracePath :%s ' % sSTT_TracePath
            print 'sSTT_USBPort1  :%s ' % sSTT_USBPort1
            print 'sSTT_FileSize  :%s ' % sSTT_FileSize

    # NOTE bypass for debug, 1=>enable, 0=>disable
    bEnableDownloadFirmware = 1
    
    command = r'python "%s/oneclick/autotest.py"' % debug_environ[
        'WORKSPACE'] + " -cfg %s -log -logpath %s %s"
    script = r"C:\AutoTestLibrary\sample\at.py"

    main()
