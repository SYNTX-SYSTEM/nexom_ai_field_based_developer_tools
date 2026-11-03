from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fieldcore import uid
from store import Store
import os,re
app=FastAPI(title='User Intent Inspector')
store=Store(os.getenv('DB_PATH','intent.sqlite'))
class Request(BaseModel):
 request:str=Field(min_length=1)
 customer_id:str='demo-customer'
class History(BaseModel):
 shipment_id:str
 customer_id:str='demo-customer'
 delivery_date:str
 carrier:str
@app.post('/api/history')
def add_history(h:History):return {'id':store.save('history',h.model_dump())}
@app.post('/api/analyze')
def analyze(req:Request):
 text=req.request;ref=bool(re.search(r'last week|same shipment|as usual',text,re.I))
 match=re.search(r'(\d+|one|two|three|four|five) days? earlier',text,re.I)
 delta=-(int(match.group(1)) if match.group(1).isdigit() else {'one':1,'two':2,'three':3,'four':4,'five':5}[match.group(1).lower()]) if match else None
 candidates=[x for x in store.list('history') if x['customer_id']==req.customer_id] if ref else []
 gaps=[]
 if ref and len(candidates)!=1:gaps.append({'code':'HISTORICAL_REFERENCE','reason':f'{len(candidates)} candidate shipments','status':'unresolved'})
 if delta is not None and len(candidates)!=1:gaps.append({'code':'BASELINE_DATE','reason':'relative date requires resolved shipment','status':'unresolved'})
 requirements=[{'kind':'delivery_delta_days','value':delta,'source_ref':'request:relative-date'}] if delta is not None else []
 result={'trace_id':uid(),'original_request':text,'fields':{'F02':{'request':text},'F04':{'historical_reference':ref},'F05':{'requirements':requirements}},'candidate_shipments':candidates,'unresolved':gaps,'relations':[{'predicate':'REFERENCES_SHIPMENT','status':'resolved' if len(candidates)==1 else 'unresolved'}] if ref else []}
 store.save('trace',result,result['trace_id']);store.event('INTERPRETATION_CREATED',result['trace_id'],result)
 return result
@app.get('/api/traces/{trace_id}')
def trace(trace_id:str):
 x=store.get(trace_id)
 if x is None:raise HTTPException(404,'trace not found')
 return x
@app.get('/api/history')
def history():return store.list('history')
