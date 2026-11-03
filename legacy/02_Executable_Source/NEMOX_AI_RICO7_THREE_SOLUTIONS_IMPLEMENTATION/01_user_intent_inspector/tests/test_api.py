from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)
def test_intent():
 r=client.post('/api/analyze',json={'request':'Same shipment as last week, but two days earlier.'});assert r.status_code==200
 assert r.json()['unresolved'];assert r.json()['fields']['F05']['requirements'][0]['value']==-2
