from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from Report import Report
from PdfReport import PdfReport
from reportlab.lib.units import inch
import sys

from objects.kind import Kind


class SalesReport(Report, PdfReport):
    metadata={'name':'Sales Report','action':'salesreport'}
    reportname = 'Sales Report'
    total_index=3
    do_total=True
    show_header=True
    
    def headscripts(self):
        return '''
            <script type="text/javascript">                                         
                jQuery(document).ready( function(){
                    jQuery('#begin_date,#end_date').datepicker({dateFormat:'yy-mm-dd'}).blur();
                    jQuery('td.status:contains("NOT FOUND")').parent().children('td').css({'color':'red'});
                });
           </script>
        '''      

        
    def query(self,args):
        self.cursor=self.conn.cursor()
        kind="%s" % args.get('kind', '1')
        print>>sys.stderr, kind
        print>>sys.stderr, args
        begin_date=args.get('begin_date','1990-01-01') or  '1990-01-01'
        end_date=args.get('end_date','2030-01-01') or '2030-01-01'
        with_notfound = args.get('with_notfound',False) or False
        print>>sys.stderr, begin_date, end_date, with_notfound
        if with_notfound:
            status_string = '\'SOLD|NOT FOUND\''
        else:
            status_string= '\'SOLD\''
        sql_query = """
            SELECT 
                t1.id, t1.booktitle, b1.sold_when, b1.ourprice, 
                COUNT( CASE WHEN b2.status='STOCK' 
                       THEN 1 
                       ELSE NULL END) AS copies_in_stock, 
                COUNT( CASE WHEN b2.status='SOLD'
                       THEN 1 
                       ELSE NULL END) AS copies_sold, 
                b1.status 
            FROM title t1 
            JOIN book b1 
              ON t1.id=b1.title_id 
            JOIN kind k1 
              ON t1.kind_id=k1.id  
            JOIN book b2 
              ON b2.title_id=t1.id 
            WHERE k1.id=%s AND b1.status 
            RLIKE %s AND b1.sold_when>='%s' 
              AND b1.sold_when<=ADDDATE('%s',INTERVAL 1 DAY) 
            GROUP BY b1.id  
            ORDER BY b1.sold_when""" % (kind, status_string, begin_date, end_date)
        print>>sys.stderr, sql_query
        self.cursor.execute( sql_query )
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_results(self,results):
        return ["<tr ondblclick=\"document.location.href='/titleedit?id=%s';\"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class='status'>%s</td></tr>" % (r[0], r[1], r[2], r[3], r[4], r[5], r[6])  for r in results]
    
    def format_header(self):
	return "<tr><th>Title</th><th>Date Sold</th><th>Price</th><th>Copies In Stock</th><th>Copies Sold</th><th>Status</th></tr>"

    def format_results_as_pdf(self,results):
        self.defineConstants()
        if len(results) == 0:
            raise TypeError
        num_rows = len(results) 
        rows_height = []  
        for a in range(num_rows):
            rows_height.append(None)
        colwidths = ( None,None,None,None,None,None,None,None)
        
        #print results
        t = Table( results )
        #t = Table( results, colwidths, rows_height )
        GRID_STYLE = TableStyle(
            [     ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                  ('FONT', (0,-1), (-1, -1), "Times-Bold"),
#                  ('FONT', (0,1), (-1, -1), "Times-Roman"),
              ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
            )
        t.setStyle( GRID_STYLE )
        return t

     
    def _queryForm(self):
        val="<label class='textbox' for='kind'>Kind</label><select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select><br>"
        val =val+"""
            <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/><br>
            <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/><br>
            <label class='textbox' for='with_notfound'>Include \"NOT FOUND\" records?</label><input type='checkbox' class='textbox' name='with_notfound' id='with_notfound'/><br>
        """ % (self.args.get("begin_date",""),self.args.get("end_date",""))
        return val

