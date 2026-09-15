import unittest,pathlib,sys,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from model.air_thermal import *
class T(unittest.TestCase):
 def test_theta252(self): self.assertAlmostEqual(max_theta_sa(252,25,70),45/252)
 def test_theta400(self): self.assertAlmostEqual(max_theta_sa(400,25,70),0.1125)
 def test_bulk100(self): self.assertTrue(6.5<bulk_air_rise_c(400,100)<7.5)
 def test_run(self): self.assertEqual(air_state(True,True,60,80),"RUN")
 def test_base_throttle(self): self.assertEqual(air_state(True,True,65,80),"THROTTLE")
 def test_vrm_throttle(self): self.assertEqual(air_state(True,True,60,90),"THROTTLE")
 def test_fan_shutdown(self): self.assertEqual(air_state(False,True,40,50),"SHUTDOWN")
 def test_base_shutdown(self): self.assertEqual(air_state(True,True,70,50),"SHUTDOWN")
 def test_config_rule(self):
  c=json.loads((ROOT/"architecture/air_thermal.json").read_text())
  self.assertTrue(c["qualification"]["free_air_cfm_is_not_operating_airflow"])
if __name__=="__main__":unittest.main()
