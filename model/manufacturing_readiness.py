import json
from pathlib import Path

REQUIRED_FAB_GATES = (
    "schematic_complete",
    "schematic_erc_zero_unresolved_errors",
    "footprints_verified",
    "pcb_routing_complete",
    "pcb_drc_zero_unresolved_errors",
    "stackup_selected",
    "controlled_current_paths_validated",
    "thermal_mechanical_validation_complete",
    "bom_complete_with_manufacturer_part_numbers",
    "cpl_generated_from_routed_board",
    "gerbers_generated_from_routed_board",
    "drill_files_generated_from_routed_board",
    "fabrication_output_review_complete",
)

def load_readiness(path: str | Path):
    return json.loads(Path(path).read_text())

def missing_gates(doc):
    gates = doc["required_gates"]
    missing = [g for g in REQUIRED_FAB_GATES if gates.get(g) is not True]
    return missing

def fabrication_ready(doc):
    return not missing_gates(doc)

def assert_no_false_release(doc):
    ready = fabrication_ready(doc)
    status = doc.get("status")
    blocked = set(doc.get("blocked_outputs", []))
    if not ready:
        if status == "READY_FOR_FABRICATION":
            raise AssertionError("false READY_FOR_FABRICATION status")
        for required in {"Gerber", "Excellon drill", "CPL/position", "production BOM", "JLCPCB-ready package"}:
            if required not in blocked:
                raise AssertionError(f"missing blocked output marker: {required}")
    return True
