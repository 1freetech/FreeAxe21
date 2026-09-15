import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.power_architecture import load_architecture, validate_architecture, domain_map


class TestPowerArchitecture(unittest.TestCase):
    def setUp(self):
        self.arch = load_architecture()

    def test_reference_architecture_is_structurally_valid(self):
        self.assertEqual(validate_architecture(self.arch), [])

    def test_all_eight_asics_are_uniquely_mapped(self):
        m = domain_map(self.arch)
        self.assertEqual(set(m), {f"U{i}" for i in range(1, 9)})
        self.assertEqual(len(m), 8)

    def test_two_domains_four_series_asics_each(self):
        domains = self.arch["candidate_core_topology"]["domains"]
        self.assertEqual(len(domains), 2)
        self.assertTrue(all(len(d["asics"]) == 4 for d in domains))
        self.assertTrue(all(len(d["regulator_stack"]) == 2 for d in domains))

    def test_duplicate_asic_is_rejected(self):
        bad = copy.deepcopy(self.arch)
        bad["candidate_core_topology"]["domains"][1]["asics"][3] = "U1"
        self.assertTrue(validate_architecture(bad))

    def test_wrong_input_voltage_is_rejected(self):
        bad = copy.deepcopy(self.arch)
        bad["input"]["nominal_voltage_v"] = 5.0
        self.assertIn("current shared architecture requires nominal 12 V input", validate_architecture(bad))

    def test_hydro_flow_interlock_is_mandatory(self):
        bad = copy.deepcopy(self.arch)
        bad["variant_delta"]["Hydro"]["hard_interlock"] = "none"
        self.assertIn("Hydro variant must explicitly hard-interlock on loss of flow", validate_architecture(bad))


if __name__ == "__main__":
    unittest.main()
