# 
# 2012-09-05 Marco      File Creation
# 2012-09-24 Marco      Support CLI
# 2013-03-25 Marco      Read file in Binary
# 2013-11-16 Kmwong     In page CSS
# 2013-11-16 Kmwong     Add else statement for particular log file by CLI
# 2013-11-17 Kmwong     Re-write whole script
#
#
#   Purpose:
#   1. Summarize the result by searching keywords "Status * (Passed | Failed)"
#   2. Highlight Line by keywords "Passed" or "Failed"
#   3. Support CLI and Double click .py directly in Windows
#   4. Support for converting a single file or a batch of files
#
#   Usage:   
#   Input parameter: -i     input path/directory ( default = ./ ) or input file 
#                    -o     ouput path/directory ( default = ./output )
#
#   Example:
#   1. log2html.py -i simple.log
#   2. log2html.py -i C:\log2html\simple.log
#   3. log2html.py -i C:\log2html\
#   4. log2html.py -i simple.log -o logfolder
#   5. log2html.py -i simple.log -o c:\logfolder
#
import sys,os
import re
import subprocess
import time
import ConfigParser
import shutil
from optparse import OptionParser
from string import Template
import stat

#-----------------------------------------------------------------------
#Handle command-line options
def createParser():

    parser = OptionParser()    

    parser.add_option("-i","--input_path", dest="input_path",
                      help="import log file path", type="string")

    parser.add_option("-o","--output_path", dest="output_path",
                      help="path of output html path", type="string")

    return parser


