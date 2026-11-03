import pytest
from fastapi.testclient import TestClient
from api.main import app
from fieldcore.core import FieldRepository
client=TestClient(app)
@pytest.fixture(autouse=True)
def clean():FieldRepository().reset();yield;FieldRepository().reset()
def test_intent_trace():
    r=client.post('/api/intent',json={'text':'Same shipment as last week, but two days earlier.'});assert r.status_code==200
    x=r.json();assert x['requirements'][0]['value']==-2;assert 'historical_shipment_reference' in x['unresolved'];assert len(x['trace']['relations'])==3

def test_feedback_scope_and_confirm():
    d=client.post('/api/decisions',json={'action':'Carrier A'}).json()
    f=client.post('/api/feedback',json={'decision_id':d['id'],'correction':{'operation':'quote','route':'MUC-HAM','preferred_action':'Carrier B'}}).json()
    assert client.post('/api/subsequent',json={'operation':'quote','route':'MUC-HAM','base_action':'Carrier A'}).json()['result']['action']=='Carrier A'
    assert client.post(f"/api/feedback/{f['id']}/confirm",json={'accept':True}).status_code==200
    x=client.post('/api/subsequent',json={'operation':'quote','route':'MUC-HAM','base_action':'Carrier A'}).json()
    assert x['result']['action']=='Carrier B';assert x['changed']
    y=client.post('/api/subsequent',json={'operation':'quote','route':'MUC-BER','base_action':'Carrier A'}).json();assert not y['changed']
    assert len(client.get('/api/history/demo').json()['feedback'])==1

def test_gap_resolution():
    x=client.post('/api/gaps',json={'text':'Ship this as usual, but use the cheaper option.'}).json()
    assert x['blocking_frontier']==['shipment_id']
    x=client.post(f"/api/gaps/{x['id']}/resolve",json={'answers':{'shipment_id':'SHP-100'}}).json()
    assert set(x['blocking_frontier'])=={'rate_options','delivery_deadline'}
    x=client.post(f"/api/gaps/{x['id']}/resolve",json={'answers':{'rate_options':'A,B','delivery_deadline':'2026-11-10'}}).json();assert x['complete']

def test_state_validation():
    repo=FieldRepository();f=repo.create('Intent','demo',{})
    with pytest.raises(ValueError):repo.transition(f['id'],'CONFIRMED','invalid')
    repo.transition(f['id'],'ENRICHED','extract');assert repo.transition(f['id'],'CONFIRMED','review')['version']==3

def test_relation_scope():
    repo=FieldRepository();a=repo.create('A','demo',{});b=repo.create('B','other',{})
    with pytest.raises(ValueError):repo.relation(a['id'],b['id'],'X','demo','event')
