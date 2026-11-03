from fastapi.testclient import TestClient
from backend.main import app,minimal_missing
client=TestClient(app)
def test_gaps():
 r=client.post('/api/gaps/analyze',json={'request':'Ship as usual but cheaper'});assert r.status_code==200
 assert 'shipment_reference' in r.json()['missing']
 assert minimal_missing({'shipment_reference','origin','destination','delivery_limit'})==[] or minimal_missing({'shipment_reference','origin','destination','delivery_limit'})==['choose_cheaper_carrier']
