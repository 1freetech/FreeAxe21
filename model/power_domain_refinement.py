from dataclasses import dataclass

@dataclass(frozen=True)
class DomainSizing:
    total_power_w: float
    domains: int
    series_chips: int
    per_chip_v: float
    domain_v: float
    power_per_domain_w: float
    current_per_domain_a: float
    stack_capacity_a: float
    utilization: float


def size_domains(total_power_w: float, *, domains: int = 2,
                 series_chips: int = 4, per_chip_v: float = 1.0,
                 regulator_devices_per_domain: int = 2,
                 regulator_current_per_device_a: float = 40.0) -> DomainSizing:
    if total_power_w <= 0 or domains <= 0 or series_chips <= 0 or per_chip_v <= 0:
        raise ValueError("power, domain count, series chip count and voltage must be positive")
    domain_v = series_chips * per_chip_v
    power_per_domain = total_power_w / domains
    current = power_per_domain / domain_v
    capacity = regulator_devices_per_domain * regulator_current_per_device_a
    return DomainSizing(total_power_w, domains, series_chips, per_chip_v, domain_v,
                        power_per_domain, current, capacity, current / capacity)


def domain_voltage_range(series_chips: int, chip_voltages_mv: list[int]) -> tuple[float, float]:
    if series_chips <= 0 or not chip_voltages_mv:
        raise ValueError("invalid input")
    volts = [series_chips * mv / 1000.0 for mv in chip_voltages_mv]
    return min(volts), max(volts)


def topology_valid_for_regulator(*, series_chips: int, chip_voltages_mv: list[int],
                                 regulator_vout_max_v: float) -> bool:
    _, vmax = domain_voltage_range(series_chips, chip_voltages_mv)
    return vmax <= regulator_vout_max_v
