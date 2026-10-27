"""Run the shipped regression using temporary synthetic data, not a live agent."""
import pathlib, runpy, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "memory"))
print("SYNTHETIC ONLY: temporary stores and fixture receipts; no live authentication.")
runpy.run_path(str(ROOT / "tests/test_lean_workflow.py"), run_name="__main__")
print("The base-store assertions concern a temporary test store, not production inspection.")
