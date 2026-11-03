from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)
def test_feedback():
 d=client.post('/api/decisions',json={'request':'Quote freight','carrier':'Carrier A'}).json()
 f=client.post('/api/feedback',json={'decision_id':d['decision_id'],'corrected_carrier':'Carrier B'}).json()
 c=client.post('/api/confirm',json={'correction_id':f['correction_id'],'confirmed':True});assert c.status_code==200
 comparison=client.post('/api/compare',json={'request':'Quote freight again'}).json()
 assert comparison['with_feedback']['carrier']=='Carrier B'
