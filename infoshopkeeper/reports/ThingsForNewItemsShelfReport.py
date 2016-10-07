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
            SELECT DISTINCT(subq2.id), subq2.booktitle, subq2.author_string 
                FROM (SELECT t2.id id, t2.booktitle booktitle, subq1.author_string author_string, subq1.min_b_inventoried_when  FROM 
                        (SELECT t1.isbn isbn, MIN(t1.id) min_isbn, MIN(b1.inventoried_when) min_b_inventoried_when, GROUP_CONCAT(DISTINCT(a1.author_name)) author_string 
                                FROM book b1                    
                                JOIN title t1 ON b1.title_id=t1.id  
                                JOIN author_title at1 ON at1.title_id=t1.id 
                                JOIN author a1 ON at1.author_id=a1.id  
                                WHERE t1.kind_id=%s AND b1.status='STOCK'
                                GROUP BY t1.isbn) AS subq1 
                        JOIN title t2 ON t2.isbn=subq1.isbn 
                        JOIN book b2 ON b2.title_id=t2.id
                        WHERE b2.status='STOCK') AS subq2 
                ORDER BY subq2.min_b_inventoried_when 
                DESC LIMIT 100
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
