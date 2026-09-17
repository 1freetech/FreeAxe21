# FREEAXE 21 VRM OCP and fault qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro electrical design. It defines the protection boundary for each two-device TPS546D24S VCORE stack without pretending an unverified current-limit register value is safe.

## Verified device capability

Texas Instruments lists TPS546D24S as a 40 A-per-device synchronous buck converter that supports multi-device stacking/current sharing. PMBus exposes phased output-current warning and fault controls, and fault response can be configured for restart, latch-off, or continued operation. TI documents IOUT_OC_WARN_LIMIT as a per-phase warning command; each phase reports an overcurrent warning independently. TI also documents the related stack behavior such that the effective multiphase current limit depends on the lowest configured per-phase fault limit and the number of phases.

The 80 A arithmetic sum for a two-device stack is therefore a controller nameplate ceiling, not a FREEAXE continuous domain rating. FREEAXE must not set OCP merely by multiplying 40 A by two.

## FREEAXE protection envelope

Each four-BM1373 domain keeps the existing analytical load points:

- 31.5 A/domain: reference operating checkpoint.
- 50 A/domain: continuous electrical qualification checkpoint only.
- 60 A/domain: controlled stress checkpoint only.
- 80 A/domain: prohibited as an inferred continuous rating merely because two nominal 40 A converters are stacked.

At 50 A/domain the ideal two-phase average is 25 A/phase; at the 60 A stress point it is 30 A/phase. Existing phase-sharing, magnetics, copper-loss, telemetry, transient, stability and thermal gates remain independently binding.

Until hardware evidence exists, normal firmware must never command or intentionally sustain the 60 A stress point. The final OCP threshold must sit above the highest validated continuous transient requirement while remaining below the weakest independently established safe limit among regulator thermal capability, selected inductor Isat/Irms, connector/input path, routed copper/vias, and capacitor ripple/transient capability.

## Protection hierarchy

FREEAXE requires three distinct protection layers rather than one current number:

1. **Warning/derating layer.** Firmware receives a PMBus overcurrent warning before a destructive condition and unloads the ASIC domain when practical. The warning threshold remains TBD until telemetry error, ripple and phase imbalance are measured.
2. **Fault layer.** A sustained or sufficiently severe overcurrent forces VCORE into a defined safe response. The default FREEAXE design intent is shutdown/latch-off for a persistent hard fault. Automatic retry is not approved until repeated-restart energy and ASIC behavior are measured.
3. **Independent upstream protection.** The 12 V input protection remains responsible for cable, connector, board-short and gross-converter-fault energy that cannot safely be delegated to PMBus firmware or a VCORE controller.

No software warning is allowed to substitute for hardware fault protection.

## Required protection behavior

1. Power-up default must be fail-safe. Missing ESP32/PMBus configuration must not expose an unrestricted high-current operating state.
2. Both regulators in a stacked domain must enter a known coordinated fault state. A failed/faulted phase must not silently leave its partner attempting to carry the entire domain load.
3. Sustained overcurrent qualification must use latch-off or a deliberately bounded retry policy; unlimited rapid auto-retry is prohibited because it can repeatedly heat a shorted rail.
4. Firmware should capture commanded VCORE, PMBus IOUT, regulator die temperature, fault status and shutdown cause where telemetry remains available.
5. A hard overtemperature or persistent overcurrent event must require the domain to return below a defined safe condition before hashing resumes.
6. Air and Hydro use the same electrical OCP boundary unless measured VRM/inductor temperatures justify variant-specific derating. Hydro coolant capacity must not justify a higher regulator current limit unless the VRM itself is mechanically coupled to the validated liquid thermal path.

## Threshold-selection rule

No final IOUT_OC_WARN_LIMIT or IOUT_OC_FAULT_LIMIT is approved yet. Candidate thresholds must include measurement/tolerance margin and be selected only after final inductor hot Isat/Irms curves, hot DCR, PMBus-versus-external current error, routed copper resistance, capacitor network, compensation and thermal data exist.

A valid warning/fault pair must satisfy all of the following:

- normal sustained operation, including measured ripple and phase imbalance, cannot nuisance-trip;
- the warning remains below the lowest demonstrated continuous thermal/electrical limit of the domain;
- the hard fault remains below the lowest destructive/uncontrolled limit established for magnetics, regulators, copper/vias, connector path and ASIC rail;
- per-phase programming is checked against the effective two-phase stack threshold rather than treating a PMBus value as a domain-current value;
- 60 A stress operation cannot silently redefine the continuous limit.

## Bench qualification sequence

The eventual prototype test must use independent current/voltage measurement in addition to PMBus telemetry. At minimum:

1. Verify clean startup and current sharing at light load.
2. Hold 31.5 A/domain and record phase balance, VCORE_SOURCE/VCORE_LOAD, input current, regulator die temperatures, inductor/capacitor temperatures and copper hot spots.
3. Hold 50 A/domain only after selected magnetics, capacitor bank, routed copper and cooling have passed their own limits.
4. Apply controlled load steps around the intended continuous point and verify no nuisance trip, unacceptable VCORE excursion, phase loss or unstable retry behavior.
5. Exercise 60 A/domain only as a short controlled stress test with external current limiting and temperature aborts. Passing does not make 60 A continuous-rated.
6. Sweep slowly across warning and fault thresholds to verify the programmed per-phase and effective stack behavior.
7. Create a controlled near-short/electronic-load fault with externally limited source energy and verify the configured OCP response removes energy without repeated uncontrolled restart.
8. Verify a fault with PMBus host communication absent; electrical protection must remain effective.
9. Compare PMBus IOUT and temperature telemetry with independent instruments and record error.
10. Repeat relevant thermal/OCP tests in both Air and Hydro mechanical configurations because local VRM temperature can differ even though the electrical PCB is shared.

## Schematic-release rule

No final OCP register/strap value is approved by this document. That value depends on exact magnetics, capacitor network, compensation, routed copper, connector/input path, cooling and measured transient behavior. Until those exist and the bench sequence passes, `controlled_current_paths_validated` and `thermal_mechanical_validation_complete` remain false and FREEAXE 21 is not fabrication-ready or JLCPCB-ready.