"""FREEAXE 21 dependency-5 output-capacitor qualification calculations.

Equations mirror the TPS546D24S datasheet design procedure, but FREEAXE
inputs are analytical assumptions rather than measured load-transient data.
No capacitor BOM is selected by this model.
"""
import math


def transient_capacitance_f(transient_a, inductance_h, vout_v, allowed_overshoot_v):
    if min(transient_a, inductance_h, vout_v, allowed_overshoot_v) <= 0:
        raise ValueError("inputs must be positive")
    return transient_a**2 * inductance_h / (vout_v * allowed_overshoot_v)


def bandwidth_capacitance_f(transient_a, allowed_transient_v, switching_hz):
    if min(transient_a, allowed_transient_v, switching_hz) <= 0:
        raise ValueError("inputs must be positive")
    bandwidth_hz = switching_hz / 10.0
    return 1.0 / (2.0 * math.pi * bandwidth_hz * (allowed_transient_v / transient_a))


def ripple_capacitance_f(inductor_ripple_a, switching_hz, allowed_ripple_v):
    if min(inductor_ripple_a, switching_hz, allowed_ripple_v) <= 0:
        raise ValueError("inputs must be positive")
    return inductor_ripple_a / (8.0 * switching_hz * allowed_ripple_v)


def qualification_window(transient_a_values=(10.0, 20.0, 25.0), inductance_uh=0.68,
                         vout_v=4.0, switching_khz=600.0,
                         allowed_transient_v=0.10, allowed_ripple_v=0.020,
                         inductor_ripple_a=6.536):
    rows=[]
    for transient_a in transient_a_values:
        c_tr=transient_capacitance_f(transient_a,inductance_uh*1e-6,vout_v,allowed_transient_v)
        c_bw=bandwidth_capacitance_f(transient_a,allowed_transient_v,switching_khz*1e3)
        rows.append({"transient_a":transient_a,"transient_min_uf":round(c_tr*1e6,1),
                     "bandwidth_min_uf":round(c_bw*1e6,1),
                     "governing_min_uf":round(max(c_tr,c_bw)*1e6,1)})
    c_r=ripple_capacitance_f(inductor_ripple_a,switching_khz*1e3,allowed_ripple_v)
    return {"assumptions":{"inductance_uh":inductance_uh,"vout_v":vout_v,
             "switching_khz":switching_khz,"allowed_transient_v":allowed_transient_v,
             "allowed_ripple_v":allowed_ripple_v,"inductor_ripple_a":inductor_ripple_a},
            "transient_rows":rows,"ripple_min_uf":round(c_r*1e6,1)}
