##Return books that are less than a month old we havent had before.

from Report import Report

from objects.kind import Kind

class NewItemReport(Report):
    metadata={'name':'New This Month','action':'newitemreport'}
    do_total=False
    show_header=True

    def query(self,args):
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
	SELECT title.id, title.booktitle, GROUP_CONCAT(DISTINCT author.author_name), kind.kind_name, book.listprice FROM book, title, author, kind WHERE book.title_id=title.id AND author.title_id=title.id AND kind.id=title.kind_id AND kind.id=%s GROUP BY author.title_id HAVING MAX(book.inventoried_when)>DATE_ADD(CURDATE(), INTERVAL -30 DAY) ORDER BY book.inventoried_when DESC
	""",(args['kind']))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_header(self):
	return "<tr><th>Title</th><th>Author</th><th>Kind</th><th>Price</th></tr>"

    def format_results(self,results):
        return ["<tr ondblclick=\"document.location.href='/titleedit?id=%s';\"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0],r[1], r[2], r[3], r[4])  for r in results]


    def _queryForm(self):
        val="<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select>"
	
        return val
