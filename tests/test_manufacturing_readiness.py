import csv, pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.manufacturing_readiness import *

class ManufacturingReadinessTests(unittest.TestCase):
    def setUp(self):
        self.doc = load_readiness(ROOT / "manufacturing/readiness.json")

    def test_not_fabrication_ready(self):
        self.assertFalse(fabrication_ready(self.doc))

    def test_all_required_gates_declared(self):
        self.assertEqual(set(REQUIRED_FAB_GATES), set(self.doc["required_gates"]))

    def test_no_false_release(self):
        self.assertTrue(assert_no_false_release(self.doc))

    def test_gerbers_explicitly_blocked(self):
        self.assertIn("Gerber", self.doc["blocked_outputs"])

    def test_jlcpcb_explicitly_blocked(self):
        self.assertIn("JLCPCB-ready package", self.doc["blocked_outputs"])

    def test_shared_board_variants(self):
        self.assertTrue(self.doc["shared_board"])
        self.assertEqual(set(self.doc["variants"]), {"Air", "Hydro"})

    def test_bom_skeleton_has_eight_asics(self):
        with open(ROOT / "manufacturing/BOM_SKELETON.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        asic = next(r for r in rows if r["Function"] == "SHA-256 ASIC")
        self.assertEqual(int(asic["Qty"]), 8)
        self.assertEqual(asic["Candidate family/part"], "BM1373")

    def test_unresolved_bom_items_are_blockers(self):
        with open(ROOT / "manufacturing/BOM_SKELETON.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        unresolved = [r for r in rows if "UNSELECTED" in r["MPN status"] or "UNDESIGNED" in r["MPN status"]]
        self.assertGreater(len(unresolved), 0)
        self.assertTrue(all(r["Release blocker"] == "Yes" for r in unresolved))

if __name__ == "__main__":
    unittest.main()
