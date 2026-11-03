from datetime import datetime, timezone
from uuid import uuid4
from typing import Literal
from pydantic import BaseModel, Field

def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return str(uuid4())
class SourceRef(BaseModel):
    source_id: str
    segment: str = ''
class FieldRecord(BaseModel):
    field_id: str = Field(default_factory=uid)
    field_type: str
    scope_id: str
    version: int = 1
    state: Literal['INITIAL','ENRICHED','UNRESOLVED','CORRECTED','CONFIRMED','SUPERSEDED']='INITIAL'
    values: dict = Field(default_factory=dict)
    sources: list[SourceRef] = Field(default_factory=list)
class Relation(BaseModel):
    relation_id: str = Field(default_factory=uid)
    source_id: str
    predicate: str
    target_id: str
    source_ref: str
    status: Literal['proposed','confirmed','superseded']='proposed'
class Event(BaseModel):
    event_id: str = Field(default_factory=uid)
    kind: str
    aggregate_id: str
    correlation_id: str
    payload: dict
    occurred_at: str = Field(default_factory=now)
TRANSITIONS={
 'INITIAL':{'ENRICHED','UNRESOLVED'},
 'ENRICHED':{'UNRESOLVED','CONFIRMED','CORRECTED'},
 'UNRESOLVED':{'ENRICHED','CORRECTED'},
 'CORRECTED':{'CONFIRMED','UNRESOLVED'},
 'CONFIRMED':{'SUPERSEDED'},
 'SUPERSEDED':set(),
}
def transition(record:FieldRecord, target:str):
    if target not in TRANSITIONS[record.state]: raise ValueError(f'invalid transition {record.state} -> {target}')
    return record.model_copy(update={'state':target,'version':record.version+1})
