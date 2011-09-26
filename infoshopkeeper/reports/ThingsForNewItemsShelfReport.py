from Report import Report

from objects.kind import Kind

class ThingsForNewItemsShelfReport(Report):
    metadata={'name':'Things for New Items Shelf','action':'thingsForNewItemsShelf'}
    do_total=False
    show_header=True

    def query(self,args):
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
	SELECT title.id, title.booktitle, subq1.author_string, book.*  FROM title JOIN book ON title.id=book.title_id JOIN (SELECT t2.id AS subid, GROUP_CONCAT(author.author_name) AS author_string FROM title t2 JOIN author_title ON t2.id=author_title.title_id JOIN author ON author.id=author_title.author_id GROUP BY t2.id) AS subq1 ON subq1.subid=title.id WHERE title.kind_id=%s GROUP BY title.id HAVING COUNT(title_id)=1 AND book.status='STOCK' AND book.inventoried_when > DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) ORDER BY book.inventoried_when DESC
	""",(args['kind']))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_header(self):
        return "<tr><th>Title</th><th>Author</th></tr>"

    def format_results(self,results):
        return ["<tr onclick=\"window.open('/titleedit?id=%s');\"><td>%s</td><td>%s</td></tr>" % (r[0],r[1],r[2])  for r in results]


    def _queryForm(self):
        val="<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select>"
	
        return val
