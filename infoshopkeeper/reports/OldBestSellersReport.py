from .Report import Report

from objects.kind import Kind


class BestSellersReport(Report):
    metadata = {"name": "Best Sellers Report", "action": "bestsellersreport"}
    do_total = False
    show_header = True

    def query(self, args):
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            SELECT 
                title.id, title.booktitle, 
                COUNT(
                            CASE WHEN b1.status='STOCK' 
                            THEN 1 
                            ELSE NULL END) number_in_stock, 
                subq1.number_sold 
            FROM (SELECT 
                    book.title_id AS id1, 
                    COUNT(*) AS number_sold 
                  FROM book 
                  WHERE book.status='SOLD' 
                  GROUP BY book.title_id ) AS subq1 
            JOIN book b1 
              ON subq1.id1=b1.title_id 
            JOIN title 
              ON title.id=subq1.id1 
           WHERE title.kind_id=%s 
           GROUP BY b1.title_id 
           ORDER BY subq1.number_sold DESC;
        """,
            (args["kind"]),
        )
        results = self.cursor.fetchall()
        self.cursor.close()
        return results

    def format_header(self):
        return "<tr><th>Title</th><th>Copies In Stock</th><th>Copies Sold</th></tr>"

    def format_results(self, results):
        return [
            "<tr ondblclick=\"document.location.href='/titleedit?id=%s';\"><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (r[0], r[1], r[2], r[3])
            for r in results
        ]

    def _queryForm(self):
        val = "<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val + "<option value='%s'>%s</option>" % (k.id, k.kindName)
        val = val + "</select>"
        return val
