import tempfile,pathlib,sqlite3,json,hashlib,hmac,os
import helo_memory as b,exact_retrieval as x,lean_workflow as w
if b.DB.exists(): b.DB.unlink()
b.initialize()
assert b.status()["memories"]==0 and b.status()["lessons"]==0
KEY=bytes.fromhex("11"*32)
os.environ["HELO_RECEIPT_HMAC_KEY_HEX"]=KEY.hex()
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
    root=pathlib.Path(d);db=root/"isolated.sqlite3"
    with sqlite3.connect(str(b.DB)) as src,sqlite3.connect(str(db)) as dst: src.backup(dst)
    def receipt(name,identity="Helo",status="COMPLETED"):
        p=root/(name+".json")
        rec={"tool":"run_job","status":status,"exit_code":0,"timed_out":False,"op_id":"helo-"+name,"script":"approved.ps1","sha256_run":"a"*64,"authenticated_agent_id":identity,"identity_verified_by":"8938"}
        canonical=json.dumps(rec,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
        rec["receipt_hmac_sha256"]=hmac.new(KEY,canonical,hashlib.sha256).hexdigest()
        p.write_text(json.dumps(rec))
        return str(p)
    q=dict(zip(x.FIELDS,("Helo","test","issue","v1","exact","none")))
    req=dict(q,lesson_text="synthetic verified correction",failure_record=receipt("failure"),correction_record=receipt("correction"))
    tampered=pathlib.Path(receipt("tampered"))
    tampered_obj=json.loads(tampered.read_text());tampered_obj["status"]="FAILED";tampered.write_text(json.dumps(tampered_obj))
    tampered_req=dict(q,lesson_text="tampered receipt",failure_record=str(tampered),correction_record=receipt("tampered-correction"))
    assert w.record_lesson(tampered_req,db,root)["error"]=="RECEIPT_AUTHENTICATION_FAILED"
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
    unsafe=root/"unsafe.sqlite3";unsafe.write_bytes(b"")
    if os.name=="posix":
        unsafe.chmod(0o644)
        try: b.connect(unsafe);assert False,"permissive database accepted"
        except RuntimeError as e: assert str(e)=="INSECURE_DATABASE_PERMISSIONS"
        unsafe.chmod(0o600)
    target=root/"target.sqlite3";target.write_bytes(b"")
    link=root/"linked.sqlite3"
    try:
        link.symlink_to(target)
        try: b.connect(link);assert False,"symlink database accepted"
        except RuntimeError as e: assert str(e)=="UNSAFE_DATABASE_PATH"
    except (OSError,NotImplementedError): pass
    print("PASS isolated write, retrieval, duplicate rejection, foreign identity rejection, feedback, suspension, replay rejection")
assert b.status()["memories"]==0 and b.status()["lessons"]==0
print("PASS production remains blank; production writes blocked")
