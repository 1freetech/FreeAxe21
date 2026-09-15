# FREEAXE 21 VRM reference boundary

Status: engineering constraint, not fabrication release.

## What is sourced

Texas Instruments specifies TPS546D24S as a 40 A synchronous buck converter with 2x/3x/4x stacking and current sharing up to 160 A. It supports differential remote sense, PMBus VOUT/IOUT/die-temperature telemetry, selectable internal compensation, and twelve selectable switching frequencies from 225 kHz to 1.5 MHz.

TI reference design PMP21254 is a tested high-current ASIC/FPGA core supply using four TPS546D24A 40 A phases from a 6-13.2 V input to 1.2 V / 160 A. It establishes useful precedent for stacked D24-family converters on high-current ASIC rails, but it does not validate FREEAXE's 4.0 V domain rail, BM1373 load dynamics, magnetics, compensation, or PCB geometry.

## FREEAXE 21 derived architecture

FREEAXE 21 Air and Hydro retain two four-BM1373 voltage domains. Each domain presently allocates two TPS546D24S devices. The resulting 80 A/domain device nameplate is not a continuous FREEAXE rating.

The current model keeps:

- 31.5 A/domain at the historical 252 W board reference.
- 50 A/domain at the 400 W thermal qualification envelope.
- 60 A/domain only as a controlled electrical stress point.

The provisional 60 A engineering ceiling is therefore 75% of the two-device 80 A nameplate. It remains conditional on magnetics, switching losses, regulator temperature, capacitor ripple/transients, current sharing, and routed-copper validation.

## Important correction to the design process

Do not select an inductor value or switching frequency by copying a TI reference design. PMP21254 is a 1.2 V / 160 A design and FREEAXE's current behavioral model uses approximately 4.0 V per four-chip domain. The required duty cycle and inductor ripple are materially different. Final L, DCR, saturation-current, frequency, compensation, and capacitor values must be calculated together for the actual FREEAXE rail and then bench validated.

Likewise, the existing 15 mm, two-layer, 20 mm-per-layer, 2 oz VCORE copper candidate remains a bulk-resistance sensitivity calculation only. It does not account for neck-downs, via constriction, spreading resistance, pads, current crowding, copper tolerance, or local thermal coupling.

## Dependency-5 exit criteria

Dependency 5 cannot close until all of the following exist:

1. Exact inductor MPN with L, DCR, Isat/Irms and temperature-rise evidence at the chosen frequency.
2. Chosen TPS546D24S switching frequency and phase relationship.
3. Ripple-current calculation at input-voltage and output-voltage corners.
4. Output capacitor bank and transient/compensation validation.
5. PMBus/OCP limits and fault response for each two-device domain.
6. Differential remote-sense routing defined at the ASIC-domain load point.
7. Exact PCB stackup, copper weights, routed polygons and via arrays.
8. Current-sharing and thermal test at the expected operating point plus 50 A qualification point.
9. Controlled 60 A stress test only if component thermal margins support it.
10. Four-BM1373 domain startup, voltage-sharing and accepted-share stability testing.

Until these gates pass, the VRM architecture is a candidate design and FREEAXE 21 remains not ready for fabrication.
