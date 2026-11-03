from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from typing import Any
from fieldcore.core import init,FieldRepository
from intent_inspector.service import inspect
from feedback_engine.service import decide,correct,confirm,retrieve,subsequent,history
from gap_detector.service import analyze,resolve
init()
app=FastAPI(title='nemox Field Developer Tools',version='1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:3000','http://127.0.0.1:3000'],allow_methods=['*'],allow_headers=['*'])
class Request(BaseModel):
    text:str=Field(min_length=1);scope:str='demo';values:dict[str,Any]={}
class Decision(BaseModel):
    scope:str='demo';action:str;context:dict[str,Any]={}
class Correction(BaseModel):
    scope:str='demo';decision_id:str;correction:dict[str,Any]
class Confirmation(BaseModel):
    scope:str='demo';accept:bool
class Subsequent(BaseModel):
    scope:str='demo';operation:str;route:str;base_action:str
class Answers(BaseModel):
    scope:str='demo';answers:dict[str,Any]
@app.exception_handler(ValueError)
async def invalid(request,exc):return __import__('fastapi').responses.JSONResponse(status_code=400,content={'detail':str(exc)})
@app.get('/api/health')
def health():return {'ok':True}
@app.post('/api/intent')
def intent(r:Request):return inspect(r.text,r.scope)
@app.post('/api/decisions')
def decision(r:Decision):return decide(r.scope,r.action,r.context)
@app.post('/api/feedback')
def feedback(r:Correction):return correct(r.decision_id,r.scope,r.correction)
@app.post('/api/feedback/{fid}/confirm')
def confirmation(fid:str,r:Confirmation):return confirm(fid,r.scope,r.accept)
@app.post('/api/subsequent')
def next_decision(r:Subsequent):return subsequent(r.scope,r.operation,r.route,r.base_action)
@app.get('/api/history/{scope}')
def decision_history(scope:str):return history(scope)
@app.post('/api/gaps')
def gaps(r:Request):return analyze(r.text,r.scope,r.values)
@app.post('/api/gaps/{gid}/resolve')
def gap_resolution(gid:str,r:Answers):return resolve(gid,r.scope,r.answers)
@app.get('/api/graph/{scope}')
def graph(scope:str):return FieldRepository().graph(scope)
@app.post('/api/reset')
def reset():FieldRepository().reset();return {'reset':True}
