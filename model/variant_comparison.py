def power_from_eff(hashrate_th_s, efficiency_j_th):
    return hashrate_th_s*efficiency_j_th
def thermal_headroom(envelope_w, modeled_w):
    return envelope_w-modeled_w
def current_12v(power_w, efficiency=0.95):
    return power_w/(12*efficiency)
