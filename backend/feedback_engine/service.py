import json
from fieldcore.core import connection,uid,now,FieldRepository

def decide(scope,action,context):
    did=uid()
    with connection() as db:db.execute('INSERT INTO decisions VALUES(?,?,?,?,?)',(did,scope,json.dumps(context),action,now()))
    return {'id':did,'scope':scope,'action':action,'context':context}

def correct(decision_id,scope,correction):
    with connection() as db:
        d=db.execute('SELECT * FROM decisions WHERE id=? AND scope=?',(decision_id,scope)).fetchone()
        if not d:raise ValueError('decision not found in scope')
        fid=uid();db.execute('INSERT INTO feedback VALUES(?,?,?,?,?,?)',(fid,decision_id,scope,json.dumps(correction),'PROPOSED',now()))
    return {'id':fid,'decision_id':decision_id,'scope':scope,'correction':correction,'status':'PROPOSED'}

def confirm(feedback_id,scope,accept):
    with connection() as db:
        row=db.execute('SELECT * FROM feedback WHERE id=? AND scope=?',(feedback_id,scope)).fetchone()
        if not row:raise ValueError('feedback not found')
        if row['status']!='PROPOSED':raise ValueError('feedback already reviewed')
        status='CONFIRMED' if accept else 'REJECTED'
        db.execute('UPDATE feedback SET status=? WHERE id=?',(status,feedback_id))
    field=None
    if accept:
        repo=FieldRepository();field=repo.create('Feedback',scope,{'decision_id':row['decision_id'],'correction':json.loads(row['correction']),'feedback_id':feedback_id},['user-confirmation'])
        repo.transition(field['id'],'ENRICHED','feedback-recorded');repo.transition(field['id'],'CONFIRMED','user-confirmation')
    return {'id':feedback_id,'status':status,'field':field}

def retrieve(scope,operation,route):
    with connection() as db:rows=db.execute('SELECT f.* FROM feedback f JOIN decisions d ON f.decision_id=d.id WHERE f.scope=? AND f.status="CONFIRMED" ORDER BY f.created',(scope,)).fetchall()
    matches=[]
    for row in rows:
        c=json.loads(row['correction'])
        if c.get('operation')==operation and c.get('route')==route:matches.append({'feedback_id':row['id'],'correction':c})
    return matches

def subsequent(scope,operation,route,base_action):
    matches=retrieve(scope,operation,route)
    action=matches[-1]['correction'].get('preferred_action',base_action) if matches else base_action
    d=decide(scope,action,{'operation':operation,'route':route,'retrieved_feedback_ids':[m['feedback_id'] for m in matches]})
    return {'baseline':base_action,'result':d,'retrieved':matches,'changed':action!=base_action}

def history(scope):
    with connection() as db:
        decisions=[dict(r) for r in db.execute('SELECT * FROM decisions WHERE scope=? ORDER BY created',(scope,))]
        feedback=[dict(r) for r in db.execute('SELECT * FROM feedback WHERE scope=? ORDER BY created',(scope,))]
    for d in decisions:d['context']=json.loads(d['context'])
    for f in feedback:f['correction']=json.loads(f['correction'])
    return {'decisions':decisions,'feedback':feedback}
