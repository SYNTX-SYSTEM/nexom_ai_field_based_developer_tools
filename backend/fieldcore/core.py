import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager

DB = Path(__file__).resolve().parents[2] / 'data' / 'nemox.sqlite3'
STATES = {'INITIAL': {'ENRICHED','UNRESOLVED'}, 'ENRICHED': {'UNRESOLVED','CONFIRMED'}, 'UNRESOLVED': {'ENRICHED','CORRECTED'}, 'CORRECTED': {'CONFIRMED','UNRESOLVED'}, 'CONFIRMED': {'SUPERSEDED'}, 'SUPERSEDED': set()}

def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return str(uuid.uuid4())

@contextmanager
def connection():
    DB.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(DB,timeout=10)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback();raise
    finally: db.close()

def init():
    with connection() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS fields(id TEXT PRIMARY KEY,type TEXT NOT NULL,scope TEXT NOT NULL,state TEXT NOT NULL,version INTEGER NOT NULL,payload TEXT NOT NULL,source_refs TEXT NOT NULL,created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS relations(id TEXT PRIMARY KEY,source TEXT NOT NULL,target TEXT NOT NULL,kind TEXT NOT NULL,scope TEXT NOT NULL,valid INTEGER NOT NULL DEFAULT 1,source_event TEXT NOT NULL,created TEXT NOT NULL,FOREIGN KEY(source) REFERENCES fields(id),FOREIGN KEY(target) REFERENCES fields(id));
        CREATE TABLE IF NOT EXISTS transitions(id TEXT PRIMARY KEY,field_id TEXT NOT NULL,old_state TEXT NOT NULL,new_state TEXT NOT NULL,event TEXT NOT NULL,version INTEGER NOT NULL,created TEXT NOT NULL,FOREIGN KEY(field_id) REFERENCES fields(id));
        CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY,scope TEXT NOT NULL,context TEXT NOT NULL,action TEXT NOT NULL,created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS feedback(id TEXT PRIMARY KEY,decision_id TEXT NOT NULL,scope TEXT NOT NULL,correction TEXT NOT NULL,status TEXT NOT NULL,created TEXT NOT NULL,FOREIGN KEY(decision_id) REFERENCES decisions(id));
        CREATE TABLE IF NOT EXISTS gaps(id TEXT PRIMARY KEY,request_id TEXT NOT NULL,capability TEXT NOT NULL,scope TEXT NOT NULL,values_json TEXT NOT NULL,created TEXT NOT NULL);
        ''')

class FieldRepository:
    def create(self,kind,scope,payload,refs=None,state='INITIAL'):
        fid=uid()
        with connection() as db:
            db.execute('INSERT INTO fields VALUES(?,?,?,?,?,?,?,?)',(fid,kind,scope,state,1,json.dumps(payload),json.dumps(refs or []),now()))
        return self.get(fid)
    def get(self,fid):
        with connection() as db:
            row=db.execute('SELECT * FROM fields WHERE id=?',(fid,)).fetchone()
        if row is None: raise ValueError('field not found')
        d=dict(row);d['payload']=json.loads(d['payload']);d['source_refs']=json.loads(d['source_refs']);return d
    def transition(self,fid,new,event,expected=None):
        with connection() as db:
            row=db.execute('SELECT state,version FROM fields WHERE id=?',(fid,)).fetchone()
            if not row: raise ValueError('field not found')
            if expected is not None and expected!=row['version']: raise ValueError('version conflict')
            if new not in STATES[row['state']]: raise ValueError(f'invalid transition {row["state"]} -> {new}')
            version=row['version']+1
            db.execute('UPDATE fields SET state=?,version=? WHERE id=?',(new,version,fid))
            db.execute('INSERT INTO transitions VALUES(?,?,?,?,?,?,?)',(uid(),fid,row['state'],new,event,version,now()))
        return self.get(fid)
    def relation(self,source,target,kind,scope,event):
        with connection() as db:
            a=db.execute('SELECT scope FROM fields WHERE id=?',(source,)).fetchone();b=db.execute('SELECT scope FROM fields WHERE id=?',(target,)).fetchone()
            if not a or not b: raise ValueError('unknown relation endpoint')
            if a['scope']!=scope or b['scope']!=scope: raise ValueError('scope mismatch')
            rid=uid();db.execute('INSERT INTO relations VALUES(?,?,?,?,?,?,?,?)',(rid,source,target,kind,scope,1,event,now()))
        return {'id':rid,'source':source,'target':target,'kind':kind,'scope':scope}
    def graph(self,scope):
        with connection() as db:
            fields=[dict(x) for x in db.execute('SELECT * FROM fields WHERE scope=? ORDER BY created',(scope,))]
            relations=[dict(x) for x in db.execute('SELECT * FROM relations WHERE scope=?',(scope,))]
            transitions=[dict(x) for x in db.execute('SELECT * FROM transitions WHERE field_id IN (SELECT id FROM fields WHERE scope=?)',(scope,))]
        for f in fields:f['payload']=json.loads(f['payload']);f['source_refs']=json.loads(f['source_refs'])
        return {'fields':fields,'relations':relations,'transitions':transitions}
    def reset(self):
        with connection() as db:
            for table in ['relations','transitions','feedback','gaps','decisions','fields']:db.execute('DELETE FROM '+table)

class FieldContextResolver:
    def resolve(self,scope,origin=None):
        graph=FieldRepository().graph(scope)
        if not origin:return graph
        ids={origin}
        changed=True
        while changed:
            old=len(ids)
            for r in graph['relations']:
                if r['valid'] and (r['source'] in ids or r['target'] in ids):ids.update([r['source'],r['target']])
            changed=len(ids)!=old
        graph['fields']=[f for f in graph['fields'] if f['id'] in ids]
        graph['relations']=[r for r in graph['relations'] if r['source'] in ids and r['target'] in ids]
        return graph
