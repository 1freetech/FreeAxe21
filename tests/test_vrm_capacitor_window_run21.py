import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.vrm_capacitor_window_run21 import *

class TestVRMCapWindow(unittest.TestCase):
    def test_transient_10a(self):
        self.assertAlmostEqual(transient_capacitance_f(10,.68e-6,4,.1)*1e6,170.0)
    def test_bandwidth_10a(self):
        self.assertAlmostEqual(bandwidth_capacitance_f(10,.1,600e3)*1e6,265.258,places=3)
    def test_ripple(self):
        self.assertAlmostEqual(ripple_capacitance_f(6.536,600e3,.02)*1e6,68.083,places=3)
    def test_20a_window(self):
        row=qualification_window()["transient_rows"][1]
        self.assertEqual(row["governing_min_uf"],680.0)
    def test_25a_window(self):
        row=qualification_window()["transient_rows"][2]
        self.assertEqual(row["governing_min_uf"],1062.5)
    def test_monotonic(self):
        rows=qualification_window()["transient_rows"]
        self.assertLess(rows[0]["governing_min_uf"],rows[1]["governing_min_uf"])
        self.assertLess(rows[1]["governing_min_uf"],rows[2]["governing_min_uf"])
    def test_invalid(self):
        with self.assertRaises(ValueError): transient_capacitance_f(0,.68e-6,4,.1)

if __name__=="__main__": unittest.main()
