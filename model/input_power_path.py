from dataclasses import dataclass


@dataclass(frozen=True)
class InputPathResult:
    total_current_a: float
    current_per_positive_contact_a: float
    current_per_return_contact_a: float
    power_w: float
    harness_drop_v: float
    harness_loss_w: float


@dataclass(frozen=True)
class TwoBranchResult:
    total_current_a: float
    branch_current_a: float
    auxiliary_current_a: float
    connector_current_a: float


def current_for_power(power_w: float, voltage_v: float) -> float:
    if power_w < 0:
        raise ValueError("power_w cannot be negative")
    if voltage_v <= 0:
        raise ValueError("voltage_v must be positive")
    return power_w / voltage_v


def evaluate_input_path(
    voltage_v: float,
    current_a: float,
    positive_contacts: int = 2,
    return_contacts: int = 2,
    harness_loop_resistance_ohm: float = 0.0066,
) -> InputPathResult:
    """Evaluate the shared FREEAXE21 12 V connector/harness path.

    The default 6.6 mOhm loop is a sensitivity value only, not a released
    harness-resistance or ampacity claim.
    """
    if voltage_v <= 0:
        raise ValueError("voltage must be positive")
    if current_a < 0:
        raise ValueError("current cannot be negative")
    if positive_contacts < 1 or return_contacts < 1:
        raise ValueError("at least one positive and one return contact are required")
    if harness_loop_resistance_ohm < 0:
        raise ValueError("harness resistance cannot be negative")

    drop_v = current_a * harness_loop_resistance_ohm
    loss_w = current_a * current_a * harness_loop_resistance_ohm
    return InputPathResult(
        total_current_a=current_a,
        current_per_positive_contact_a=current_a / positive_contacts,
        current_per_return_contact_a=current_a / return_contacts,
        power_w=voltage_v * current_a,
        harness_drop_v=drop_v,
        harness_loss_w=loss_w,
    )


def split_two_domain_input(core_power_w: float, voltage_v: float, auxiliary_current_a: float = 0.0) -> TwoBranchResult:
    """Split input-side core power equally between the two VRM domains.

    This is an architecture/load-allocation model. It does not predict regulator
    conversion efficiency or individual ASIC power.
    """
    if auxiliary_current_a < 0:
        raise ValueError("auxiliary_current_a cannot be negative")
    total_core_current = current_for_power(core_power_w, voltage_v)
    branch_current = total_core_current / 2.0
    return TwoBranchResult(
        total_current_a=total_core_current,
        branch_current_a=branch_current,
        auxiliary_current_a=auxiliary_current_a,
        connector_current_a=total_core_current + auxiliary_current_a,
    )


def validate_contact_margin(
    total_current_a: float,
    positive_contacts: int,
    family_rating_a_per_contact: float,
    design_derating: float = 0.90,
) -> bool:
    if total_current_a < 0:
        raise ValueError("total_current_a cannot be negative")
    if not 0 < design_derating <= 1:
        raise ValueError("design_derating must be in (0, 1]")
    if positive_contacts < 1:
        raise ValueError("positive_contacts must be >= 1")
    allowed = family_rating_a_per_contact * design_derating
    return (total_current_a / positive_contacts) <= allowed


def fuse_allowed_current_a(fuse_ambient_c: float) -> float:
    """Linear interpolation of the published *typical* JCASE 60 A derating table.

    This is for design screening only; it does not replace Littelfuse time-current
    coordination or thermal qualification in the final holder/PCB environment.
    """
    points = [(-40.0, 60.0), (0.0, 60.0), (20.0, 60.0), (65.0, 51.0),
              (85.0, 46.0), (110.0, 38.0), (125.0, 33.0)]
    if fuse_ambient_c < points[0][0] or fuse_ambient_c > points[-1][0]:
        raise ValueError("fuse_ambient_c outside published screening table")
    for (t0, i0), (t1, i1) in zip(points, points[1:]):
        if t0 <= fuse_ambient_c <= t1:
            if t1 == t0:
                return i0
            frac = (fuse_ambient_c - t0) / (t1 - t0)
            return i0 + frac * (i1 - i0)
    return points[-1][1]
