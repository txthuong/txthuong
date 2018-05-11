
def myLog2Html(dest,d):
    color = lambda x : "green" if ( x == "Passed" ) else ("red" if (x=="Failed") else "black")
    fp = open(r"%s\summary.html" % dest, "w")

    fp.write('\n')
    fp.write(r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
    fp.write('\n')
    fp.write('<html xmlns="http://www.w3.org/1999/xhtml">')
    fp.write('\n')
    fp.write(r'<head>')
    fp.write('\n')
    fp.write(r'<style>BODY{background-color:peachpuff;}TABLE{border-width: 1px;border-style: solid;border-color: black;border-collapse: collapse;}TH{border-width: 1px;padding: 0px;border-style: solid;border-color: black;background-color:thistle}TD{border-width: 1px;padding: 0px;border-style: solid;border-color: black;background-color:PaleGoldenrod}</style>')
    fp.write('\n')
    fp.write(r'</head><body>')
    fp.write('\n')
    fp.write(r'<H2>One Click Test Result Summary<br>---------------------------------------------------------------------<br>Note: Test: 1-Click, Owner and Test: Estimated Duration are not used yet<br>Note: Elapsed time are total all loops<br></H2>')
    fp.write('\n')
    fp.write(r'<table>')
    fp.write('\n')
    fp.write(r'<colgroup>')
    fp.write('\n')
    for i in range(0,9):
        fp.write(r'<col/>')
        fp.write('\n')
    fp.write(r'</colgroup>')
    fp.write('\n')
    #fp.write(r'<tr><th>Test: Test Name</th><th>Test: Script Name</th><th>Test: 1-Click</th><th>Owner</th><th>Test: Estimated Duration</th><th>Status</th><th>Comment</th><th>loop1</th><th>test_time_loop_1</th></tr>')
    
    fp.write(r'<tr><th>Test: Test Name</th><th>Test: Script Name</th><th>Test: 1-Click</th><th>Owner</th><th>Test: Estimated Duration</th><th>Status in QC</th><th>Issue ID</th><th>loop1</th><th>loop2</th><th>loop3</th><th>loop4</th><th>loop5</th><th>Elapsed Time</th></tr>')

    
    fp.write('\n')
    #fp.write(r'<tr><td>A_INTEL_LTE_AVMS_UPD_0002</td><td>A_INTEL_LTE_AVMS_UPD_0002.py</td><td>Intel_LTE_PF_AVMS.21</td><td>rtn</td><td>10</td><td><font color="green">Passed</font></td><td></td><td><a href="http://cnhkg-ev-hudson:8080/job/RTN-STUDY/72/artifact/html/72/A_INTEL_LTE_GEN_ATI_0001.html"><font color="green">Passed</font></a></td><td>00:03:39.1159094</td></tr>')
    for tc in d.keys():
        fp.write(r'<tr><td>%s</td><td>%s</td><td>NA</td><td>%s</td><td>NA</td><td><font color="%s">%s</font></td><td></td><td><a href="%s" target="_blank"><font color="%s">%s</font></a></td><td><a href="%s"><font color="%s">%s</font></a></td><td><a href="%s"><font color="%s">%s</font></a></td><td><a href="%s"><font color="%s">%s</font></a></td><td><a href="%s"><font color="%s">%s</font></a></td><td>%s</td></tr>' %
                 (tc,
                  d[tc]['Script'],
                  'vhoang',
                  'Not Use',
                  'Not Use',
                  d[tc]['result']['loop1']['link'],
                  color(d[tc]['result']['loop1']['status']),
                  d[tc]['result']['loop1']['status'],
                  d[tc]['result']['loop2']['link'],
                  color(d[tc]['result']['loop2']['status']),
                  d[tc]['result']['loop2']['status'],
                  d[tc]['result']['loop3']['link'],
                  color(d[tc]['result']['loop3']['status']),
                  d[tc]['result']['loop3']['status'],
                  d[tc]['result']['loop4']['link'],
                  color(d[tc]['result']['loop4']['status']),
                  d[tc]['result']['loop4']['status'],
                  d[tc]['result']['loop5']['link'],
                  color(d[tc]['result']['loop5']['status']),
                  d[tc]['result']['loop5']['status'],
                  'Not Use'
                  ))
    fp.write('\n')
    fp.write(r'</table>')
    fp.write('\n')
    fp.write(r'</body></html>')
    fp.write('\n')


    fp.close()


