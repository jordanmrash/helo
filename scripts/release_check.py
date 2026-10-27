"""Offline public-repository gate. Standard library only; no live-system certification."""
import ast, json, os, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
def main():
    files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    files = sorted(set(files))
    checks = []
    def check(name, fn):
        try:
            fn()
            checks.append({"name": name, "passed": True})
        except Exception as e:
            checks.append({"name": name, "passed": False, "detail": str(e)})
    def require(ok, message):
        if not ok: raise ValueError(message)
    def scan():
        for rel in files:
            p = ROOT / rel
            require(not re.search(r"(?i)(\.(sqlite3?|db|pem|pfx|key)$|(^|/)(logs|secrets)/|(^|/)\.env$)", rel), "Forbidden artifact: " + rel)
            try: text = p.read_text(encoding="utf-8-sig")
            except UnicodeError: continue
            patterns = [r"(?i)[a-z]:[\\/]Users[\\/][^\s\\/]+", r"/(?:Users|home)/[^\s/]+/", r"(?i)https?://[^\s/]*devtunnels\.ms", r"gh[pousr]_" + r"[A-Za-z0-9]{20,}", r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]
            require(not any(re.search(x, text) for x in patterns), "Potential disclosure in " + rel)
    def links():
        for rel in files:
            if not rel.endswith(".md"): continue
            text = (ROOT / rel).read_text(encoding="utf-8-sig")
            text = re.sub(r"```.*?```", "", text, flags=re.S)
            for target in re.findall(r"\]\(([^\s)]+)\)", text):
                if re.match(r"^[a-zA-Z]+:", target) or target.startswith("#"): continue
                target = target.split("#")[0]
                require(((ROOT / rel).parent / target).exists(), "Broken local link: " + rel + " -> " + target)
    def syntax():
        for rel in files:
            p = ROOT / rel
            if p.suffix == ".py": ast.parse(p.read_text(encoding="utf-8-sig"), filename=rel)
            if p.suffix == ".json": json.loads(p.read_text(encoding="utf-8-sig"))
            if p.suffix == ".js": subprocess.run(["node", "--check", str(p)], check=True, capture_output=True, timeout=20)
    check("public disclosure patterns and artifact names", scan)
    check("local Markdown link targets (anchors excluded)", links)
    check("Python AST, JSON parsing, JavaScript syntax", syntax)
    commands = [["node", "release4/adapter-contract-selftest.js"], ["node", "release4/scoring-engine-selftest.js"], ["node", "examples/evidence-gate/run.js"]] if (ROOT / "release4").exists() else [[sys.executable, "examples/learning-cycle/run.py"]]
    for cmd in commands:
        def run(cmd=cmd):
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            r = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, timeout=45)
            require(r.returncode == 0, r.stdout + r.stderr)
            print(r.stdout.strip())
        check(" ".join(cmd[1:]), run)
    report = {"scope": "Offline source and synthetic checks only. No live host, authentication or behavioral-parity certification.", "checks": checks, "passed": all(c["passed"] for c in checks)}
    print(json.dumps(report, indent=2))
    if "--json" in sys.argv:
        i = sys.argv.index("--json")
        if i + 1 >= len(sys.argv): raise SystemExit("--json requires an output path")
        pathlib.Path(sys.argv[i+1]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1
if __name__ == "__main__": raise SystemExit(main())
