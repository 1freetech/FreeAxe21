# FREEAXE 21 VCORE remote-sense boundary

Status: dependency-5 electrical/layout constraint; **not routed-PCB validation and not a fabrication release**.

## Purpose

FREEAXE 21 Air and Hydro share the same two-domain VCORE architecture. Each domain uses stacked TPS546D24S regulators and four BM1373 devices. This document fixes where VCORE regulation is to be observed so differential remote sensing cannot accidentally hide an excessive copper drop or regulate an arbitrary point in the high-current path.

## Sourced capability

Texas Instruments specifies differential remote sensing on TPS546D24S, with an internal feedback divider and less than 1% VOUT error over the stated junction-temperature range. TI also specifies stacked current sharing, PMBus VOUT/IOUT/die-temperature telemetry, adjustable current limiting, and selectable internal compensation. Those are device capabilities, not proof that the FREEAXE PCB is correctly routed or stable.

## Derived FREEAXE boundary

The existing provisional distribution target is no more than **0.8 mOhm end-to-end resistance per VCORE domain path** at the 50 A continuous qualification point. That produces a derived 40 mV distribution drop and 2 W path loss at 50 A. The same resistance produces 25.2 mV / 0.794 W at 31.5 A and 48 mV / 2.88 W at the 60 A stress-only point.

The differential sense pair shall therefore terminate at a defined representative **domain load regulation point near the ASIC-side VCORE distribution region**, after the principal regulator-to-load copper path. It shall not sense directly at the regulator output merely because that location is convenient, and it shall not terminate at an electrically extreme single ASIC pad that causes the regulator to over-correct for local spreading resistance.

The exact physical pads/vias remain to be selected from the real PCB placement and routing. Until then, this is a boundary rule rather than a coordinate-level layout instruction.

## Measurement boundary

Prototype qualification must expose or otherwise make measurable both sides of the distribution path:

1. **VCORE_SOURCE** — regulator/output-capacitor-side measurement point.
2. **VCORE_LOAD** — representative ASIC-domain load-side measurement point colocated electrically with the differential-sense termination.
3. Measure both with independent instrumentation while also logging PMBus VOUT/IOUT.
4. Calculate `R_path = (VCORE_SOURCE - VCORE_LOAD) / I_domain` only after readings have reached thermal equilibrium.
5. At 50 A/domain, reject the routed path if the measured source-to-load drop exceeds 40 mV or if any local copper/via/component transition violates its temperature limit even when total drop is below 40 mV.
6. Repeat the 50 A test in both Air and Hydro mechanical assemblies. Hydro ASIC cooling cannot be used to waive a VRM/copper hot spot.
7. Exercise 60 A only as controlled stress testing with shutdown limits; it remains non-continuous unless separately qualified.

## Routing requirements

- Route the differential pair together, away from switch nodes, inductors, clocks, ASIC UART lines, and other high-dV/dt or high-dI/dt structures.
- Keep sense conductors out of the power-current path; they are measurement conductors, not load-sharing copper.
- Avoid sharing sense vias with high-current layer transitions where practical.
- Preserve a quiet return reference to the intended load regulation point.
- Document the final sense termination and the VCORE_SOURCE/VCORE_LOAD test points in the schematic and PCB notes before layout sign-off.
- Do not use remote-sense compensation to justify a path that fails the 0.8 mOhm/40 mV distribution target or thermal qualification.

## Why this matters

Remote sensing can make the ASIC-side voltage appear well regulated while the regulator-side voltage rises enough to compensate for PCB loss. That is useful within a qualified distribution network, but it can also conceal excessive I-squared-R heating if only the sensed VCORE value is inspected. FREEAXE therefore treats voltage regulation and distribution loss as separate acceptance criteria.

## Release blocker

Dependency #5 remains open until actual stackup and routing define the physical sense/test points, extracted and four-wire measured path resistance meet the distribution budget, and 31.5 A / 50 A hardware tests demonstrate stable regulation, acceptable phase sharing, transient response, and thermal margin. The unresolved magnetics, capacitor network, compensation/OCP settings, connector/input path, and prototype thermal tests also remain blockers. FREEAXE 21 is **not fabrication-ready**.
