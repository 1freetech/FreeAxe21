#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.manufacturing_readiness import load_readiness, missing_gates, assert_no_false_release

doc = load_readiness(ROOT / "manufacturing/readiness.json")
assert_no_false_release(doc)
missing = missing_gates(doc)
print("FREEAXE 21 fabrication release: BLOCKED" if missing else "FREEAXE 21 fabrication release: READY")
for gate in missing:
    print(f"- {gate}")
sys.exit(1 if missing else 0)
