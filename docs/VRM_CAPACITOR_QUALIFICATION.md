# FREEAXE 21 output-capacitor qualification window

This document advances dependency 5 for the shared Air/Hydro VCORE design. It is an analytical gate, not a production BOM selection.

## Source basis

Texas Instruments TPS546D24S datasheet section 8.2.2.4 sizes output capacitance against load-transient overshoot/undershoot, loop bandwidth, output ripple, ESR/impedance, and real capacitance derating. TI's worked example explicitly chooses the largest applicable requirement rather than ripple capacitance alone.

## FREEAXE 21 provisional point

Shared domain assumptions remain 12 V input, approximately 4.0 V domain output, two interleaved TPS546D24S phases, 0.68 uH analytical inductor center point, and 600 kHz switching. These values are not final component selections.

For a conservative 100 mV domain transient allowance, the existing run-21 model gives approximately:

- 10 A transient: 265 uF minimum analytical capacitance.
- 20 A transient: 680 uF minimum analytical capacitance.
- 25 A transient: 1063 uF minimum analytical capacitance.
- Ripple-only requirement at about 6.54 A p-p and 20 mV: about 68 uF.

The large separation between the ripple-only and transient requirements is intentional. FREEAXE must not size the bank from ripple alone.

## Candidate design window

Until a real load-step waveform exists, schematic work should reserve physical area for at least 1.2 mF nominal low-ESR output capacitance per four-ASIC domain, with room to increase toward roughly 1.5 mF after DC-bias and tolerance derating. This is a placement reservation, not an approved capacitor count or MPN.

A candidate bank is acceptable only if its effective capacitance at the actual approximately 4 V bias remains above the model requirement, its aggregate impedance at switching frequency satisfies the ripple target, and its ripple-current and temperature ratings survive the 50 A/domain qualification point. Polymer plus MLCC is permitted, but ESR/ESL must be modeled as a parallel network rather than assuming ideal capacitors.

## Bench qualification

Before this gate can close, measure a domain with an electronic load or equivalent controlled ASIC load step. Record VOUT overshoot/undershoot, settling time, regulator die temperature, capacitor temperature, inductor temperature, and PMBus versus oscilloscope/current-probe readings at 31.5 A and 50 A continuous. The 60 A point remains stress-only. Repeat at minimum and maximum intended 12 V input and at the expected hot-board condition.

Air and Hydro retain the same electrical capacitor bank unless physical thermal testing proves a variant-specific derating is needed. Hydro cooling of ASICs does not count as capacitor or VRM cooling.

## Release rule

No capacitor MPN/count is production-approved from this document. Dependency 5 remains open until exact capacitance technology, bias derating, ESR/ESL, compensation selection, routed copper, and measured transient/thermal behavior are validated. Manufacturing readiness remains false.