from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from Report import Report
from PdfReport import PdfReport
from reportlab.lib.units import inch


class SalesReport(Report, PdfReport):
    metadata={'name':'Sales Report','action':'salesreport'}
    reportname = 'Sales Report'
    total_index=3
    do_total=True
    show_header=True
        
    def query(self,args):
        self.cursor=self.conn.cursor()
        what="%%%s%%" % args['what']
        begin_date=args.get('begin_date','1990-01-01')
        end_date=args.get('end_date','2030-01-01')
#        self.cursor.execute("""SELECT * FROM transactionLog WHERE action='SALE' AND info LIKE %s AND date>=%s AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date""",(what,begin_date,end_date ))
        self.cursor.execute("""SELECT t1.id, t1.booktitle, b1.sold_when, b1.ourprice, COUNT(CASE WHEN b2.status='STOCK' THEN 1 ELSE NULL END) as copies_in_stock, COUNT(CASE WHEN b2.status='SOLD' THEN 1 ELSE NULL END) as copies_sold FROM title t1 JOIN book b1 ON t1.id=b1.title_id JOIN book b2 ON b1.title_id=b2.title_id JOIN kind k1 ON t1.kind_id=k1.id WHERE (b1.status='SOLD' AND (k1.kind_name LIKE %s OR t1.booktitle LIKE %s) AND (b1.sold_when>=%s AND b1.sold_when<=ADDDATE(%s,INTERVAL 1 DAY)))   GROUP BY b1.id ORDER BY b1.sold_when""", (what, what, begin_date, end_date))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_results(self,results):
    # 11/10/2008 john fixed this manually
    #        return ["<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[2],r[4].tostring(),r[1])  for r in results]
    #   return ["<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[2],r[4],r[1])  for r in results]
        return ["<tr onclick=\"window.open('/titleedit?id=%s');\"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0],r[1],r[2],r[3],r[4], r[5])  for r in results]
    
    def format_header(self):
	return ["<tr><th>Date Sold</th><th>Title</th><th>Price</th><th>Copies In Stock</th><th>Copies Sold</th></tr>"]

    def format_results_as_pdf(self,results):
        self.defineConstants()
        if len(results) == 0:
            raise TypeError
        num_rows = len(results) 
        rows_height = []  
        for a in range(num_rows):
            rows_height.append(None)
        colwidths = ( None,None,None,None,None,None,None,None)
        
        
        print results
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
        return """<label class='textbox' for='what'>What</label> <input type='text' class='textbox' name='what' id='what' value='%s'/><br>
        <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/><br>
        <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/><br>
        <script type="text/javascript">                                         
            jQuery(document).ready( function(){
                jQuery('#begin_date,#end_date').datepicker({dateFormat:'yy-mm-dd'});
            });
        </script>        
        """ % (self.args.get("what",""),self.args.get("begin_date",""),self.args.get("end_date",""))

