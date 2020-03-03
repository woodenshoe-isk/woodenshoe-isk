from .Report import Report

from objects.kind import Kind


class BestSellersReport(Report):
    metadata = {"name": "Best Sellers", "action": "bestsellersreport"}
    reportname = "Best Sellers Report"
    show_header = True
    do_total = False

    def query(self, args):
        begin_date = args.get("begin_date", "1990-01-01")
        end_date = args.get("end_date", "2030-01-01")
        if not begin_date:
            begin_date = "1990-01-01"
        if not end_date:
            end_date = "2030-01-01"
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
        SELECT booktitle,count(book.id) AS blah FROM book JOIN title ON book.title_id=title.id WHERE book.status='SOLD' AND title.kind_id=%s AND sold_when>=%s AND sold_when<=ADDDATE(%s,INTERVAL 1 DAY)  GROUP BY title_id ORDER BY blah DESC LIMIT 100
        """,
            (args["kind"], begin_date, end_date),
        )

        results = self.cursor.fetchall()
        self.cursor.close()
        return results

    def format_header(self):
        return "<tr><th>Title</th><th>Count</th></tr>"

    def format_results(self, results):
        return ["<tr><td>%s</td><td>%s</td></tr>" % (r[0], r[1]) for r in results]

    def _queryForm(self):
        val = "<label class='textbox' for='kind'>Kind</label><select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val + "<option value='%s'>%s</option>" % (k.id, k.kindName)
        val = val + "</select><br>"
        val = (
            val
            + """
            <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/><br>
            <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/><br>
            <script type="text/javascript">                                         
                jQuery(document).ready( function(){
                    jQuery('#begin_date,#end_date').datepicker({dateFormat:'yy-mm-dd'}).blur();
                });
            </script>        
        """
            % (self.args.get("begin_date", ""), self.args.get("end_date", ""))
        )
        return val
