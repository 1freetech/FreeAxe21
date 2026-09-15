import json
from pathlib import Path
import unittest

from model.input_power_path import (
    current_for_power,
    evaluate_input_path,
    fuse_allowed_current_a,
    split_two_domain_input,
    validate_contact_margin,
)

ROOT = Path(__file__).resolve().parents[1]


class InputPowerPathTests(unittest.TestCase):
    def test_42a_operating_contact_split(self):
        r = evaluate_input_path(12.0, 42.0)
        self.assertAlmostEqual(r.current_per_positive_contact_a, 21.0)
        self.assertAlmostEqual(r.current_per_return_contact_a, 21.0)
        self.assertAlmostEqual(r.power_w, 504.0)

    def test_50a_is_validation_ceiling_not_operating_current(self):
        data = json.loads((ROOT / "architecture" / "input_power_path.json").read_text())
        self.assertLess(data["operational_continuous_input_current_a"], data["connector_path_validation_ceiling_a"])
        self.assertEqual(data["connector_path_validation_ceiling_a"], 50.0)

    def test_400w_low_line_current(self):
        self.assertAlmostEqual(current_for_power(400.0, 10.8), 37.037037, places=5)

    def test_450w_low_line_fits_42a_operating_limit(self):
        amps = current_for_power(450.0, 10.8)
        self.assertLessEqual(amps, 42.0)
        self.assertGreater(amps, 41.0)

    def test_two_domain_split_at_400w_low_line(self):
        r = split_two_domain_input(400.0, 10.8)
        self.assertAlmostEqual(r.branch_current_a, 18.5185185, places=5)
        self.assertAlmostEqual(r.connector_current_a, 37.037037, places=5)

    def test_two_domain_branch_design_has_headroom(self):
        r = split_two_domain_input(450.0, 10.8)
        self.assertLess(r.branch_current_a, 22.0)

    def test_mega_fit_family_margin_at_90_percent(self):
        self.assertTrue(validate_contact_margin(50.0, 2, 30.0, 0.90))
        self.assertFalse(validate_contact_margin(55.0, 2, 30.0, 0.90))

    def test_fuse_thermal_screening(self):
        self.assertEqual(fuse_allowed_current_a(65), 51.0)
        self.assertEqual(fuse_allowed_current_a(85), 46.0)
        self.assertEqual(fuse_allowed_current_a(110), 38.0)
        self.assertGreater(fuse_allowed_current_a(85), 42.0)
        self.assertLess(fuse_allowed_current_a(110), 42.0)

    def test_candidate_harness_loss_at_42a(self):
        r = evaluate_input_path(12.0, 42.0, harness_loop_resistance_ohm=0.0066)
        self.assertAlmostEqual(r.harness_drop_v, 0.2772, places=4)
        self.assertAlmostEqual(r.harness_loss_w, 11.6424, places=4)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            evaluate_input_path(0, 10)
        with self.assertRaises(ValueError):
            evaluate_input_path(12, -1)
        with self.assertRaises(ValueError):
            evaluate_input_path(12, 1, positive_contacts=0)
        with self.assertRaises(ValueError):
            fuse_allowed_current_a(130)

    def test_architecture_is_two_branch(self):
        data = json.loads((ROOT / "architecture" / "input_power_path.json").read_text())
        self.assertEqual(data["distribution"]["asic_domain_count"], 2)
        self.assertEqual(data["distribution"]["asic_count_per_domain"], 4)
        self.assertNotIn("four ASIC VRM domains", data["distribution"]["topology"])

    def test_connector_contact_loading_below_family_max(self):
        data = json.loads((ROOT / "architecture" / "input_power_path.json").read_text())
        self.assertLessEqual(
            data["connector"]["validation_ceiling_current_a_per_power_contact_at_50a"],
            data["connector"]["family_max_current_a_per_circuit"],
        )

    def test_fuse_voltage_and_temperature_gate(self):
        data = json.loads((ROOT / "architecture" / "input_power_path.json").read_text())
        self.assertGreaterEqual(data["fuse"]["voltage_rating_v"], data["input_voltage_v_max"])
        self.assertGreaterEqual(data["fuse"]["published_typical_derated_allowed_current_a"]["85c"],
                                data["operational_continuous_input_current_a"])


if __name__ == "__main__":
    unittest.main()