#-----------------------------------------------------------------------
#Log to html converter function
#folder_summary = []
def log2html_converter(file_fullpath, dest_path):

    # Summary report for folder
    tc_result_summary=[]
    #global folder_summary
    folder_summary = []
    #-----------------------------------------------------------------------------------------------------------
    # Path and filename checking

    filefullname = os.path.basename(file_fullpath)          # fullpath
    filepath =  os.path.dirname(file_fullpath)              # path
    filename = os.path.splitext(filefullname)[0]            # filename
    file_extension = os.path.splitext(filefullname)[1]      # extension

    if filefullname is not None:
        src_extension = filefullname.split(".")[-1]
    else:
        return

    if file_extension.lower() == '.log':
        print file_fullpath + " ----- > .html"
    elif file_extension.lower() == '.txt':
        print file_fullpath + " ----- > .html"
    else:
        print file_fullpath + " ----- It is not a .log or .txt file"
        return

    #-----------------------------------------------------------------------------------------------------------
    #2: Read log file contents

    f_src = open(file_fullpath, 'rb')

    aString = f_src.read()

    #print type(aString)
    #print aString

    #Regulate all line change charaters to a unique expression '\n'
    aString = aString.replace('\r\n', '\n')
    aString = aString.replace('\r', '\n')

    #Regulate the special charater in html format, such as "<" and ">"
    aString = aString.replace("<", "&lt;")
    aString = aString.replace(">", "&gt;")
    
    #break it to lines, and store each line into array
    aString_lines = aString.split('\n')
    log_summary = []

    #print aString_lines
    #print aString_lines.__len__()


    #-----------------------------------------------------------------------------------------------------------
    #Start searching the content and highline those special charaters

    for (i,each_line) in enumerate(aString_lines) :
        #print i 
        #print each_line

        # Status *: (passed | failed) , case-insensitive
        status_tc_pattern = re.compile('status[A-Z0-9 ._%+-:]+(passed|failed)', re.I)              
        status_tc_match = status_tc_pattern.search(each_line)
        if status_tc_match is not None :
            tc_name = each_line.split(" ")[1].strip(":").strip("\t")
            tc_status = each_line.split(" ")[-1].strip(":").strip("\t")
            # highlight line
            aString_lines[i] = "<a name=\"" + tc_name + "\"></a>" + "<span class=\"" + tc_status + "\">" + each_line +"</span>"
            # log summary result
            log_summary.append("<a href=\"#" + tc_name + "\">" + "Line " + str(i+1) + ": " + each_line + "</a>")
            # folder summary result
            tc_result_summary.append((tc_name,tc_status, str(i+1),each_line))

        # Snd COM , case-sensitive
        snd_pattern = re.compile("Snd COM")
        snd_match = snd_pattern.search(each_line)
        if snd_match is not None :
            square_content = each_line[each_line.find("[")+1:each_line.rfind("]")]
            highlighted_line = each_line.replace(square_content, "<span class=\"sndcom\">"+square_content+"</span>")
            aString_lines[i] = highlighted_line


        # Rcv COM , case-sensitive
        rcv_pattern = re.compile("Rcv COM")
        rcv_match = rcv_pattern.search(each_line)
        if rcv_match is not None :
            square_content = each_line[each_line.find("[")+1:each_line.rfind("]")]
            highlighted_line = each_line.replace(square_content, "<span class=\"rcvcom\">"+square_content+"</span>")
            aString_lines[i] = highlighted_line


        # (NO MATCH|NO RESPONSE|ERROR|PROBLEM)
        problem_pattern = re.compile("(NO MATCH|NO RESPONSE|ERROR|PROBLEM)")
        problem_match = problem_pattern.search(each_line)
        if problem_match is not None :
            each_line = "<span class=\"nomatch\">" + each_line + "</span>"
        


    #-----------------------------------------------------------------------------------------------------------
    #3: Output to a html file

    whole_log_file = ""

    # html header
    html_header = """
    <html>
    <head>
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
    <title>html log sample</title>
    <!-- <link rel=\"stylesheet\" href=\"log.css\" type=\"text/css\" media=\"screen\" /> -->
      <style type="text/css">
        /*------------------------------=BASIC SETUP------------------------------*//* Makeshift CSS Reset */
        * {	margin: 0;	padding: 0;}
        /* Tell the browser to render HTML 5 elements as block */
        header, footer, section, aside, nav, article {	display: block;}
        body {	margin: 0 auto;	padding: 22px 0;	width: 95%;	font: 13px/22px Helvetica, Arial, sans-serif;	background: #F3F3F3;	overflow: scroll;}
        /*------------------------------=Table------------------------------*/
        table {	font: 13px/22px Helvetica, Arial, sans-serif;}
        .reporthead {	background: rgb(213, 255, 223);	font: 13px/22px Helvetica, Arial, sans-serif;}
        .reporttext {	text-decoration: none;}
        .passed {	color:green;	font-weight:bold;	font-size: 28px;}
        .failed {	color:red;	font-weight:bold;	font-size: 28px;}
        .failed_status {	color:red;	font-weight:bold;}
        .sndcom {	color:blue;	font-weight:bold;}
        .rcvcom {	color:red;	font-weight:bold;}
        .nomatch {	color:red;	font-weight:bold;}
        a:link {	text-decoration: none;}
        a:visited {	text-decoration: none;}
        a:hover {	text-decoration: underline;}
        a:active {	text-decoration: none;}
        /*------------------------------	background: #F3F3F3;------------------------------*/
      </style>
    </head>
    <body>
    """

    whole_log_file += html_header


    # summary table
    html_result_link = ""
    html_result_link += "<div class=\"reporthead\">"+"Search \"status * passed | failed\" (" + str(len(log_summary)) + " hits in 1 files)" + "</div>"
    for log_result in log_summary :
        html_result_link += "" + "<div class=\"reportext\">" + log_result + "</div>"

    whole_log_file += html_result_link
    whole_log_file += "<br>"

    # log content
    # whole_log_file += "<div class=\"reporttext\">"
    # for each_line in aString_lines :
        # whole_log_file += "<br>" + each_line + "\n"
    # whole_log_file += "</div>"


    whole_log_file += "<br>"
    #whole_log_file += "<br>" + file_fullpath
    #whole_log_file += "<br>" + os.getcwd() 
    #whole_log_file += "<br>" + dest_path
    #whole_log_file += "<br>" + os.path.relpath(file_fullpath)
    whole_log_file += "<div class=\"reporthead\"><a href=./" + filefullname + " >./" + filefullname + "</a></div>"

    # log content
    whole_log_file += "<div class=\"reporttext\">"
    whole_log_file += "<table>"

    for (i,each_line) in enumerate(aString_lines) :
        whole_log_file += "<tr>"
        whole_log_file += "<td width=60>"
        whole_log_file += "L" + str(i+1) + ":  "
        whole_log_file += "</td>"
        whole_log_file += "<td>"
        whole_log_file += each_line + "\n"
        whole_log_file += "</td>"
        whole_log_file += "</tr>"
    whole_log_file += "</table>"
    whole_log_file += "</div>"

    # html_footer
    whole_log_file += "</body></html>"

    # Save to a file
    dest_path = dest_path + '//'
    output_filename=filefullname.replace(file_extension, ".html")
    f_dst = open(dest_path + output_filename, 'w')
    f_dst.write(whole_log_file)
    f_dst.close()


    folder_summary.append((filefullname, filepath, len(tc_result_summary)))
    for (i,each_line) in enumerate(tc_result_summary) :

        folder_summary.append(each_line)
        #print i, each_line[0], each_line[1], each_line[2]

    #variable = raw_input('Press any key to continue..')



def print_folder_summary():
    pass



#-----------------------------------------------------------------------
#Main function

