import sqlite3, pathlib, hashlib
import helo_memory as base
FIELDS=("agent_id","scope","problem_signature","compatibility_contract","applicability","exceptions")
def lookup(criteria, db=None):
    if type(criteria) is not dict or set(criteria)!=set(FIELDS): raise ValueError("invalid query fields")
    if criteria.get("agent_id")!="Helo" or any(type(criteria[k]) is not str or not 0<len(criteria[k])<=256 for k in FIELDS): raise ValueError("invalid Helo query")
    path=pathlib.Path(db) if db is not None else base.DB
    uri="file:"+path.resolve().as_posix()+"?mode=ro"
    with sqlite3.connect(uri,uri=True,timeout=3) as c:
        c.execute("PRAGMA query_only=ON")
        c.execute("PRAGMA foreign_keys=ON")
        row=c.execute("SELECT l.id,l.content,l.evidence_ref,e.payload,e.payload_sha256 FROM lesson_index x INDEXED BY idx_helo_exact JOIN lessons l ON l.id=x.lesson_id JOIN evidence e ON e.id=l.evidence_ref WHERE x.agent_id=? AND x.scope=? AND x.problem_signature=? AND x.compatibility_contract=? AND x.applicability=? AND x.exceptions=? AND l.agent='helo' AND l.status='active' AND e.agent='helo' AND e.source='helo_runtime' AND e.outcome='verified_correction' LIMIT 2",tuple(criteria[k] for k in FIELDS)).fetchall()
        valid=[r for r in row if hashlib.sha256(r[3].encode()).hexdigest()==r[4]]
        if len(row)!=1 or len(valid)!=1: return None
        return {"lesson_id":valid[0][0],"content":valid[0][1],"evidence_ref":valid[0][2]}
def schema_sql():
    return ("CREATE TABLE IF NOT EXISTS lesson_index (lesson_id INTEGER PRIMARY KEY REFERENCES lessons(id), agent_id TEXT NOT NULL CHECK(agent_id='Helo'), scope TEXT NOT NULL, problem_signature TEXT NOT NULL, compatibility_contract TEXT NOT NULL, applicability TEXT NOT NULL, exceptions TEXT NOT NULL)", "CREATE INDEX IF NOT EXISTS idx_helo_exact ON lesson_index(agent_id,scope,problem_signature,compatibility_contract,applicability,exceptions)")
