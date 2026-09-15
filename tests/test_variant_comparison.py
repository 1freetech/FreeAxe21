import unittest,pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from model.variant_comparison import *
class T(unittest.TestCase):
 def test_air_low(self): self.assertAlmostEqual(power_from_eff(20,9.55),191)
 def test_air_high(self): self.assertEqual(power_from_eff(20,13),260)
 def test_hydro_low(self): self.assertAlmostEqual(power_from_eff(20.6,9.55),196.73)
 def test_hydro_high(self): self.assertAlmostEqual(power_from_eff(20.6,13),267.8)
 def test_30_13(self): self.assertEqual(power_from_eff(30,13),390)
 def test_30_15_exceeds(self): self.assertGreater(power_from_eff(30,15),400)
 def test_air_margin(self): self.assertEqual(thermal_headroom(400,260),140)
 def test_hydro_margin(self): self.assertAlmostEqual(thermal_headroom(400,267.8),132.2)
 def test_not_release(self):
  c=json.loads((ROOT/"architecture/variant_comparison.json").read_text())
  self.assertTrue(c["release_blockers"])
if __name__=="__main__":unittest.main()
