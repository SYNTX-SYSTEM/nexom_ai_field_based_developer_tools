import re,json
from fieldcore.core import connection,uid,now,FieldRepository
CAPABILITIES={'cheaper_shipping':{'required':['shipment_id','rate_options','delivery_deadline'],'questions':{'shipment_id':'Which shipment should we use?','rate_options':'Which rate options are available?','delivery_deadline':'What is the latest acceptable delivery date?'},'dependencies':{'rate_options':['shipment_id'],'delivery_deadline':['shipment_id']}},'booking':{'required':['shipment_id','destination','delivery_deadline'],'questions':{'shipment_id':'Which shipment?','destination':'What destination?','delivery_deadline':'What deadline?'},'dependencies':{}}}

def capability(text):return 'cheaper_shipping' if re.search('cheaper|lower cost',text,re.I) else 'booking'
def analyze(text,scope='demo',values=None):
    values=values or {};kind=capability(text);spec=CAPABILITIES[kind]
    request=FieldRepository().create('Request',scope,{'text':text},['user-input'])
    fid=uid()
    with connection() as db:db.execute('INSERT INTO gaps VALUES(?,?,?,?,?,?)',(fid,request['id'],kind,scope,json.dumps(values),now()))
    return evaluate(fid,scope)
def evaluate(gid,scope):
    with connection() as db:row=db.execute('SELECT * FROM gaps WHERE id=? AND scope=?',(gid,scope)).fetchone()
    if not row:raise ValueError('gap not found')
    spec=CAPABILITIES[row['capability']];values=json.loads(row['values_json']);missing=[x for x in spec['required'] if not values.get(x)]
    frontier=[x for x in missing if all(values.get(d) for d in spec['dependencies'].get(x,[]))]
    return {'id':gid,'capability':row['capability'],'values':values,'missing':missing,'blocking_frontier':frontier,'questions':[{'attribute':x,'question':spec['questions'][x]} for x in frontier],'complete':not missing,'edges':[{'source':d,'target':x} for x,deps in spec['dependencies'].items() for d in deps]}
def resolve(gid,scope,answers):
    with connection() as db:
        row=db.execute('SELECT values_json FROM gaps WHERE id=? AND scope=?',(gid,scope)).fetchone()
        if not row:raise ValueError('gap not found')
        values=json.loads(row['values_json']);values.update({k:v for k,v in answers.items() if v is not None and str(v).strip()})
        db.execute('UPDATE gaps SET values_json=? WHERE id=?',(json.dumps(values),gid))
    return evaluate(gid,scope)
