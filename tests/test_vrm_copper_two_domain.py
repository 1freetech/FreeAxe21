import pathlib,sys,unittest,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.vrm_copper_two_domain import *

class TestRun15(unittest.TestCase):
    def test_reference_current(self):
        self.assertAlmostEqual(domain_current(252,4.0),31.5)
    def test_400w_current(self):
        self.assertAlmostEqual(domain_current(400,4.0),50.0)
    def test_480w_current(self):
        self.assertAlmostEqual(domain_current(480,4.0),60.0)
    def test_stack_utilization_400w(self):
        self.assertAlmostEqual(stack_utilization(50),0.625)
    def test_stack_utilization_stress(self):
        self.assertAlmostEqual(stack_utilization(60),0.75)
    def test_copper_at_80c(self):
        m=path_metrics(50,length_mm=15,width_mm=20,thickness_um=70,layers=2,temp_c=80)
        self.assertLess(m["drop_mv"],10)
        self.assertLess(m["loss_w"],0.6)
    def test_single_layer_rejected(self):
        two=path_metrics(50,length_mm=15,width_mm=20,thickness_um=70,layers=2,temp_c=80)
        one=path_metrics(50,length_mm=15,width_mm=20,thickness_um=70,layers=1,temp_c=80)
        self.assertGreater(one["drop_mv"],two["drop_mv"])
        self.assertGreater(one["loss_w"],two["loss_w"])
    def test_release_blocked(self):
        cfg=json.loads((ROOT/"architecture/vrm_copper_two_domain.json").read_text())
        self.assertTrue(cfg["limits"]["no_manufacturing_release"])
        self.assertTrue(cfg["open_items"])
if __name__=="__main__": unittest.main()
