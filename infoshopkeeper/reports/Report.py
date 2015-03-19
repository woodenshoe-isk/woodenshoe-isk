# a base class for all reports
from components import db
from formencode import htmlfill


class Report:
    ##must be filled out in subclass
    ##name is actual display name
    ##action is url href. Name it what you like, 
    ##it just needs a string for factory to create link
    metadata={'name':'', 'action':''}
    
    #if you want todal rollup at end
    #total_index is column you want totaled
    total_index=0
    do_total=False
    
    #do we want to see the header of the results table?
    show_header=False

    def __init__(self,args):
        self.conn=db.connect()
        self.args=args
    
    def get_total(self,results):
        total=0
        for r in results:
            total=total+r[self.total_index]
        return total
    
    #override to do actual query
    def query(self,args):
        self.cursor=self.conn.cursor()
    
    #generally leave this alone
    def queryForm(self):
        top="<form action='/report' method='get'>"
        bottom_template="<input type='hidden' name='query_made' /><input type='hidden' name='reportname'/><div class='button_panel'><input type='submit' class='submit' value='get report'/></div></form>"
        defaults={"reportname":self.metadata['action'], "query_made":"yes"}
        parser=htmlfill.FillingParser(defaults)
        parser.feed(bottom_template)
        parser.close()
        html=top+self._queryForm()+parser.text()
        return html
    
    #override to do return actual form for query
    def _queryForm(self):
        return ""
        
    #override to format header if you want to show results header
    def formatHeader(self):
        pass
    
    #override thist to format results in a table format
    def formatResults(self, results):
        pass
