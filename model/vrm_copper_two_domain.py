COPPER_RHO20 = 1.724e-8
ALPHA = 0.00393

def copper_resistance(length_mm, width_mm, thickness_um, layers=1, temp_c=20):
    if min(length_mm,width_mm,thickness_um,layers) <= 0:
        raise ValueError("geometry must be positive")
    rho = COPPER_RHO20 * (1 + ALPHA*(temp_c-20))
    area = width_mm*1e-3 * thickness_um*1e-6 * layers
    return rho*(length_mm*1e-3)/area

def path_metrics(current_a, **kwargs):
    r=copper_resistance(**kwargs)
    return {"resistance_mohm":r*1e3,
            "drop_mv":current_a*r*1e3,
            "loss_w":current_a*current_a*r}

def domain_current(total_core_w, domain_voltage_v, domains=2):
    if total_core_w < 0 or domain_voltage_v <= 0 or domains <= 0:
        raise ValueError("invalid power-domain inputs")
    return total_core_w/(domains*domain_voltage_v)

def stack_utilization(current_a, devices=2, per_device_a=40):
    return current_a/(devices*per_device_a)
