from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from .Report import Report
from .PdfReport import PdfReport
from reportlab.lib.units import inch
from objects.transaction import Transaction
import sys

class TransactionReport(Report, PdfReport):
    metadata={'name':'Transaction Report','action':'transactionreport'}
    total_index=3
    do_total=False
    show_header=True
     
    def query(self, args):
        #print>>sys.stderr, "in query", args
        what="%%%s%%" % args.get('what', '')
        action=args.get('action', '')
        begin_date=args.get('begin_date', '1990-01-01')
        end_date=args.get('end_date', '2030-01-01')
        
        #build table of clauses for WHERE 
        clauses=[]
        if what:
            clauses.append("transactionLog.info LIKE '%%%s%%'" % what )
        if action:
            clauses.append("transactionLog.action LIKE '%%%s%%'" % action )
        if begin_date:
            clauses.append("transactionLog.date >= '%s'" % begin_date )
        if end_date:
            clauses.append("transactionLog.date <= ADDDATE('%s',INTERVAL 1 DAY)" % end_date )

        results=Transaction.select( ' AND '.join(clauses))
        #print>>sys.stderr, 'Results:', results
        return results
    
    def format_results(self, results):
        return ["<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r.date, r.action, r.info, r.amount)  for r in results]
    
    def format_header(self):
        return "<tr><th>Date</th><th>Action</th><th>Info</th><th>Amount</th></tr>"

    def format_results_as_pdf(self, results):
        self.defineConstants()
        if len(results) == 0:
            raise TypeError
        num_rows = len(results) 
        rows_height = []  
        for a in range(num_rows):
            rows_height.append(None)
        colwidths = ( None, None, None, None, None, None, None, None)
        
        
        #print results
        t = Table( results )
        #t = Table( results, colwidths, rows_height )
        GRID_STYLE = TableStyle(
            [     ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                  ('FONT', (0, -1), (-1, -1), "Times-Bold"),
#                  ('FONT', (0,1), (-1, -1), "Times-Roman"),
              ('ALIGN', (1, 1), (-1, -1), 'RIGHT')]
            )
        t.setStyle( GRID_STYLE )
        return t

     
    def _queryForm(self):
        actionList=','.join(["<option value='%s'>%s</option>" % (x[0], x[0]) for x in Transaction._connection.queryAll("SELECT DISTINCT t.action FROM transactionLog t ORDER BY t.action")])
        return ("""<label class='textbox' for='what'>What</label> <input type='text' class='textbox' name='what' id='what' value='%s'/><br>
        <label class='textbox' for='action'>Action</label> <select class='textbox' id='action' name='action'>""" + actionList + """</select><br>
        <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/><br>
        <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/><br>
        <script type="text/javascript">                                         
            jQuery(document).ready( function(){
                jQuery('#begin_date,#end_date').datepicker({dateFormat:'yy-mm-dd'}).blur();
            });
        </script>        
        """) % (self.args.get("what", ""), self.args.get("begin_date", ""), self.args.get("end_date", ""))

