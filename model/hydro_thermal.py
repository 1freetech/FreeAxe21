def coolant_delta_t_c(power_w, flow_lpm, cp=4180.0, density_kg_l=0.995):
    if power_w < 0 or flow_lpm <= 0: raise ValueError
    mdot = flow_lpm/60.0*density_kg_l
    return power_w/(mdot*cp)

def required_ua(power_w, mean_coolant_c, ambient_c):
    dt=mean_coolant_c-ambient_c
    if power_w < 0 or dt <= 0: raise ValueError
    return power_w/dt

def hydro_state(flow_lpm,pump_tach_ok,outlet_c,sensors_ok=True):
    if not sensors_ok or not pump_tach_ok or flow_lpm < 0.5 or outlet_c >= 45: return "SHUTDOWN"
    if flow_lpm < 1.0: return "THROTTLE"
    return "RUN"
