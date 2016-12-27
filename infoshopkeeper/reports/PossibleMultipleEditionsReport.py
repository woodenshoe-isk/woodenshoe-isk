##return books with same title & different isbn
##mostly we're looking for hardcovers to return
from .Report import Report

from objects.kind import Kind

class PossibleMultipleEditionsReport(Report):
    metadata={'name':'Possible Multiple Editions','action':'possibleMultipleEditionsReport'}
    do_total=False
    show_header=True

    def query(self, args):
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
	SELECT t1.id, t1.booktitle, t1.isbn, COUNT(b1.id) FROM title t1 JOIN title t2 ON t1.booktitle=t2.booktitle JOIN book b1 ON b1.title_id=t1.id JOIN book b2 ON b2.title_id=t2.id WHERE t2.isbn != t1.isbn AND t1.kind_id=1 AND b1.status='STOCK' AND b2.status='STOCK' GROUP BY t1.id ORDER BY t1.booktitle
	""")
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_header(self):
	return "<tr><th>Title</th><th>ISBN</th><th>Copies in Stock</th></tr>"

    def format_results(self, results):
        return ["<tr ondblclick=\"document.location.href='/titleedit?id=%s';\"><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0], r[1], r[2], r[3])  for r in results]



