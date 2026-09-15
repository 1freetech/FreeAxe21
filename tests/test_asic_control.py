import json, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.asic_control import *

class T(unittest.TestCase):
 def setUp(self):
  self.cfg=json.loads((ROOT/"architecture/asic_control.json").read_text())
 def test_config(self): self.assertTrue(validate_control_config(self.cfg))
 def test_eight_required(self): self.assertTrue(may_hash(8,1,1,1,1,1))
 def test_missing_chip_blocks(self): self.assertFalse(may_hash(7,1,1,1,1,1))
 def test_uart_blocks(self): self.assertFalse(may_hash(8,0,1,1,1,1))
 def test_cooling_blocks(self): self.assertFalse(may_hash(8,1,1,1,0,1))
 def test_power_blocks(self): self.assertFalse(may_hash(8,1,1,0,1,1))
 def test_reset_blocks(self): self.assertFalse(may_hash(8,1,1,1,1,0))
 def test_fault_latches(self):
  x=fault_action("FLOW_LOSS"); self.assertFalse(x["hashing"]); self.assertTrue(x["fault_latched"])
 def test_clock_unresolved(self): self.assertEqual(self.cfg["clock"]["status"],"UNRESOLVED_PHYSICAL")
if __name__=="__main__": unittest.main()
