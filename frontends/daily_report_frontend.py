import datetime
import pdb

def render(doc):
    header  = """
<html>
<head>
</head>
"""
    footer = """
</div>
</body>
</html>
"""

    body = '<body style = "margin:0 ; padding:0">'
    body += '<div id="main" style = "width: 94%; padding: 3%">'
    body += """
    <h1 style="text-align:center; color:#666; margin-bottom:10px; font-size:25px; font-family:Arial, Helvetica"> <b style="color:#f26722; font-size:27px">go</b><strong style="color:#2d67b2; font-size:27px">ibibo</strong> Daily Dashboard </h1>
    <h1 style="text-align:center; color:#666; margin-bottom:5px; font-size:15px; font-family:Arial, Helvetica"> 
"""
    body += str(datetime.datetime.strptime(doc['date'],'%Y-%m-%d').strftime('%A, %d %B %Y'))
    body += '</h1>'
    body += createbody(doc)
    html = header+'\n'+body+'\n'+footer
    fileobj = open('/home/abhishek/dev/extra/dailyreport.html','w')
    fileobj.write(html)

def createchart(charttype,listoflists,xtitle,ytitle):
    script = """
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>
            <script type="text/javascript">
            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(drawChart);
            function drawChart() {
            var data = google.visualization.arrayToDataTable(
            """
    script += str(listoflists).replace("u'","")
    script += """    
            );
            var options = {
            """
    script += "title: '%s'," % (ytitle)
    script += "hAxis: {title: '%s', titleTextStyle: {color: 'red'}}" % (xtitle)
    script += "};"
    script += " var chart = new google.visualization.%s(document.getElementById('%s'));" % (charttype,xtitle+"_"+ytitle)
    script += """
            chart.draw(data, options);
            }
            </script>
            """
    return script,xtitle+"_"+ytitle

def createbody(doc):
    body = ""
    # generate category block
    for key,value in doc.iteritems():
        if key in ['visitors','tickets','GMV','gross margin','costs']:
            body += '<div id = "category" style = "border:2px solid #ccc;margin:10px; ">'
            body += '<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px; padding:5px">'
            if key in ["GMV"]:
                body += '<caption style="font:bold 16px Arial, Helvetica, sans-serif; padding:5px 0; border-bottom:1px solid #ccc;text-align:left;padding-left:15px;">%s : ' % (str(key))
            else:
                body += '<caption style="font:bold 16px Arial, Helvetica, sans-serif; padding:5px 0; border-bottom:1px solid #ccc;text-align:left;padding-left:15px;">%s : ' % (str(key).title())
            body += str(value['total'])
            body += "</caption>"

            # generate info block inside category block
            for k,v in value.iteritems():
                body += '<tr>'
                if k != 'total':
                    body +='<td width="38%" style="text-align:right">'
                    body += '%s :</td>' % (str(k).title())
                    body +='<td width="2%">&nbsp;</td>'
                    body += '<td>%s</td>' % (str(v))
                    body += '</tr>'
            body += '</table>'

            #generate charts inside category block
            if doc['extra'].has_key(key):
                extrainfo = doc['extra'][key]
                body += '<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px; padding:5px;border-top:1px solid #ccc;"><tr>'
                for k,v in extrainfo.iteritems():
                    xtitle = str(k)
                    ytitle = str(key)
                    # create listoflists from v,which is dict
                    listoflists = [["name",ytitle]]
                    for x,y in v.iteritems():
                        # do modifications to x and y if necessary
                        #pdb.set_trace()
                        x = str(x) #to remove u' from names
                        y = int(y)
                        listoflists.append([x,y])
                    script,divid = createchart("ColumnChart",listoflists,xtitle,ytitle)
                    body += script
                    body += '<td width = "50%">'
                    body += '<div id="%s"></div>' % (divid)
                    body += '</td>'
                body += '</tr></table>'
            body += '</div>'

        elif key == 'channels':
            body += '<div id = "category" style = "border:2px solid #ccc;margin:10px; ">'
            body += '<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px; padding:5px">'
            body += '<caption style="font:bold 16px Arial, Helvetica, sans-serif; padding:5px 0; border-bottom:1px solid #ccc;text-align:left;padding-left:15px;">Channels Performance ' 
            body += "</caption>"
            body += '<tr>'
            for item in [('Visitors','visits'),('Transactions','transactions'),('CPT','CPT'),('Average Value','avg_value'),('Conversion Rate','conversion_rate')]:
                xtitle = "Channels"
                ytitle = item[0]
                #generate listoflists
                listoflists = [[item[0],"value"]]
                for k,v in value.iteritems():
                    listoflists.append([k,v[item[1]]])
                script,divid = createchart("PieChart",listoflists,xtitle,ytitle)
                body += script
                body += '<td width = "20%">'
                body += '<div id="%s"></div>' % (divid)
                body += '</td>'
            body += '</tr><table>'
            body += '</div>'

        elif key == 'visitors':
            body += '<div id = "category" style = "border:2px solid #ccc;margin:10px; ">'
            body += '<table width="100%" cellspacing="0" cellpadding="0" style="font-size:12px; padding:5px">'
            body += '<caption style="font:bold 16px Arial, Helvetica, sans-serif; padding:5px 0; border-bottom:1px solid #ccc;text-align:left;padding-left:15px;">%s : ' % (str(key).title())
            body += str(value['total'])
            body += "</caption>"

            # generate info block inside category block
            for k,v in doc['visitors'].iteritems():
                body += '<tr>'
                if k != 'total':
                    body +='<td width="38%" style="text-align:right">'
                    body += '%s :</td>' % (str(k).title())
                    body +='<td width="2%">&nbsp;</td>'
                    body += '<td>%s</td>' % (str(v))
                    body += '</tr>'
            body += '</table>'

            # generate pie charts for geographical distribution
            body += '<tr>'
            for item in [('Visitors','visits'),('Transactions','transactions')]:
                xtitle = "Geographical Distribution"
                ytitle = item[0]
                #generate listoflists
                listoflists = [[item[0],"value"]]
                for k,v in value.iteritems():
                    listoflists.append([k,v[item[1]]])
                script,divid = createchart("PieChart",listoflists,xtitle,ytitle)
                body += script
                body += '<td width = "50%">'
                body += '<div id="%s"></div>' % (divid)
                body += '</td>'
            body += '</tr><table>'
            body += '</div>'


        else:
            pass


    return body
















