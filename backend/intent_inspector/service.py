import re
from fieldcore.core import FieldRepository,FieldContextResolver

HISTORY=[{'id':'SHP-100','customer':'demo','origin':'Munich','destination':'Hamburg','delivery':'2026-11-07','carrier':'North Freight'}, {'id':'SHP-101','customer':'demo','origin':'Munich','destination':'Berlin','delivery':'2026-11-08','carrier':'East Freight'}]

def inspect(request,scope='demo'):
    repo=FieldRepository();source=repo.create('Request',scope,{'text':request},['user-input'])
    requirements=[]
    if re.search(r'two days earlier|2 days earlier',request,re.I):requirements.append({'name':'delivery_delta_days','value':-2,'evidence':'two days earlier'})
    if re.search(r'cheaper|lower cost',request,re.I):requirements.append({'name':'price_priority','value':'lower','evidence':'cheaper'})
    historical=bool(re.search(r'last week|same shipment|as usual',request,re.I))
    candidates=HISTORY if historical else []
    unresolved=['historical_shipment_reference'] if len(candidates)!=1 and historical else []
    intent=repo.create('Intent',scope,{'goal':'shipment_change' if historical else 'logistics_request','unresolved':unresolved},['user-input'])
    req=repo.create('Requirement',scope,{'items':requirements},['user-input'])
    context=repo.create('OperationalContext',scope,{'candidates':candidates,'selected':None},['synthetic-history'])
    for f in [intent,req,context]:repo.transition(f['id'],'UNRESOLVED' if unresolved else 'ENRICHED','interpretation')
    for target,kind in [(intent,'INTERPRETED_AS'),(req,'REQUIRES'),(context,'CONTEXT_CANDIDATES')]:repo.relation(source['id'],target['id'],kind,scope,'request')
    return {'request':request,'requirements':requirements,'candidates':candidates,'unresolved':unresolved,'field_ids':[source['id'],intent['id'],req['id'],context['id']],'trace':FieldContextResolver().resolve(scope,source['id'])}
