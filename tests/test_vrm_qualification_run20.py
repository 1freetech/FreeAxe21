import unittest
from model.vrm_qualification_run20 import buck_inductor_ripple_a, per_phase_metrics, candidate_sweep


class TestVRMQualificationRun20(unittest.TestCase):
    def test_known_ripple(self):
        self.assertAlmostEqual(buck_inductor_ripple_a(12,4,0.68e-6,600e3),26.1437908,places=5)

    def test_50a_two_phase_average(self):
        m=per_phase_metrics(50,2,10)
        self.assertEqual(m["avg_a"],25)
        self.assertEqual(m["peak_a"],30)

    def test_rms_above_average(self):
        m=per_phase_metrics(50,2,10)
        self.assertGreater(m["rms_a"],m["avg_a"])

    def test_sweep_has_nine_points(self):
        self.assertEqual(len(candidate_sweep()),9)

    def test_higher_frequency_reduces_ripple(self):
        rows=candidate_sweep()
        r400=next(r for r in rows if r["inductance_uh"]==0.68 and r["switching_khz"]==400)
        r800=next(r for r in rows if r["inductance_uh"]==0.68 and r["switching_khz"]==800)
        self.assertLess(r800["ripple_pp_a"],r400["ripple_pp_a"])

    def test_larger_inductance_reduces_ripple(self):
        rows=candidate_sweep()
        r047=next(r for r in rows if r["inductance_uh"]==0.47 and r["switching_khz"]==600)
        r100=next(r for r in rows if r["inductance_uh"]==1.0 and r["switching_khz"]==600)
        self.assertLess(r100["ripple_pp_a"],r047["ripple_pp_a"])

    def test_bad_buck_inputs(self):
        with self.assertRaises(ValueError): buck_inductor_ripple_a(4,4,1e-6,600e3)


if __name__ == "__main__": unittest.main()
