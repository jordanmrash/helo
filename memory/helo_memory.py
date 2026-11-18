import sqlite3, pathlib, datetime, json, os, stat
ROOT = pathlib.Path(__file__).resolve().parent
DB = ROOT / "helo_memory.sqlite3"
AGENT = "helo"
def _reject_unsafe_path(path):
    p=pathlib.Path(path)
    for candidate in (p.parent,p):
        if candidate.exists():
            info=candidate.lstat()
            if stat.S_ISLNK(info.st_mode) or bool(getattr(info,"st_file_attributes",0) & 0x400): raise RuntimeError("UNSAFE_DATABASE_PATH")
    return p.resolve(strict=False)
def _restrict_permissions(path):
    if os.name=="posix":
        os.chmod(path,0o600)
        if stat.S_IMODE(path.stat().st_mode) & 0o077: raise RuntimeError("INSECURE_DATABASE_PERMISSIONS")
def connect(path=DB,readonly=False):
    p=_reject_unsafe_path(path)
    if readonly:
        if not p.exists(): raise RuntimeError("DATABASE_NOT_FOUND")
        c=sqlite3.connect(f"file:{p.as_posix()}?mode=ro",uri=True,timeout=3)
        c.execute("PRAGMA query_only=ON")
    else:
        existed=p.exists()
        c=sqlite3.connect(str(p),timeout=5)
        if not existed: _restrict_permissions(p)
        elif os.name=="posix" and stat.S_IMODE(p.stat().st_mode) & 0o077:
            c.close();raise RuntimeError("INSECURE_DATABASE_PERMISSIONS")
    c.execute("PRAGMA foreign_keys=ON")
    return c
def initialize():
    if DB.exists(): raise RuntimeError("Refusing to initialize existing memory database")
    with connect() as c:
        c.execute("CREATE TABLE identity (agent TEXT PRIMARY KEY CHECK(agent = 'helo'), schema_version INTEGER NOT NULL)")
        c.execute("INSERT INTO identity VALUES (?,?)", (AGENT,1))
        c.execute("CREATE TABLE memories (id INTEGER PRIMARY KEY, agent TEXT NOT NULL CHECK(agent = 'helo'), content TEXT NOT NULL, evidence_ref TEXT NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(agent) REFERENCES identity(agent))")
        c.execute("CREATE TABLE lessons (id INTEGER PRIMARY KEY, agent TEXT NOT NULL CHECK(agent = 'helo'), content TEXT NOT NULL, evidence_ref TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','suspended')), failures INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL, FOREIGN KEY(agent) REFERENCES identity(agent))")
        c.execute("CREATE TABLE evidence (id TEXT PRIMARY KEY, agent TEXT NOT NULL CHECK(agent = 'helo'), source TEXT NOT NULL, outcome TEXT NOT NULL, payload_sha256 TEXT NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(agent) REFERENCES identity(agent))")
        c.execute("CREATE TABLE lesson_index (lesson_id INTEGER PRIMARY KEY REFERENCES lessons(id), agent_id TEXT NOT NULL CHECK(agent_id='Helo'), scope TEXT NOT NULL, problem_signature TEXT NOT NULL, compatibility_contract TEXT NOT NULL, applicability TEXT NOT NULL, exceptions TEXT NOT NULL)")
        c.execute("CREATE INDEX idx_helo_exact ON lesson_index(agent_id,scope,problem_signature,compatibility_contract,applicability,exceptions)")
        c.execute("CREATE TRIGGER no_import_memories BEFORE INSERT ON memories WHEN NEW.evidence_ref NOT LIKE 'helo:%' BEGIN SELECT RAISE(ABORT,'Helo evidence required'); END")
        c.execute("CREATE TRIGGER no_import_lessons BEFORE INSERT ON lessons WHEN NEW.evidence_ref NOT LIKE 'helo:%' BEGIN SELECT RAISE(ABORT,'Helo evidence required'); END")
def status():
    with connect() as c:
        return {"agent":c.execute("SELECT agent FROM identity").fetchone()[0], "memories":c.execute("SELECT COUNT(*) FROM memories").fetchone()[0], "lessons":c.execute("SELECT COUNT(*) FROM lessons").fetchone()[0], "integrity":c.execute("PRAGMA integrity_check").fetchone()[0]}
if __name__ == "__main__":
    initialize()
    print(json.dumps(status(),sort_keys=True))
