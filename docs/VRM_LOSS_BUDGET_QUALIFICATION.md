# FREEAXE 21 VRM loss-budget qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro board by defining how regulator, magnetics, copper, and input-path losses must be accounted before a sustained VCORE current or hashrate is promoted.

## Evidence boundary

Texas Instruments specifies TPS546D24S as a 40 A synchronous buck converter, 2.95 V to 16 V PVIN, with integrated 4.5 mOhm high-side and 0.9 mOhm low-side MOSFETs, stackable current sharing, PMBus VOUT/IOUT/die-temperature telemetry, differential remote sensing, selectable switching frequency, and configurable fault behavior. These are sourced device capabilities; they do not prove FREEAXE conversion efficiency or thermal capability.

FREEAXE therefore does not infer VRM efficiency from the 40 A nameplate or from ideal duty-cycle equations. Final efficiency must be measured on representative routed hardware.

## Qualification points

Each four-BM1373 VCORE domain retains:

- 31.5 A/domain: reference load point.
- 50 A/domain: continuous electrical qualification point.
- 60 A/domain: controlled stress only.
- 80 A/domain: summed regulator nameplate only; not a design rating.

At a provisional 4.0 V domain rail, delivered load power is 126 W, 200 W, and 240 W respectively. With two identical domains the 50 A qualification point represents 400 W delivered VCORE power before conversion and distribution losses. These are derived calculations, not measured miner power.

## Required loss ledger

For each domain and qualification point, record separately:

1. regulator high-side/low-side conduction loss;
2. regulator switching/gate/control loss;
3. inductor DCR/core loss at measured hot temperature;
4. output-plane, via, pad, and neck I^2R loss;
5. local PVIN/input-plane and via loss;
6. connector, fuse, protection FET, shunt, and other shared 12 V path loss allocated to the domain;
7. auxiliary rail/control/fan/pump power separately from ASIC VCORE power.

Do not combine unknown terms into an unexplained efficiency percentage. Datasheet calculations are estimates; prototype input/output wattage is the acceptance measurement.

## Measurement gate

On representative hardware, simultaneously measure 12 V input voltage/current at the board boundary and VCORE voltage/current at each domain load point after thermal equilibrium. Correlate with PMBus telemetry and regulator/inductor/copper temperatures. Repeat at 31.5 A and 50 A per domain, at intended input-voltage extremes and in both Air and Hydro assemblies.

Calculate measured domain conversion/distribution efficiency as P_VCORE_load / P_domain_input only after instrumentation boundaries are documented. Report auxiliary power separately so board-wall efficiency cannot be confused with VRM efficiency.

A measured efficiency number must include instrument accuracy and repeatability. Any unexplained input-minus-output power must remain an unresolved loss, not be assigned to ASIC consumption.

## Thermal/reliability rule

No sustained-current promotion is allowed if the measured electrical efficiency is acceptable but any regulator, inductor, capacitor, connector, protection component, via transition, or copper neck violates its qualified thermal margin. Hydro may improve ASIC temperature without improving a VRM bottleneck; Air and Hydro therefore qualify independently.

## Release rule

This document does not assign a final VRM efficiency or approve 50 A/domain continuous operation. Dependency 5 remains open until final routed geometry, stackup, magnetics/capacitors, compensation/OCP, source impedance, loss measurements, and thermal/transient/current-sharing tests exist. FREEAXE 21 remains not fabrication-ready or JLCPCB-ready.