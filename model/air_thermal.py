def max_theta_sa(power_w, ambient_c, base_limit_c):
    if power_w <= 0 or base_limit_c <= ambient_c: raise ValueError
    return (base_limit_c-ambient_c)/power_w

def bulk_air_rise_c(power_w, actual_cfm, rho=1.184, cp=1007.0):
    if power_w < 0 or actual_cfm <= 0: raise ValueError
    mdot=actual_cfm*0.00047194745*rho
    return power_w/(mdot*cp)

def air_state(fan_tach_ok,sensors_ok,base_c,vrm_c):
    if not fan_tach_ok or not sensors_ok or base_c >= 70 or vrm_c >= 100: return "SHUTDOWN"
    if base_c >= 65 or vrm_c >= 90: return "THROTTLE"
    return "RUN"