if __name__=='__main__':

    parser = createParser()
    (options, args) = parser.parse_args()

    # input path
    if options.input_path is None:
        file_fullpath = os.getcwd() + "\\"          # default by empty input
    elif os.path.exists(options.input_path):
        file_fullpath = os.path.abspath(options.input_path)     # testing file / file with path / path 
    else:
        print os.path.abspath(options.input_path) + " ----- Not found"
        file_fullpath = ""
  
    # output path
    if options.output_path is None:
        output_path = os.getcwd() + "\\" + "output" + "\\"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = options.output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    #print options.input_path
    #print options.output_path
    #print ""
    #print file_fullpath
    #print output_path



    # start convertion

    #print os.path.basename(file_fullpath)
    #print os.path.dirname(file_fullpath)
    #print os.path.abspath(file_fullpath)


    # for single file
    #print os.path.isfile(file_fullpath)
    if os.path.isfile(file_fullpath):
        log2html_converter(file_fullpath, output_path)  

    # for directory
    #print os.path.isdir(file_fullpath)
    if os.path.isdir(file_fullpath):
        dirList = os.listdir(file_fullpath)

        # filter *.*
        filelist = []
        for (i,fname) in enumerate(dirList):
            if os.path.isfile(os.path.abspath(fname)):
                filelist.append(os.path.abspath(fname))

        # filter *.log or *.txt, case-insensitive
        loglist = []
        for (i,fname) in enumerate(filelist):
            file_ext = os.path.splitext(os.path.basename(fname))[1].lower()
            if file_ext==".log" or file_ext==".txt":
                loglist.append(os.path.abspath(fname))
        

        global folder_summary
        folder_summary = []

        for eachfile in loglist:
            # copy source file to output directory , archive, relative path for .html
            shutil.copyfile(eachfile, output_path+os.path.basename(eachfile))
            # start conversion
            log2html_converter(eachfile, output_path)  



    #print folder_summary
    summary_log_file = ""

    # html header
    html_header = """
    <html>
    <head>
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
    <title>html log sample</title>
    <!-- <link rel=\"stylesheet\" href=\"log.css\" type=\"text/css\" media=\"screen\" /> -->
      <style type="text/css">
        /*------------------------------=BASIC SETUP------------------------------*//* Makeshift CSS Reset */
        * {	margin: 0;	padding: 0;}
        /* Tell the browser to render HTML 5 elements as block */
        header, footer, section, aside, nav, article {	display: block;}
        body {	margin: 0 auto;	padding: 22px 0;	width: 95%;	font: 13px/22px Helvetica, Arial, sans-serif;	background: #F3F3F3;	overflow: scroll;}
        /*------------------------------=Table------------------------------*/
        table {	font: 13px/22px Helvetica, Arial, sans-serif;}
        .reporthead {	background: rgb(213, 255, 223);	font: 13px/22px Helvetica, Arial, sans-serif;}
        .reporttext {	text-decoration: none;}
        .passed {	color:green;	font-weight:bold;	font-size: 28px;}
        .failed {	color:red;	font-weight:bold;	font-size: 28px;}
        .failed_status {	color:red;	font-weight:bold;}
        .sndcom {	color:blue;	font-weight:bold;}
        .rcvcom {	color:red;	font-weight:bold;}
        .nomatch {	color:red;	font-weight:bold;}
        a:link {	text-decoration: none;}
        a:visited {	text-decoration: none;}
        a:hover {	text-decoration: underline;}
        a:active {	text-decoration: none;}
        /*------------------------------	background: #F3F3F3;------------------------------*/
      </style>
    </head>
    <body>
    """
    summary_log_file += html_header

    # html_body

    for (i,each_line) in enumerate(folder_summary) :
        print i, each_line

        if each_line[0].lower().find(".log") != -1:
            LOG_NAME = each_line[0]
            KEYWORDS_HIT = str(each_line[2])
            summary_log_file += "<div class=\"reporthead\">"+ LOG_NAME + " Search \"status * passed | failed\" (" + KEYWORDS_HIT + " hits in 1 files)" + "</div>"
        else:
            SEARCH_RESULT = each_line[3]
            RESULT_LINE = each_line[2]
            RELATIVEPATH = ""
            HTML_NAME = os.path.splitext(LOG_NAME)[0] + ".html"
            TC_NAME = each_line[0]
            summaryline = "<a href=./" + HTML_NAME + "#" + TC_NAME + ">" +"Line " +  RESULT_LINE + ": " + SEARCH_RESULT + "</a>"
            summary_log_file += "" + "<div class=\"reportext\">" + summaryline + "</div>\n"

    # html_footer
    summary_log_file += "</body></html>"

    # Save to a file
    dest_path = output_path + '//'
    output_filename = "summary.htm"
    f_dst = open(dest_path + output_filename, 'w')
    f_dst.write(summary_log_file)
    f_dst.close()

    #for (i,each_line) in enumerate(folder_summary) :
        #print i, each_line
        #print_folder_summary

    print ""
    variable = raw_input('Press any key to exit..')
#-----------------------------------------------------------------------
