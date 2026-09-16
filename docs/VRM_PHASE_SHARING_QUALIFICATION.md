# FREEAXE 21 VRM phase-sharing qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro board. It defines how the two stacked TPS546D24S converters in each four-BM1373 VCORE domain must be qualified for current sharing before the electrical design can be frozen.

## Evidence boundary

Texas Instruments specifies TPS546D24S as a 40 A synchronous buck converter that can be stacked 2x, 3x, or 4x with current sharing and a single PMBus address per output. It also provides VOUT, IOUT, and die-temperature telemetry, differential remote sense, adjustable current limit, phase interleaving, and configurable fault response. These are device capabilities, not proof that the FREEAXE layout shares current acceptably.

TI reference design PMP21254 demonstrates four stacked devices supplying a high-current ASIC/FPGA core rail and is useful evidence that the architecture is practical. FREEAXE still requires its own validation because its output voltage, magnetics, capacitor network, PCB geometry, cooling, and ASIC load spectrum differ.

## Shared-domain qualification points

Each four-BM1373 domain retains these total-load points:

- 31.5 A/domain reference: ideal two-phase average is 15.75 A per phase.
- 50 A/domain continuous qualification: ideal two-phase average is 25.0 A per phase.
- 60 A/domain controlled stress only: ideal two-phase average is 30.0 A per phase.
- 80 A/domain is only the sum of two 40 A regulator nameplates and is not an operating target.

The Air and Hydro variants use the same electrical phase-sharing requirement. Better ASIC cooling in Hydro does not justify allowing one regulator phase to run overloaded.

## Provisional acceptance window

Until hardware characterization supports a tighter limit, use a conservative engineering gate of **no more than 10% phase-current imbalance relative to the ideal half-domain current at thermal equilibrium** at the 31.5 A and 50 A domain points.

That means the provisional absolute difference from ideal for either phase is:

- 31.5 A/domain: each phase should remain within 15.75 A ± 1.575 A.
- 50 A/domain: each phase should remain within 25.0 A ± 2.5 A.

This 10% window is a FREEAXE engineering requirement, not a claimed TPS546D24S datasheet specification. It must be revisited after real measurement uncertainty and TI current-sharing behavior are characterized. A board also fails if either phase violates component thermal limits even while current imbalance remains inside the window.

## Measurement requirements

At minimum, prototype qualification must record:

1. Total domain current using an independent calibrated instrument.
2. Per-phase current from PMBus telemetry where exposed by the stacked configuration, cross-checked against an independent measurement method during development.
3. Regulator die temperature from PMBus plus external package/board temperature measurement.
4. Inductor temperature for each phase.
5. VCORE_SOURCE and VCORE_LOAD voltage so current-sharing results are not confused with excessive distribution loss.
6. Measurements after thermal equilibrium at 31.5 A and 50 A/domain, repeated in both Air and Hydro mechanical assemblies.
7. Startup, load-step, unload-step, and fault/retry behavior to confirm one phase does not transiently carry an unsafe share of the domain load.

If direct independent per-phase current measurement cannot be implemented without disturbing the switching path, the prototype must provide a justified correlation method using characterized inductor DCR/current sensing or another suitable technique. PMBus telemetry alone is not accepted as the sole validation instrument.

## Layout and component matching rules

The two phases in a domain should use matched regulator devices, inductor part numbers, output-current path geometry, local PVIN decoupling strategy, and comparable thermal environments wherever practical. Do not create an intentionally asymmetric copper path merely because average current sharing is available. Keep the stacked-device communication/synchronization routing consistent with TI requirements and preserve the existing Kelvin remote-sense boundary.

A phase that persistently runs hotter must be investigated for current imbalance, DCR mismatch, copper resistance, decoupling asymmetry, airflow/cold-plate coupling, or telemetry error before raising any domain-current limit.

## Release rule

`vrm_phase_sharing_validated` remains false until both domains pass the 31.5 A and 50 A steady-state tests, transient/fault checks, telemetry correlation, and thermal checks in the actual shared PCB. The 60 A point may only be attempted afterward as a brief controlled stress test. Passing it does not create a 60 A continuous rating.

This document does not approve a regulator current limit, compensation value, inductor MPN, PCB stackup, or sustained hashrate increase. FREEAXE 21 remains not fabrication-ready until the remaining schematic, routing, stackup, current-density, thermal/mechanical, BOM/CPL, Gerber/drill, ERC/DRC, and fabrication gates are complete.
