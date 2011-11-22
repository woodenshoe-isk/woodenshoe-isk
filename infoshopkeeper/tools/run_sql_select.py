from components import db

def run_sql_select( query_string):
    conn=db.connect()
    # query_string='''
    # SELECT * FROM (SELECT b1.title_id FROM book b1 GROUP BY b1.title_id HAVING COUNT(CASE WHEN b1.status='STOCK' THEN 1 END) = 0) AS subq1 JOIN title t1 ON t1.id =subq1.title_id JOIN book b2 ON b2.title_id=t1.id 
    # '''
    query=db.connect().cursor()
    query.execute(query_string )
    headers=[ h[0] for h in query.description ]
    
    results=[]
    for i in xrange(1, query.rowcount):
        record=query.fetchone()
        results.append(dict(zip(headers, record)))
    return results
    