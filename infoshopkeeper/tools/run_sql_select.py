from tools import db

def run_sql_select( query_string):
    conn=db.connect()
    query=db.connect().cursor()
    query.execute(query_string )
    
    #get names of columns
    headers=[ h[0] for h in query.description ]
    
    results=[]
    for i in xrange(1, query.rowcount):
        record=query.fetchone()
        results.append(dict(zip(headers, record)))
    return results
    
