import json,sqlite3,pathlib,hashlib,datetime
import helo_memory as b
import exact_retrieval as x
FIELDS=x.FIELDS
def hashfile(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
    return h.hexdigest()
def validate_8938(ref,root,expected_agent="Helo"):
    base=pathlib.Path(root).resolve(strict=True)
    path=pathlib.Path(ref).resolve(strict=True)
    if not path.is_relative_to(base) or path.suffix.lower()!=".json": raise ValueError("FOREIGN_PATH")
    rec=json.loads(path.read_text(encoding="utf-8"))
    if rec.get("tool") not in ("run_job","run_batch_file") or rec.get("status")!="COMPLETED" or rec.get("exit_code")!=0 or rec.get("timed_out") is not False: raise ValueError("INVALID_8938_OPERATION")
    if not rec.get("op_id") or not rec.get("script") or not rec.get("sha256_run"): raise ValueError("INCOMPLETE_8938_OPERATION")
    # An operation prefix or filename is not proof of the initiating agent.
    if rec.get("authenticated_agent_id")!=expected_agent or rec.get("identity_verified_by")!="8938": raise ValueError("AGENT_IDENTITY_UNVERIFIED")
    return {"op_id":rec["op_id"],"record_sha256":hashfile(path)}
def valid_request(d,keys):
    return type(d) is dict and set(d)==set(keys) and d.get("agent_id")=="Helo" and all(type(d[k]) is str and 0<len(d[k])<=256 for k in keys)
def record_lesson(d,db=None,record_root=None):
    keys=FIELDS+("lesson_text","failure_record","correction_record")
    if not valid_request(d,keys): return {"status":"REJECTED","error":"INVALID_INPUT"}
    if db is None or record_root is None or pathlib.Path(db).resolve()==b.DB.resolve(): return {"status":"REJECTED","error":"PRODUCTION_WRITES_DISABLED"}
    try:
        failure=validate_8938(d["failure_record"],record_root)
        correction=validate_8938(d["correction_record"],record_root)
        if failure["op_id"]==correction["op_id"]: raise ValueError("SAME_OPERATION")
        payload=json.dumps({"failure":failure,"correction":correction},sort_keys=True,separators=(",",":"))
        h=hashlib.sha256(payload.encode()).hexdigest();eid="helo:"+h
        with sqlite3.connect(str(db),timeout=5) as c:
            c.execute("PRAGMA foreign_keys=ON");c.execute("BEGIN IMMEDIATE")
            if c.execute("SELECT agent FROM identity").fetchone()[0]!="helo": raise ValueError("FOREIGN_DATABASE")
            query="SELECT COUNT(*) FROM lesson_index x JOIN lessons l ON x.lesson_id=l.id WHERE "+" AND ".join("x."+k+"=?" for k in FIELDS)+" AND l.status='active'"
            if c.execute(query,tuple(d[k] for k in FIELDS)).fetchone()[0]: raise ValueError("DUPLICATE_LESSON")
            c.execute("INSERT INTO evidence(id,agent,source,outcome,payload_sha256,payload,created_at) VALUES(?,?,?,?,?,?,?)",(eid,"helo","helo_runtime","verified_correction",h,payload,datetime.datetime.now(datetime.timezone.utc).isoformat()))
            c.execute("INSERT INTO lessons(agent,content,evidence_ref,status,failures,created_at) VALUES(?,?,?,?,?,?)",("helo",d["lesson_text"],eid,"active",0,datetime.datetime.now(datetime.timezone.utc).isoformat()))
            lid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
            c.execute("INSERT INTO lesson_index(lesson_id,agent_id,scope,problem_signature,compatibility_contract,applicability,exceptions) VALUES(?,?,?,?,?,?,?)",(lid,)+tuple(d[k] for k in FIELDS))
            assert c.execute("SELECT evidence_ref FROM lessons WHERE id=?",(lid,)).fetchone()[0]==eid
            c.commit()
        return {"status":"COMPLETED","lesson_id":lid,"readback_verified":True}
    except (ValueError,KeyError,TypeError,sqlite3.Error,OSError,json.JSONDecodeError) as e: return {"status":"REJECTED","error":str(e)}
def record_application(d,db=None,record_root=None):
    keys=("agent_id","lesson_id","operation_id","outcome","evidence_ref")
    if not valid_request(d,keys) or d["outcome"] not in ("verified_success","verified_failure"): return {"status":"REJECTED","error":"INVALID_INPUT"}
    if db is None or record_root is None or pathlib.Path(db).resolve()==b.DB.resolve(): return {"status":"REJECTED","error":"PRODUCTION_WRITES_DISABLED"}
    try:
        rec=validate_8938(d["evidence_ref"],record_root)
        if rec["op_id"]!=d["operation_id"]: raise ValueError("OPERATION_MISMATCH")
        with sqlite3.connect(str(db),timeout=5) as c:
            c.execute("BEGIN IMMEDIATE")
            lid=int(d["lesson_id"]);row=c.execute("SELECT failures,status FROM lessons WHERE id=? AND agent='helo'",(lid,)).fetchone()
            if not row: raise ValueError("LESSON_NOT_FOUND")
            c.execute("CREATE TABLE IF NOT EXISTS application_log (operation_id TEXT PRIMARY KEY,lesson_id INTEGER NOT NULL,outcome TEXT NOT NULL,receipt_sha256 TEXT NOT NULL)")
            c.execute("INSERT INTO application_log VALUES(?,?,?,?)",(rec["op_id"],lid,d["outcome"],rec["record_sha256"]))
            failures=row[0]+(d["outcome"]=="verified_failure");status="suspended" if failures>=2 else row[1]
            c.execute("UPDATE lessons SET failures=?,status=? WHERE id=?",(failures,status,lid))
            assert c.execute("SELECT status FROM lessons WHERE id=?",(lid,)).fetchone()[0]==status
            c.commit()
        return {"status":"COMPLETED","lesson_status":status,"failures":failures}
    except (ValueError,KeyError,TypeError,sqlite3.Error,OSError,json.JSONDecodeError) as e: return {"status":"REJECTED","error":str(e)}
