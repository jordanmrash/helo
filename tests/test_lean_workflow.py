import tempfile,pathlib,sqlite3,json,hashlib
import helo_memory as b,exact_retrieval as x,lean_workflow as w
import atexit
_test_db_directory=tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
atexit.register(_test_db_directory.cleanup)
b.DB=pathlib.Path(_test_db_directory.name)/"test_memory.sqlite3"
b.initialize()
with sqlite3.connect(str(b.DB)) as _schema_db:
    _schema_db.execute("CREATE TABLE IF NOT EXISTS evidence (id TEXT PRIMARY KEY, agent TEXT NOT NULL, source TEXT NOT NULL, outcome TEXT NOT NULL, payload_sha256 TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL)")
    _schema_db.execute("CREATE TABLE IF NOT EXISTS lesson_index (lesson_id INTEGER NOT NULL, agent_id TEXT NOT NULL, scope TEXT NOT NULL, problem_signature TEXT NOT NULL, compatibility_contract TEXT NOT NULL, applicability TEXT NOT NULL, exceptions TEXT NOT NULL, FOREIGN KEY(lesson_id) REFERENCES lessons(id))")
    _schema_db.execute("CREATE INDEX IF NOT EXISTS idx_helo_exact ON lesson_index(agent_id,scope,problem_signature,compatibility_contract,applicability,exceptions)")
assert b.status()["memories"]==0 and b.status()["lessons"]==0
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    root=pathlib.Path(d);db=root/"isolated.sqlite3"
    with sqlite3.connect(str(b.DB)) as src,sqlite3.connect(str(db)) as dst: src.backup(dst)
    def receipt(name,identity="Helo",status="COMPLETED"):
        p=root/(name+".json")
        p.write_text(json.dumps({"tool":"run_job","status":status,"exit_code":0,"timed_out":False,"op_id":"helo-"+name,"script":"approved.ps1","sha256_run":"a"*64,"authenticated_agent_id":identity,"identity_verified_by":"8938"}))
        return str(p)
    q=dict(zip(x.FIELDS,("Helo","test","issue","v1","exact","none")))
    req=dict(q,lesson_text="synthetic verified correction",failure_record=receipt("failure"),correction_record=receipt("correction"))
    assert w.record_lesson(req)["status"]=="REJECTED"
    result=w.record_lesson(req,db,root);assert result["status"]=="COMPLETED",result
    lid=result["lesson_id"];assert x.lookup(q,db)["lesson_id"]==lid
    assert w.record_lesson(req,db,root)["error"]=="DUPLICATE_LESSON"
    bad=dict(req,problem_signature="different",correction_record=receipt("acl",identity="ACL"))
    assert w.record_lesson(bad,db,root)["error"]=="AGENT_IDENTITY_UNVERIFIED"
    for name in ("failone","failtwo"):
        path=receipt(name);out=w.record_application({"agent_id":"Helo","lesson_id":str(lid),"operation_id":"helo-"+name,"outcome":"verified_failure","evidence_ref":path},db,root)
        assert out["status"]=="COMPLETED",out
    assert out["lesson_status"]=="suspended" and out["failures"]==2
    assert x.lookup(q,db) is None
    assert w.record_application({"agent_id":"Helo","lesson_id":str(lid),"operation_id":"helo-failtwo","outcome":"verified_failure","evidence_ref":path},db,root)["status"]=="REJECTED"
    with sqlite3.connect(str(db)) as c: assert c.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    print("PASS isolated write, retrieval, duplicate rejection, foreign identity rejection, feedback, suspension, replay rejection")
assert b.status()["memories"]==0 and b.status()["lessons"]==0
print("PASS production remains blank; production writes blocked")
