import unittest, pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from model.hydro_thermal import *
class T(unittest.TestCase):
 def test_252(self): self.assertTrue(2.3<coolant_delta_t_c(252,1.5)<2.6)
 def test_400(self): self.assertTrue(3.7<coolant_delta_t_c(400,1.5)<4.0)
 def test_480(self): self.assertTrue(4.5<coolant_delta_t_c(480,1.5)<4.8)
 def test_ua(self): self.assertEqual(required_ua(400,35,25),40)
 def test_run(self): self.assertEqual(hydro_state(1.5,True,34),"RUN")
 def test_throttle(self): self.assertEqual(hydro_state(.75,True,34),"THROTTLE")
 def test_flow_shutdown(self): self.assertEqual(hydro_state(.49,True,34),"SHUTDOWN")
 def test_tach_shutdown(self): self.assertEqual(hydro_state(1.5,False,34),"SHUTDOWN")
 def test_temp_shutdown(self): self.assertEqual(hydro_state(1.5,True,45),"SHUTDOWN")
if __name__=="__main__": unittest.main()
