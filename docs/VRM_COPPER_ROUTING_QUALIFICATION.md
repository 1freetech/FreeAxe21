# FREEAXE 21 VRM copper and via qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro PCB. It converts the existing 31.5 A / 50 A / 60 A per-domain electrical envelope into PCB-routing requirements without pretending a generic trace-width formula proves the board safe.

## Evidence boundary

IPC-2152 is the applicable empirical basis for PCB conductor current versus temperature rise; simple legacy IPC-2221 trace formulas are not accepted as final qualification. Saturn PCB Toolkit documents IPC-2152 conductor and via calculations and recommends IPC-2152 without modifiers for ordinary use. Texas Instruments high-current layout guidance independently emphasizes short, wide current paths, adequate copper, thermal-via arrays, minimized high-frequency loop area, and avoiding excessive/crowded vias that remove useful plane copper.

These sources are layout guidance, not validation of FREEAXE geometry. Final current capacity depends on the selected fabrication stackup, finished copper thickness, plane geometry, via drill/plating, nearby copper, airflow/liquid mechanical configuration, ambient temperature, connector footprints, and measured board temperatures.

## Shared-board routing envelope

Each four-BM1373 VCORE domain retains:

- 31.5 A/domain: reference load point.
- 50 A/domain: continuous electrical qualification point.
- 60 A/domain: short controlled stress point only.
- 80 A/domain: regulator nameplate sum only, never a PCB-routing target.

The Air and Hydro variants use the same copper architecture unless measured thermal results require an Air derating. Hydro ASIC cooling must not be credited toward PCB current capacity unless the cold plate is intentionally and electrically safely coupled to the relevant copper/VRM thermal path and that arrangement is tested.

## Layout rules before routing freeze

1. Do not route the 50 A domain path as a single narrow trace. Use broad copper regions/planes and parallel layers where the selected stackup permits.
2. Keep each regulator-to-inductor-to-output-capacitor power path compact. Minimize the high-di/dt input and switch loops; large switch-node copper is prohibited merely for thermal spreading because it increases switching-node area and EMI coupling.
3. Put local input decoupling immediately at each regulator power stage and provide a low-inductance return.
4. Use multiple vias whenever domain current must change layers. Via count is to be calculated from finished hole diameter, plating thickness, board thickness, allowed temperature rise, and current sharing; no fixed "amps per via" rule is accepted.
5. Do not crowd via arrays so tightly that antipads/drills materially neck the plane. Preserve continuous copper around the array.
6. Kelvin/differential VCORE sense routing must not share the high-current voltage-drop path. Sense at the intended load regulation point and route the pair away from switch nodes.
7. Reserve temperature-measurement locations at both regulator stacks, both inductors, the highest-current copper necks, input connector/fuse path, and representative output-domain copper.
8. Any connector, fuse, shunt, protection FET, or mechanical transition that carries the full board current is part of the current-density gate; a wide PCB plane cannot compensate for a hotter bottleneck elsewhere.

## Required stackup calculation

Before `controlled_current_paths_validated` may become true, record for every high-current segment:

- layer and finished copper thickness;
- minimum effective width after pads, clearances, slots, and via antipads;
- segment length;
- expected continuous current and stress current;
- IPC-2152/Saturn calculated temperature-rise estimate;
- DC resistance and I^2R loss estimate;
- via drill, finished plating assumption, count, and calculated current/temperature margin for every layer transition;
- nearest heat source and assumed local ambient/airflow condition.

The calculation must use the actual routed geometry exported from the PCB, not a hypothetical width entered before layout.

## Prototype acceptance test

After routing and fabrication, operate each domain at 31.5 A and then 50 A with independent voltage/current instrumentation. Record connector, fuse/protection, regulator, inductor, capacitor-bank, via-array, and copper-neck temperatures after thermal equilibrium. Compare VCORE at the regulator sense point and ASIC-domain load point to quantify distribution drop. Repeat the relevant measurements in both Air and Hydro mechanical assemblies.

Only after 50 A/domain passes the selected component temperature limits and the project's thermal-margin requirement may 60 A/domain be exercised briefly as a controlled stress test. Passing 60 A does not establish a 60 A continuous rating.

## Release rule

No copper width, via count, layer count, or finished copper weight is approved by this document. Those values must follow the selected PCB stackup and actual routing. Until routed geometry is checked with IPC-2152-based calculations and verified thermally on prototypes, `controlled_current_paths_validated` remains false and FREEAXE 21 is not fabrication-ready.
