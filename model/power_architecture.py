"""Structural validator for the FREEAXE 21 candidate power-domain architecture."""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DEFAULT_ARCH = HERE / "architecture" / "power_domains.json"


def load_architecture(path: Path = DEFAULT_ARCH) -> dict:
    return json.loads(path.read_text())


def validate_architecture(arch: dict) -> list[str]:
    errors: list[str] = []
    asic = arch.get("asic", {})
    topo = arch.get("candidate_core_topology", {})
    count = asic.get("count")
    domains = topo.get("domains", [])
    series_per_domain = topo.get("series_asics_per_domain")
    domain_count = topo.get("voltage_domain_count")

    if count != 8:
        errors.append("FREEAXE 21 architecture must currently contain exactly 8 BM1373 ASICs")
    if asic.get("model") != "BM1373":
        errors.append("ASIC model must be BM1373")
    if domain_count != 2 or len(domains) != 2:
        errors.append("candidate architecture requires two voltage domains")
    if series_per_domain != 4:
        errors.append("candidate architecture requires four series ASICs per domain")

    members = [u for d in domains for u in d.get("asics", [])]
    expected = [f"U{i}" for i in range(1, 9)]
    if sorted(members) != sorted(expected):
        errors.append("domains must cover U1..U8 exactly once")
    if len(members) != len(set(members)):
        errors.append("an ASIC appears in more than one power domain")

    regulator = topo.get("regulator", {})
    if regulator.get("part") != "TPS546D24S":
        errors.append("candidate regulator must be TPS546D24S")
    if regulator.get("devices_per_domain") != 2:
        errors.append("candidate architecture requires two stacked regulator devices per domain")
    if any(len(d.get("regulator_stack", [])) != 2 for d in domains):
        errors.append("each domain must map to two stacked regulator devices")

    if arch.get("input", {}).get("nominal_voltage_v") != 12.0:
        errors.append("current shared architecture requires nominal 12 V input")

    hydro = arch.get("variant_delta", {}).get("Hydro", {})
    if "loss_of_flow" not in hydro.get("hard_interlock", ""):
        errors.append("Hydro variant must explicitly hard-interlock on loss of flow")
    return errors


def domain_map(arch: dict) -> dict[str, str]:
    return {u: d["id"] for d in arch["candidate_core_topology"]["domains"] for u in d["asics"]}
