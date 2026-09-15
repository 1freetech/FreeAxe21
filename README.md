# FREEAXE 21

FREEAXE 21 is an open engineering project for an eight-BM1373 Bitcoin miner with two cooling variants built on the same electrical PCB:

- **FREEAXE 21 Air** — target: ~20 TH/s sustained certification.
- **FREEAXE 21 Hydro** — current design estimate: ~20.6 TH/s, with higher points treated as experimental until measured.

The current architecture uses eight BM1373 ASICs, two four-chip voltage domains, an ESP32-S3-class controller, ESP-Miner/AxeOS-compatible control assumptions, 12 V input, and separate Air/Hydro thermal hardware.

## Current evidence-based performance window

Public BM1373 references place the useful design region around roughly 9.55–13 J/TH for ~20 TH/s-class operation. FREEAXE 21 has **not** yet been physically measured, so all FREEAXE hashrate, power and temperature values in this repository are engineering targets or derived models unless explicitly labeled otherwise.

## Repository structure

- `architecture/` — machine-readable electrical, control, thermal and comparison definitions.
- `model/` — reduced-order engineering calculations.
- `tests/` — deterministic validation of the current models and safety gates.
- `layout/` — current board placement geometry and SVG visualization.
- `docs/` — design notes and assumptions.
- `manufacturing/` — release-readiness gate and BOM skeleton.
- `scripts/` — release checks.

## Manufacturing status

**NOT production-ready and NOT JLCPCB-ready.** Manufacturing remains blocked until the actual schematic, routing, ERC/DRC, exact stackup, current-density, thermal/mechanical, BOM/CPL, Gerber/drill and fabrication checks are complete.

## Current major blockers

1. Validate four-BM1373 series-domain startup and voltage sharing.
2. Validate level shifting across the voltage-domain boundary.
3. Lock the physical BM1373 reference-clock implementation from validated hardware evidence.
4. Complete exact regulator magnetics/capacitors/compensation and transient validation.
5. Measure prototype board power, accepted-share stability, ASIC/VRM temperatures and long-duration behavior.
6. Validate Air fan/heatsink operating point and Hydro pump/pressure-drop/radiator operating point.

## Naming

The model name is **FREEAXE 21**. The “21” is the product/model identity; it does not mean that 21 TH/s is a guaranteed sustained rating.
