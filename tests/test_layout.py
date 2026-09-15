import json, pathlib, sys, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.layout import *
CFG=json.loads((ROOT/'layout/board_layout.json').read_text())
class LayoutRun13Tests(unittest.TestCase):
    def test_board_retained(self):
        self.assertEqual((CFG['board']['width_mm'],CFG['board']['height_mm']),(180.0,120.0))
    def test_two_domains_four_each(self):
        self.assertEqual(CFG['shared']['domain_count'],2)
        self.assertEqual([sum(a['domain']==d for a in CFG['asics']) for d in ['A','B']],[4,4])
    def test_domain_rows_are_contiguous(self):
        for d in ['A','B']:
            row=sorted(a['x_mm'] for a in CFG['asics'] if a['domain']==d)
            self.assertEqual([round(row[i+1]-row[i],3) for i in range(3)],[16.0,16.0,16.0])
    def test_cluster_envelope(self):
        env=asic_envelope(CFG['asics'],CFG['shared']['asic_package_nominal_mm'])
        self.assertEqual(envelope_size(env),(58.0,26.0))
    def test_contact_covers_cluster(self):
        env=asic_envelope(CFG['asics'],CFG['shared']['asic_package_nominal_mm'])
        x,y,w,h=CFG['shared']['cooling_contact_rect_mm']
        self.assertLessEqual(x,env[0]); self.assertLessEqual(y,env[1])
        self.assertGreaterEqual(x+w,env[2]); self.assertGreaterEqual(y+h,env[3])
    def test_vrms_outside_contact(self):
        x,y,w,h=CFG['shared']['cooling_contact_rect_mm']
        c={'x_mm':x,'y_mm':y,'w_mm':w,'h_mm':h}
        self.assertFalse(overlaps(CFG['zones']['domain_a_vrm_pair'],c))
        self.assertFalse(overlaps(CFG['zones']['domain_b_vrm_pair'],c))
    def test_vrm_to_row_gap_is_short(self):
        self.assertLessEqual(minimum_vrm_to_asic_edge_gap(CFG,'A'),15.0)
        self.assertLessEqual(minimum_vrm_to_asic_edge_gap(CFG,'B'),15.0)
        self.assertGreaterEqual(minimum_vrm_to_asic_edge_gap(CFG,'A'),5.0)
        self.assertGreaterEqual(minimum_vrm_to_asic_edge_gap(CFG,'B'),5.0)
    def test_cooler_mount_pitch(self):
        self.assertEqual(cooler_hole_pitch(CFG['cooler_mount_holes']),(75.0,75.0))
    def test_mount_holes_inside_edge_keepout(self):
        b=CFG['board']; m=b['edge_keepout_mm']
        self.assertTrue(all(point_inside_board(x,y,b,m) for x,y in CFG['cooler_mount_holes']))
    def test_common_variant_coordinates(self):
        self.assertTrue(CFG['variants']['air']['shared_pcb'])
        self.assertTrue(CFG['variants']['hydro']['shared_pcb'])
    def test_old_four_vrm_zones_removed(self):
        self.assertFalse(any(k in CFG['zones'] for k in ['vrm_1','vrm_2','vrm_3','vrm_4']))
if __name__=='__main__': unittest.main()
