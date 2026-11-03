from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fieldcore import uid
from store import Store
import os
app=FastAPI(title='Understanding Gap Detector')
store=Store(os.getenv('DB_PATH','gaps.sqlite'))
class Request(BaseModel):
 request:str=Field(min_length=1)
 available:dict[str,str]=Field(default_factory=dict)
class Resolution(BaseModel):
 analysis_id:str
 attribute:str
 value:str=Field(min_length=1)
# Graph edges express prerequisites. Multiple options can be modeled by alternative sets.
REQUIRES={'choose_cheaper_carrier':[{'baseline_shipment','rate_options','delivery_limit'}], 'baseline_shipment':[{'shipment_reference'}], 'rate_options':[{'origin','destination'}], 'delivery_limit':[]}
def minimal_missing(available:set[str],target='choose_cheaper_carrier'):
 def walk(node,stack):
  if node in available:return [set()]
  if node in stack:raise ValueError('dependency cycle')
  alternatives=REQUIRES.get(node,[])
  if not alternatives:return [{node}]
  results=[]
  for group in alternatives:
   choices=[set()]
   for child in sorted(group):
    sub=walk(child,stack|{node})
    choices=[a|b for a in choices for b in sub]
   results+=choices
  return results
 options=walk(target,set());min_size=min(map(len,options));return sorted([sorted(x) for x in options if len(x)==min_size])[0]
@app.post('/api/gaps/analyze')
def analyze(req:Request):
 missing=minimal_missing(set(req.available))
 x={'analysis_id':uid(),'request':req.request,'available':req.available,'missing':missing,'state':'UNRESOLVED' if missing else 'CONFIRMED','clarifications':[{'attribute':k,'question':f'Please provide {k.replace("_"," ")}.'} for k in missing]}
 store.save('analysis',x,x['analysis_id']);store.event('GAP_ANALYZED',x['analysis_id'],x);return x
@app.post('/api/gaps/resolve')
def resolve(r:Resolution):
 x=store.get(r.analysis_id)
 if not x or 'analysis_id' not in x:raise HTTPException(404,'analysis not found')
 updated={**x['available'],r.attribute:r.value};missing=minimal_missing(set(updated))
 result={'analysis_id':uid(),'parent_analysis_id':r.analysis_id,'request':x['request'],'available':updated,'missing':missing,'state':'UNRESOLVED' if missing else 'CONFIRMED','clarifications':[{'attribute':k,'question':f'Please provide {k.replace("_"," ")}.'} for k in missing]}
 store.save('analysis',result,result['analysis_id']);store.event('GAP_RESOLVED',result['analysis_id'],result);return result
@app.get('/api/gaps/{analysis_id}')
def get(analysis_id:str):
 x=store.get(analysis_id)
 if not x:raise HTTPException(404,'analysis not found')
 return x
