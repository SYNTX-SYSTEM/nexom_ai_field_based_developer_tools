from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fieldcore import uid
from store import Store
import os
app=FastAPI(title='Recursive Feedback Engine')
store=Store(os.getenv('DB_PATH','feedback.sqlite'))
class DecisionInput(BaseModel):
 request:str=Field(min_length=1)
 carrier:str
 customer_id:str='demo-customer'
class FeedbackInput(BaseModel):
 decision_id:str
 corrected_carrier:str
 reason:str|None=None
class Confirmation(BaseModel):
 correction_id:str
 confirmed:bool
class Query(BaseModel):
 customer_id:str='demo-customer'
 request:str
@app.post('/api/decisions')
def decision(d:DecisionInput):
 x={'decision_id':uid(),**d.model_dump(),'context_snapshot':{'customer_id':d.customer_id},'status':'proposed'}
 store.save('decision',x,x['decision_id']);store.event('DECISION_CAPTURED',x['decision_id'],x);return x
@app.post('/api/feedback')
def feedback(f:FeedbackInput):
 d=store.get(f.decision_id)
 if not d or 'decision_id' not in d:raise HTTPException(404,'decision not found')
 x={'correction_id':uid(),**f.model_dump(),'old_carrier':d['carrier'],'customer_id':d['customer_id'],'status':'proposed'}
 store.save('correction',x,x['correction_id']);store.event('CORRECTION_PROPOSED',f.decision_id,x);return x
@app.post('/api/confirm')
def confirm(c:Confirmation):
 x=store.get(c.correction_id)
 if not x or 'correction_id' not in x:raise HTTPException(404,'correction not found')
 if x['status']!='proposed':raise HTTPException(409,'already reviewed')
 x={**x,'status':'confirmed' if c.confirmed else 'rejected'}
 store.save('review',x);store.event('CORRECTION_REVIEWED',x['decision_id'],x);return x
@app.post('/api/context/retrieve')
def retrieve(q:Query):
 confirmed=[x for x in store.list('review') if x['status']=='confirmed' and x['customer_id']==q.customer_id]
 selected=confirmed[-1:] if confirmed else []
 return {'request':q.request,'customer_id':q.customer_id,'retrieved_relations':[{'carrier':x['corrected_carrier'],'source_correction_id':x['correction_id']} for x in selected]}
@app.post('/api/compare')
def compare(q:Query):
 ctx=retrieve(q);carrier=ctx['retrieved_relations'][0]['carrier'] if ctx['retrieved_relations'] else 'Carrier A'
 return {'input':q.request,'without_feedback':{'carrier':'Carrier A'},'with_feedback':{'carrier':carrier},'retrieval_manifest':ctx['retrieved_relations'],'changed':carrier!='Carrier A'}
@app.get('/api/timeline')
def timeline():return {'decisions':store.list('decision'),'corrections':store.list('correction'),'reviews':store.list('review')}
