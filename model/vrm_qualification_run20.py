"""FREEAXE 21 dependency-5 VRM qualification calculations.

Behavioral/analytical only. This does not select a production inductor or
compensation network and does not make the board fabrication-ready.
"""


def buck_inductor_ripple_a(vin_v, vout_v, inductance_h, switching_hz):
    if not (vin_v > vout_v > 0 and inductance_h > 0 and switching_hz > 0):
        raise ValueError("invalid buck inputs")
    duty = vout_v / vin_v
    return (vin_v - vout_v) * duty / (inductance_h * switching_hz)


def per_phase_metrics(domain_current_a, phases, ripple_pp_a):
    if domain_current_a < 0 or phases <= 0 or ripple_pp_a < 0:
        raise ValueError("invalid phase inputs")
    avg = domain_current_a / phases
    peak = avg + ripple_pp_a / 2
    rms = (avg * avg + ripple_pp_a * ripple_pp_a / 12) ** 0.5
    return {"avg_a": avg, "peak_a": peak, "rms_a": rms}


def candidate_sweep(vin_v=12.0, vout_v=4.0, domain_current_a=50.0, phases=2):
    rows=[]
    for inductance_uh in (0.47, 0.68, 1.0):
        for switching_khz in (400, 600, 800):
            ripple=buck_inductor_ripple_a(vin_v,vout_v,inductance_uh*1e-6,switching_khz*1e3)
            m=per_phase_metrics(domain_current_a,phases,ripple)
            rows.append({"inductance_uh":inductance_uh,"switching_khz":switching_khz,
                         "ripple_pp_a":round(ripple,3),"ripple_pct_phase_avg":round(100*ripple/m["avg_a"],1),
                         "phase_peak_a":round(m["peak_a"],3),"phase_rms_a":round(m["rms_a"],3)})
    return rows
