# FREEAXE 21 — VRM thermal derating qualification

Status: dependency 5 engineering gate. This is not a released operating rating.

## Shared Air/Hydro electrical architecture

Both FREEAXE 21 variants retain the same provisional two-phase TPS546D24S VCORE architecture per four-BM1373 domain. The regulator's 40 A per-device capability and two-device stacked capability are silicon feature limits, not permission to operate a FREEAXE domain at 80 A continuously.

Current qualification points remain:

- 31.5 A/domain: reference operating point
- 50 A/domain: continuous qualification point
- 60 A/domain: controlled stress point only
- 80 A/domain: two-device nameplate sum only; not a FREEAXE operating point

## Thermal derating rule

Dependency 5 cannot close from electrical current limits alone. Continuous domain current must be derated to the lowest limit imposed by regulator junction temperature, inductor temperature, capacitor temperature, PCB copper/via temperature, connector/input-path temperature, phase balance, VCORE regulation, and assembly cooling.

TPS546D24S exposes internal die-temperature telemetry, but PMBus telemetry is not accepted as the only thermal instrument. Prototype qualification must correlate it with external temperature measurements at both regulator packages, both inductors, the hottest VCORE copper/via transition, local input/output capacitor banks, and the 12 V feed path.

## Provisional FREEAXE qualification margins

Until prototype measurements exist:

1. 50 A/domain is a test target, not a released continuous rating.
2. 60 A/domain remains stress-only even if the ASIC cold plate or heatsink can remove the ASIC heat.
3. A variant must be derated if any power-delivery component reaches its manufacturer limit or if thermal rise continues without reaching a stable plateau during the sustained test.
4. For design screening, target at least 20 C measured margin below the applicable component maximum at the intended worst-case ambient/coolant condition. This 20 C value is a FREEAXE engineering margin, not a TI specification.
5. Air and Hydro may receive different sustained current/hashrate limits even with an identical PCB because their airflow around the VRM and magnetics can differ substantially. Hydro ASIC cooling does not count as VRM cooling unless the cold-plate/mechanical design intentionally couples to those components and measurements prove the benefit.

## Qualification sequence

After lower-current bring-up passes, hold each operating point until temperatures reach a stable plateau and log domain current, VCORE source/load voltage, PMBus regulator temperatures, external regulator temperatures, inductor temperatures, capacitor-bank temperatures, input connector/protection temperature, copper/via hot spots, ambient air temperature, and—on Hydro—coolant inlet temperature.

Run the sequence at light load, 31.5 A/domain, and 50 A/domain. The 60 A/domain point may be attempted only after 50 A passes and must remain time-limited until a separate continuous qualification justifies changing that rule.

Reject or derate the operating point for thermal runaway, unresolved phase-temperature imbalance, excessive VCORE drop/ripple, telemetry disagreement, magnetics saturation symptoms, connector/copper hot spots, or insufficient component-temperature margin.

## Evidence classification

- Sourced/proven: TPS546D24S is specified by TI as a 40 A converter, supports stacked current sharing, PMBus VOUT/IOUT/internal-die-temperature telemetry, differential remote sense, phase interleaving, adjustable current limit, and operation up to 150 C junction/operating-temperature range as specified by TI.
- Derived FREEAXE calculations: existing ripple/current/loss calculations in the dependency-5 documents.
- FREEAXE engineering gates: 31.5/50/60 A domain qualification points and the provisional 20 C thermal-margin target.
- Unproven until hardware exists: actual steady-state regulator, inductor, capacitor, copper, connector and ASIC temperatures in either Air or Hydro.

## Open items

Dependency 5 remains open pending exact magnetics and capacitor MPNs, compensation/OCP values, selected PCB stackup and routed geometry, extracted/four-wire resistance, current-density analysis, assembly airflow/cold-plate interaction, and prototype thermal/transient/current-sharing measurements. FREEAXE 21 Air and Hydro are not fabrication-ready, JLCPCB-ready, production-ready, or released for a sustained 50 A/domain rating.