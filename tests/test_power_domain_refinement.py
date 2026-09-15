import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.power_domain_refinement import size_domains, domain_voltage_range, topology_valid_for_regulator


def test_four_chip_voltage_range_fits_tps546d24s():
    vrange = domain_voltage_range(4, [1000,1060,1100,1150,1200,1250])
    assert vrange == (4.0, 5.0)
    assert topology_valid_for_regulator(series_chips=4,
        chip_voltages_mv=[1000,1060,1100,1150,1200,1250], regulator_vout_max_v=5.5)


def test_corrected_anchor_current_is_low_relative_to_stack():
    p = size_domains(252.0, per_chip_v=1.0)
    assert p.domain_v == 4.0
    assert p.current_per_domain_a == 31.5
    assert abs(p.utilization - 0.39375) < 1e-9


def test_400w_envelope_still_has_current_headroom():
    p = size_domains(400.0, per_chip_v=1.0)
    assert p.current_per_domain_a == 50.0
    assert p.utilization == 0.625


def test_480w_sensitivity_stays_below_75_percent_or_equal():
    p = size_domains(480.0, per_chip_v=1.0)
    assert p.current_per_domain_a == 60.0
    assert p.utilization == 0.75


def test_architecture_has_two_domains_and_four_vrms_total():
    cfg = json.loads((ROOT/'architecture/power_domains.json').read_text())
    t = cfg['candidate_core_topology']
    assert t['voltage_domain_count'] == 2
    assert t['series_asics_per_domain'] == 4
    assert sum(len(d['regulator_stack']) for d in t['domains']) == 4
    assert all(len(d['asics']) == 4 for d in t['domains'])


def test_four_chip_domain_is_explicitly_unvalidated():
    cfg = json.loads((ROOT/'architecture/power_domains.json').read_text())
    gates = ' '.join(cfg['candidate_core_topology']['hard_validation_gates']).lower()
    assert 'four-asic series-domain' in gates
    assert 'proven on hardware' in gates
