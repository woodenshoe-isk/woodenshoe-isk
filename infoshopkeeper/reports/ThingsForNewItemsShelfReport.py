#Returns items that are less than a month old
from Report import Report

from objects.kind import Kind

class ThingsForNewItemsShelfReport(Report):
    metadata={'name':'Things for New Items Shelf','action':'thingsForNewItemsShelf'}
    do_total=False
    show_header=True

    def query(self,args):
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
            SELECT title.id, title.booktitle, subq1.author_string, MIN(book.inventoried_when) AS max_inv_when FROM title JOIN book ON title.id=book.title_id JOIN (SELECT t2.id AS subid, GROUP_CONCAT(author.author_name) AS author_string FROM title t2 JOIN author_title ON t2.id=author_title.title_id JOIN author ON author.id=author_title.author_id GROUP BY t2.id) AS subq1 ON subq1.subid=title.id WHERE title.kind_id=%s AND book.status='STOCK' GROUP BY title.id ORDER BY max_inv_when DESC LIMIT 100
        """, (args['kind']))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_header(self):
        return "<tr><th>Title</th><th>Author</th></tr>"

    def format_results(self,results):
        return ["<tr ondblclick=\"document.location.href='/titleedit?id=%s';\"><td>%s</td><td>%s</td></tr>" % (r[0],r[1],r[2])  for r in results]


    def _queryForm(self):
        val="<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select>"
	
        return val
