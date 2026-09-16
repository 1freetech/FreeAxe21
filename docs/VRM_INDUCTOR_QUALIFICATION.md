# FREEAXE 21 — VRM inductor qualification

Status: dependency 5 engineering gate. This is not a released BOM selection.

## Shared Air/Hydro electrical assumption

Both variants retain the same provisional two-phase VCORE architecture per four-BM1373 domain. For the present analytical point:

- PVIN = 12 V
- VCORE domain rail = 4.0 V
- switching frequency = 600 kHz per phase
- inductance = 0.68 uH per phase
- two interleaved phases per domain
- 31.5 A/domain = reference operating point
- 50 A/domain = continuous qualification point
- 60 A/domain = controlled stress point only

Using the ideal buck ripple approximation, Delta-I_L = (VIN - VOUT) * D / (L * f), with D = VOUT/VIN, the per-phase peak-to-peak ripple is about 6.536 A.

## Calculated phase-current envelope

| Domain current | Average/phase | Peak/phase | RMS/phase |
| ---: | ---: | ---: | ---: |
| 31.5 A | 15.75 A | 19.02 A | 15.86 A |
| 50 A | 25.00 A | 28.27 A | 25.07 A |
| 60 A stress only | 30.00 A | 33.27 A | 30.06 A |

These are derived ideal-waveform values, not measured hardware results. Real ripple and peaks can be worse because of inductance tolerance, temperature, saturation, switching-frequency tolerance, input variation, control behavior and layout parasitics.

## Provisional magnetics gate

Do not approve an inductor merely because its headline current rating exceeds 25 A. Candidate parts must be checked from manufacturer curves at the intended hot operating condition.

For screening before prototype validation:

1. Saturation current must remain above the 33.27 A calculated stress-point peak after tolerance and temperature effects. A provisional 25% engineering margin puts the screening target at >=41.6 A Isat at the chosen inductance-drop criterion.
2. Thermal/RMS current capability must exceed the 30.06 A stress-point RMS current without violating the vendor temperature-rise limit. Continuous 50 A/domain operation still requires measured inductor temperature at ~25.07 A RMS/phase.
3. DCR must be taken from the selected MPN and hot-copper estimate, then included explicitly in the domain loss budget. No generic DCR assumption may close dependency 5.
4. Inductance-vs-current curves must show adequate retained inductance through the 28.27 A continuous-qualification peak and the 33.27 A controlled-stress peak.
5. Footprint, height, pad geometry and thermal path must fit the common Air/Hydro PCB without compromising ASIC cooling hardware or VCORE copper width.

The >=41.6 A Isat value is a FREEAXE screening margin, not a BM1373 or regulator specification and not a production limit.

## Prototype validation

At minimum, log VCORE source/load voltage, total domain current, per-phase current where practical, PMBus telemetry, regulator temperature and inductor case temperature at light load, 31.5 A/domain and 50 A/domain after thermal equilibrium. The 60 A/domain point is permitted only as a controlled stress test after lower-current behavior passes.

Reject or derate a candidate if inductance collapse, abnormal current telemetry divergence, excessive ripple/ringing, phase imbalance, unstable VCORE, or magnetics temperature appears before the qualification point.

Hydro cooling of the ASICs does not automatically improve inductor temperature. Air and Hydro therefore share this electrical gate until assembly-level measurements demonstrate a justified variant-specific derating.

## Open items

Dependency 5 remains open until an exact inductor MPN is selected and its hot Isat/Irms/DCR curves, capacitor network, compensation, OCP, routed copper/vias, source impedance and prototype thermal/transient behavior are validated. FREEAXE 21 is not fabrication-ready or production-ready.
