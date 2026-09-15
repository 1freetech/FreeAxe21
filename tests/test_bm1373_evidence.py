import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.bm1373_evidence import *

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.nexus = SystemEvidence('Nexus S1 prototype', 4, 10.3, 140.0,
                                    EvidenceTier.INDEPENDENT_MEASURED_SYSTEM, 15)
        self.nmaxe = SystemEvidence('NMAxe BM1373 driver test', 1, 6.0, None,
                                    EvidenceTier.OPEN_FIRMWARE_CLAIM, None)

    def test_nexus_per_chip(self):
        self.assertAlmostEqual(self.nexus.per_chip_ths, 2.575, places=6)

    def test_nexus_efficiency(self):
        self.assertAlmostEqual(self.nexus.wall_j_per_th, 13.592233, places=5)

    def test_eight_chip_linearization(self):
        p = linearize(self.nexus, 8)
        self.assertAlmostEqual(p['hashrate_ths'], 20.6, places=6)
        self.assertAlmostEqual(p['wall_w'], 280.0, places=6)

    def test_nmaxe_6ths_is_not_power_qualified(self):
        p = linearize(self.nmaxe, 8)
        self.assertAlmostEqual(p['hashrate_ths'], 48.0, places=6)
        self.assertNotIn('wall_w', p)
        self.assertEqual(p['source_tier'], 'OPEN_FIRMWARE_CLAIM')

    def test_sustained_ceiling_stays_at_measured_anchor_without_freeaxe_data(self):
        self.assertEqual(sustained_design_ceiling(independent_measured_ths_8chip=20.6), 20.6)

    def test_freeaxe_measurement_can_raise_ceiling_later(self):
        self.assertEqual(sustained_design_ceiling(independent_measured_ths_8chip=20.6,
                                                  freeaxe_measured_ths=23.0), 23.0)

if __name__ == '__main__':
    unittest.main()
