# FREEAXE 21 VRM switching-frequency qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro board and corrects an important modeling assumption: 600 kHz must not be treated as an effective TPS546D24S switching-frequency setting.

## Sourced device constraint

Texas Instruments TPS546D24S FREQUENCY_SWITCH supports discrete effective frequencies of 225, 275, 325, 375, 450, 550, 650, 750, 900, 1100, 1300, and 1500 kHz. A decoded command from 501 kHz through below 600 kHz maps to 550 kHz; a decoded command from 601 kHz through below 700 kHz maps to 650 kHz. TI's worked design uses 550 kHz as a moderate compromise between solution size and efficiency.

Therefore any earlier FREEAXE calculation using an exact 600 kHz effective switching frequency is a modeling placeholder, not a realizable TPS546D24S operating point, and must not be used for component release.

## Corrected ripple screening

For the current provisional 12 V input, 4.0 V output, 0.68 uH per-phase inductor model, ideal buck duty ratio is 1/3. Using delta-I = (VIN - VOUT) * D / (L * fSW):

- at 550 kHz, per-phase inductor ripple is approximately 7.13 A peak-to-peak;
- at 650 kHz, per-phase inductor ripple is approximately 6.03 A peak-to-peak.

At the 50 A/domain two-phase qualification point (25 A average/phase), ideal peak phase current is therefore approximately 28.57 A at 550 kHz or 28.02 A at 650 kHz. At the controlled 60 A/domain stress point (30 A average/phase), ideal peak phase current is approximately 33.57 A at 550 kHz or 33.02 A at 650 kHz.

These are derived idealized screening calculations. They do not include dead time, conversion loss, inductance tolerance, hot inductance reduction, input ripple, control dynamics, or layout parasitics.

## Provisional architecture choice

Use 550 kHz as the default qualification candidate because it is a directly supported effective setting and TI explicitly uses it as a moderate efficiency/size operating point. Keep 650 kHz as an alternate to evaluate only if measured transient response, magnetics size, and ripple improvement justify the additional switching loss and thermal load.

Do not promote either frequency to final until the selected inductor/capacitor network, compensation setting, routed PCB, and representative thermal assembly are tested. Air and Hydro share the same nominal electrical frequency unless measured thermal behavior requires variant-specific derating; cooling hardware alone is not a reason to create different VRM firmware profiles.

## Required bench comparison

On representative hardware, compare 550 kHz and 650 kHz at light load, 31.5 A/domain, and 50 A/domain after thermal equilibrium. Record board-boundary input power, ASIC-side VCORE, phase current/ripple, transient excursion, regulator die temperature, inductor temperature, copper hot spots, and PMBus telemetry. Reject 650 kHz if its measured ripple/transient benefit does not outweigh switching-loss and temperature penalties.

## Dependency impact

All future inductor peak-current, saturation-margin, capacitor-ripple, switching-loss, and thermal calculations must use a realizable effective frequency. Existing 600 kHz-derived ripple numbers should be superseded by the 550 kHz default candidate or an explicitly identified supported alternative.

This correction does not approve 50 A/domain continuous operation or increase the FREEAXE 21 hashrate estimate. Dependency 5 remains open pending final component selections, compensation/OCP, routed stackup/current-density validation, and representative electrical/thermal measurements. FREEAXE 21 remains not fabrication-ready or JLCPCB-ready.