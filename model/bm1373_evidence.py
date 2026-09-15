from dataclasses import dataclass
from enum import IntEnum

class EvidenceTier(IntEnum):
    SPECULATIVE = 1
    OPEN_FIRMWARE_CLAIM = 2
    INDEPENDENT_MEASURED_SYSTEM = 3
    FREEAXE_MEASURED = 4

@dataclass(frozen=True)
class SystemEvidence:
    name: str
    chips: int
    hashrate_ths: float
    wall_w: float | None
    tier: EvidenceTier
    sustained_minutes: float | None = None

    @property
    def per_chip_ths(self) -> float:
        if self.chips <= 0 or self.hashrate_ths <= 0:
            raise ValueError('positive chip count and hashrate required')
        return self.hashrate_ths / self.chips

    @property
    def wall_j_per_th(self) -> float | None:
        if self.wall_w is None:
            return None
        if self.wall_w <= 0:
            raise ValueError('wall power must be positive when present')
        return self.wall_w / self.hashrate_ths


def linearize(evidence: SystemEvidence, target_chips: int) -> dict:
    if target_chips <= 0:
        raise ValueError('target_chips must be positive')
    scale = target_chips / evidence.chips
    out = {
        'hashrate_ths': evidence.hashrate_ths * scale,
        'classification': 'derived linearization; not a FREEAXE measurement',
        'source_tier': evidence.tier.name,
    }
    if evidence.wall_w is not None:
        out['wall_w'] = evidence.wall_w * scale
        out['wall_j_per_th'] = evidence.wall_j_per_th
    return out


def sustained_design_ceiling(*, independent_measured_ths_8chip: float,
                             freeaxe_measured_ths: float | None = None) -> float:
    """Do not promote undocumented short-duration overclock claims into a sustained rating."""
    if independent_measured_ths_8chip <= 0:
        raise ValueError('measured anchor must be positive')
    if freeaxe_measured_ths is not None:
        if freeaxe_measured_ths <= 0:
            raise ValueError('FREEAXE measured point must be positive')
        return max(independent_measured_ths_8chip, freeaxe_measured_ths)
    return independent_measured_ths_8chip
