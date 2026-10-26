import sqlite3, pathlib, datetime, json
ROOT = pathlib.Path(__file__).resolve().parent
DB = ROOT / "helo_memory.sqlite3"
AGENT = "helo"
def connect():
    c=sqlite3.connect(str(DB))
    c.execute("PRAGMA foreign_keys=ON")
    return c
def initialize():
    if DB.exists(): raise RuntimeError("Refusing to initialize existing memory database")
    with connect() as c:
        c.execute("CREATE TABLE identity (agent TEXT PRIMARY KEY CHECK(agent = 'helo'), schema_version INTEGER NOT NULL)")
        c.execute("INSERT INTO identity VALUES (?,?)", (AGENT,1))
        c.execute("CREATE TABLE memories (id INTEGER PRIMARY KEY, agent TEXT NOT NULL CHECK(agent = 'helo'), content TEXT NOT NULL, evidence_ref TEXT NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(agent) REFERENCES identity(agent))")
        c.execute("CREATE TABLE lessons (id INTEGER PRIMARY KEY, agent TEXT NOT NULL CHECK(agent = 'helo'), content TEXT NOT NULL, evidence_ref TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','suspended')), failures INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL, FOREIGN KEY(agent) REFERENCES identity(agent))")
        c.execute("CREATE TRIGGER no_import_memories BEFORE INSERT ON memories WHEN NEW.evidence_ref NOT LIKE 'helo:%' BEGIN SELECT RAISE(ABORT,'Helo evidence required'); END")
        c.execute("CREATE TRIGGER no_import_lessons BEFORE INSERT ON lessons WHEN NEW.evidence_ref NOT LIKE 'helo:%' BEGIN SELECT RAISE(ABORT,'Helo evidence required'); END")
def status():
    with connect() as c:
        return {"agent":c.execute("SELECT agent FROM identity").fetchone()[0], "memories":c.execute("SELECT COUNT(*) FROM memories").fetchone()[0], "lessons":c.execute("SELECT COUNT(*) FROM lessons").fetchone()[0], "integrity":c.execute("PRAGMA integrity_check").fetchone()[0]}
if __name__ == "__main__":
    initialize()
    print(json.dumps(status(),sort_keys=True))
