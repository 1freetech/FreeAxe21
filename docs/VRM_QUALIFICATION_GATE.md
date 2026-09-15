# FREEAXE 21 VRM qualification gate

This gate applies to the shared FREEAXE 21 Air/Hydro electrical PCB and must be completed before schematic release or fabrication artifacts.

## Sourced constraints

- TPS546D24S: 40 A per device; 2x/3x/4x stackable with current sharing up to 160 A; 0.25-5.5 V output through PMBus; VOUT, IOUT and internal-die-temperature telemetry. Source: Texas Instruments TPS546D24S product/datasheet, checked 2026-09-15.
- Bitaxe Gamma Hex: six BM1370 ASICs arranged as two domains of three, ESP32-S3, 12 V input, four-phase TPS546D24S regulator with telemetry. Source: bitaxeorg/BitaxeGammaHex, checked 2026-09-15. This is architecture precedent only because it uses BM1370, not BM1373.

## FREEAXE 21 derived candidate

FREEAXE 21 retains two independently regulated four-BM1373 series domains. Each domain uses a two-device TPS546D24S stack. At the conservative 4.0 V domain rail, the existing analytical points are 31.5 A/domain at 252 W total VCORE-equivalent load, 50 A/domain at 400 W, and 60 A/domain at 480 W. The 60 A value is a provisional engineering ceiling equal to 75% of the 80 A two-device nameplate, not a guaranteed continuous capability.

## Required electrical qualification before schematic freeze

1. Select exact inductor MPN(s) and document inductance, DCR, saturation current, RMS/current-temperature rating, footprint and vendor availability.
2. Select switching frequency and calculate per-phase ripple current at 12 V input across the 4.0-5.0 V domain range.
3. Establish current-limit/OCP settings with margin above the intended sustained point and below component/copper damage limits.
4. Select output capacitor bank from the TI stability/compensation requirements; verify DC-bias derating, ripple-current capability and transient response.
5. Define the two-device stack configuration, SYNC/BCX/PMBus addressing and startup configuration from the TI reference requirements.
6. Route differential remote sense as a Kelvin pair to the domain load reference; do not sense at the regulator pads.
7. Validate the candidate 2 oz, two-layer-parallel VCORE geometry after actual routing, including via arrays, neck-downs and current crowding.
8. Bench-test each domain at 31.5 A and 50 A continuous and exercise the 60 A point only as a controlled stress qualification until thermal evidence supports otherwise.
9. Record regulator die temperature, inductor temperature, VCORE droop, input current, copper hot spots and PMBus-vs-independent-instrument error.
10. Prove four-BM1373 series-domain startup and steady-state voltage sharing before the architecture can be marked validated.

## Variant-specific thermal requirement

Air must demonstrate adequate forced airflow over both VRM stacks and inductors at its rated fan operating point. Hydro must not assume the ASIC cold plate cools the VRM; either provide a mechanically verified VRM cold-plate interface or a dedicated airflow path. Both variants use identical electrical current limits unless physical testing justifies a variant-specific lower limit.

## Release rule

Failure or absence of any item above keeps `schematic_complete`, `controlled_current_paths_validated`, and `thermal_mechanical_validation_complete` false in `manufacturing/readiness.json`. No production BOM, CPL, Gerber, drill or JLCPCB-ready claim is permitted from this analytical gate alone.
