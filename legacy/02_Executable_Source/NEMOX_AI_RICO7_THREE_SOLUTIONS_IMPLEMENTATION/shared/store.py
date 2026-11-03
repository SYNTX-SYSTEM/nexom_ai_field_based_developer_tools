import sqlite3, json
from pathlib import Path
from fieldcore import uid,now
class Store:
 def __init__(self,path):
  self.path=path; self.db=sqlite3.connect(path,check_same_thread=False)
  self.db.execute('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL)')
  self.db.execute('CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, correlation_id TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL)')
  self.db.commit()
 def save(self,kind,obj,id=None):
  id=id or uid(); self.db.execute('INSERT INTO records VALUES (?,?,?,?)',(id,kind,json.dumps(obj),now()));self.db.commit();return id
 def get(self,id):
  row=self.db.execute('SELECT payload FROM records WHERE id=?',(id,)).fetchone();return json.loads(row[0]) if row else None
 def list(self,kind):
  return [{'id':r[0],**json.loads(r[1])} for r in self.db.execute('SELECT id,payload FROM records WHERE kind=? ORDER BY created_at',(kind,))]
 def event(self,kind,correlation_id,payload):
  eid=uid();self.db.execute('INSERT INTO events VALUES (?,?,?,?,?)',(eid,correlation_id,kind,json.dumps(payload),now()));self.db.commit();return eid
