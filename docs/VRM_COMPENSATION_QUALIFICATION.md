# FREEAXE 21 VRM compensation qualification

This document advances dependency 5 for the shared Air/Hydro VCORE design. It defines how the TPS546D24S control loop must be qualified; it does not approve a final compensation setting.

## Verified controller behavior

Texas Instruments specifies TPS546D24S as an average-current-mode converter with selectable internal compensation. In stacked operation the devices share a common output and a single PMBus address. The controller supports twelve switching frequencies from 225 kHz to 1.5 MHz, differential remote sensing, telemetry, configurable soft start, and configurable overcurrent behavior.

TI's current datasheet design procedure explicitly derives a target current-loop gain and voltage-loop gain from the selected inductance and real output impedance. For stacked designs, the CSA gain used in the voltage-loop calculation is divided by the number of phases. TI then selects a discrete internal compensation setting. Importantly, TI's worked example states that a mathematically stable setting was subsequently reduced during bench evaluation to improve gain and phase margin. FREEAXE therefore must not freeze compensation from calculation alone.

## FREEAXE provisional electrical point

The shared analytical center point remains:

- 12 V nominal input.
- Approximately 4.0 V four-BM1373 domain output.
- Two interleaved TPS546D24S phases per domain.
- 0.68 uH analytical inductance per phase.
- 600 kHz analytical switching point.
- At least 1.2 mF nominal low-ESR output-capacitor placement reservation per domain, with room toward 1.5 mF pending effective-capacitance validation.
- 31.5 A/domain historical reference, 50 A/domain qualification point, and 60 A/domain stress-only point.

None of these values by itself proves loop stability.

## Compensation release gate

Before schematic freeze, calculate the TPS546D24S target current-loop and voltage-loop gains using the exact selected inductor and the measured or vendor-characterized impedance of the final capacitor network at approximately 4 V bias. Include ceramic DC-bias derating, polymer/MLCC ESR and ESL, phase count, minimum/maximum input voltage, and tolerance corners.

Select the nearest conservative supported internal compensation setting from the TPS546D24S tables only after those calculations. Do not copy the compensation code or MSEL resistor from a TI example, Bitaxe-derived design, or another voltage/current operating point.

## Bench acceptance

The selected setting remains provisional until hardware testing demonstrates acceptable stability at minimum and maximum intended input voltage and at cold and hot board conditions. Test at no/light load, the 31.5 A reference, 50 A continuous qualification, and controlled load steps representative of ASIC work changes. The 60 A point remains stress-only.

Capture output-voltage overshoot/undershoot, settling, switch-node behavior, phase current sharing, PMBus current/temperature telemetry, and regulator/inductor/capacitor temperatures. Where practical, measure loop response with a frequency-response analyzer or injection method appropriate for the regulator. Any ringing, poor phase sharing, repeated fault recovery, or unacceptable thermal rise blocks the setting.

Air and Hydro retain the same electrical compensation unless measured PCB/VRM thermal behavior proves a variant-specific derating is necessary. Better ASIC cooling on Hydro is not evidence of better regulator loop stability.

## Release rule

Dependency 5 remains open. No MSEL compensation resistor/code, capacitor MPN/count, inductor MPN, OCP threshold, or 60 A continuous rating is production-approved by this document. Final closure still requires exact component selection, compensation calculation, routed-copper validation, and measured transient/thermal/stability results.