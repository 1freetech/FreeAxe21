# FREEAXE 21 VRM OCP and fault qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro electrical design. It defines the protection boundary for each two-device TPS546D24S VCORE stack without pretending an unverified current-limit register value is safe.

## Verified device capability

Texas Instruments lists TPS546D24S as a 40 A-per-device synchronous buck converter that supports 2x, 3x, and 4x stacking with current sharing up to 160 A. The device provides adjustable current limiting, over-current protection, PMBus telemetry, configurable soft start, differential remote sensing, and selectable fault responses including restart, latch-off, or ignore. Source: TI TPS546D24S product/datasheet, checked 2026-09-16.

The 80 A value for a two-device stack is therefore a device nameplate sum, not a FREEAXE continuous domain rating. FREEAXE must not set OCP merely by multiplying 40 A by two.

## FREEAXE protection envelope

Each four-BM1373 domain keeps the existing analytical load points:

- 31.5 A/domain: historical 252 W total-VCORE-equivalent reference point.
- 50 A/domain: 400 W total qualification envelope and intended continuous electrical qualification point.
- 60 A/domain: controlled stress point only.
- 80 A/domain: two-device regulator nameplate sum only; explicitly not an operating target.

Until hardware evidence exists, normal firmware must never command or intentionally sustain the 60 A stress point. The final OCP threshold must sit above the highest validated continuous transient requirement while remaining below the weakest independently established safe limit among regulator thermal capability, selected inductor Isat/Irms, connector/input path, routed copper/vias, and capacitor ripple/transient capability.

## Required protection behavior

1. Power-up default must be fail-safe. A missing ESP32/PMBus configuration must not expose an unrestricted high-current operating state.
2. Both regulators in a stacked domain must enter a known synchronized fault state. A failed/faulted phase must not silently leave its partner attempting to carry the entire domain load.
3. Sustained over-current qualification should use latch-off or a deliberately bounded retry policy; unlimited rapid auto-retry is prohibited because it can repeatedly heat a shorted rail.
4. Firmware must log the commanded VCORE, PMBus IOUT, regulator die temperature, fault status, and shutdown cause before retry where telemetry remains available.
5. A hard over-temperature or persistent over-current event must require the domain to return below a defined safe condition before hashing resumes.
6. Air and Hydro use the same electrical OCP boundary unless measured VRM/inductor temperatures justify a lower Air limit. Hydro coolant capacity must not be used to justify a higher regulator current limit unless the VRM itself is mechanically coupled to the validated liquid thermal path.

## Bench qualification sequence

The eventual prototype test must use an independent current/voltage measurement in addition to PMBus telemetry.

1. Verify clean startup and current sharing at light load.
2. Hold 31.5 A/domain and record phase balance, VCORE, input current, regulator die temperatures, inductor temperatures, capacitor temperatures, and copper hot spots.
3. Hold 50 A/domain only after the selected magnetics, capacitor bank, routed copper, and cooling arrangement have passed their own limits.
4. Apply controlled load steps around the intended continuous point and verify no nuisance trip, unacceptable VCORE excursion, phase loss, or unstable retry behavior.
5. Exercise 60 A/domain only as a short controlled stress test with external current limiting and temperature aborts. Passing this point does not make 60 A continuous-rated.
6. Create a controlled fault/short test appropriate to the prototype fixture and verify the configured OCP response removes energy without repeated uncontrolled restart.
7. Compare PMBus IOUT and temperature telemetry with independent instruments and record error.
8. Repeat the relevant thermal/OCP tests in both Air and Hydro mechanical configurations because local VRM temperature can differ even though the electrical PCB is shared.

## Schematic-release rule

No final OCP register/strap value is approved by this document. That value depends on the exact magnetics, capacitor network, compensation, routed copper, connector/input path, cooling, and measured transient behavior. Until those exist and the bench sequence passes, `controlled_current_paths_validated` and `thermal_mechanical_validation_complete` remain false and FREEAXE 21 is not fabrication-ready.