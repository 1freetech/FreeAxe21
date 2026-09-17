# FREEAXE 21 VRM stability-margin qualification

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro VCORE architecture. It turns loop stability from a qualitative requirement into a measurable release gate. It does not approve a final compensation code, capacitor network, inductor, or sustained current rating.

## Sourced controller behavior

Texas Instruments specifies TPS546D24S as an average-current-mode converter with selectable internal compensation and two-, three-, or four-device stacking. TI's design procedure calculates target current-loop and voltage-loop gains from the selected inductance and output impedance, then maps those targets to supported compensation settings. TI also states that bench optimization can be necessary and that increasing voltage-loop gain improves transient response only while sufficient gain and phase margin remain.

These are controller capabilities and design-method facts, not proof that the FREEAXE operating point is stable.

## FREEAXE analytical point

The shared working point remains 12 V nominal input, approximately 4.0 V per four-BM1373 domain, two interleaved TPS546D24S phases per domain, 0.68 uH analytical inductance per phase, and 600 kHz analytical switching frequency. The current checkpoints remain 31.5 A/domain reference, 50 A/domain continuous qualification, and 60 A/domain controlled stress only.

The capacitor reservation remains at least 1.2 mF nominal low-ESR placement per domain with room toward 1.5 mF, pending final effective-capacitance, ESR, ESL, bias, tolerance, and temperature characterization.

## Provisional stability gate

FREEAXE adopts the following engineering screening targets for the final hardware loop-response measurement:

- Phase margin: at least 45 degrees at the measured unity-gain crossover.
- Gain margin: at least 10 dB.
- Preferred design target: at least 50 degrees phase margin where achievable without unacceptable transient degradation.
- No sustained or growing oscillation, subharmonic behavior, repeated pulse-width jitter, or load-dependent instability.

These numbers are FREEAXE engineering acceptance targets, not TI or BM1373 specifications. Passing them does not override thermal, transient, current-sharing, VCORE-drop, or ASIC-stability gates.

## Measurement method

After final magnetics and capacitor selections and representative routing exist, inject a small AC perturbation into the feedback/remote-sense control path using a frequency-response analyzer or an equivalent validated method appropriate for the regulator. Measure the actual loop response rather than inferring stability from a load-step waveform alone.

Run the measurement at minimum, nominal, and maximum intended 12 V input; light load; the 31.5 A reference point; and the 50 A continuous qualification point after thermal equilibrium. Repeat at cold and hot board conditions. The 60 A point remains stress-only and is not required to establish a continuous rating.

Correlate loop-response results with simultaneous load-step captures, VCORE_SOURCE/VCORE_LOAD, phase currents, PVIN disturbance, PMBus telemetry, switch-node behavior, and regulator/inductor/capacitor temperatures. A loop-response pass with unacceptable transient excursion or thermal behavior is still a system failure.

## Air and Hydro rule

Air and Hydro use the same compensation configuration by default because they share the electrical architecture. Each assembled variant must nevertheless demonstrate acceptable behavior at its own thermally stabilized operating condition. Hydro ASIC cooling cannot be used as evidence that the VRM loop has adequate margin, and Air airflow cannot be assumed to cool all regulator components uniformly.

## Release rule

Dependency 5 remains open until the exact inductor and capacitor network, compensation setting, OCP behavior, routed stackup/copper, and representative hardware are available and measured. No compensation code, MSEL resistor, 50 A sustained rating, or higher hashrate rating is production-approved by this document. FREEAXE 21 remains not fabrication-ready or JLCPCB-ready.