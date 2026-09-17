# FREEAXE 21 VCORE transient acceptance gate

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro VCORE architecture. It converts the existing capacitor reservation into a measurable transient acceptance test. It is not a production BOM approval.

## Source basis

Texas Instruments TPS546D24S guidance requires output capacitance to be selected from load-transient voltage deviation and output ripple, with the larger requirement governing. TI's current datasheet example uses a 20 A load step and shows that transient response can require far more capacitance than ripple alone. FREEAXE therefore does not qualify VCORE from steady-state voltage or nominal capacitance alone.

## Shared analytical point

The current shared analytical architecture remains approximately 12 V input, 4.0 V per four-ASIC VCORE domain, two interleaved TPS546D24S phases, 0.68 uH per phase and 600 kHz switching. These are engineering center points, not final component selections.

Existing capacitor analysis reserves at least 1.2 mF nominal low-ESR capacitance per domain with physical room toward roughly 1.5 mF after real DC-bias/tolerance data are known. That reservation remains provisional.

## Provisional transient acceptance envelope

Until a measured BM1373 domain-current waveform replaces the synthetic test, qualify each domain with controlled positive and negative load steps at 10 A, 20 A and 25 A delta-I. The provisional FREEAXE acceptance target is no more than +/-100 mV excursion around the commanded approximately 4.0 V rail for those qualification steps, followed by monotonic recovery without sustained ringing or repeated fault/retry behavior.

The +/-100 mV value is a FREEAXE engineering screening target, not a published BM1373 absolute-limit claim. It must be tightened if verified BM1373 voltage tolerance requires a smaller excursion.

For every load step record at minimum:

- VCORE at the regulator source and remote-sense/load point simultaneously.
- Peak undershoot and overshoot.
- Time to first minimum/maximum and time to settle.
- Ringing frequency and decay if present.
- Total domain current and per-phase current sharing.
- PMBus VOUT, IOUT and die-temperature telemetry.
- Both regulator and both inductor temperatures after thermal equilibrium.
- Input PVIN droop/ringing so an upstream 12 V event is not misdiagnosed as output-loop behavior.

## Operating points

Run the transient matrix after steady-state operation at the existing 31.5 A/domain reference point and again at the 50 A/domain continuous qualification point. Repeat at minimum and maximum intended 12 V input and at the expected hot-board condition. The 60 A/domain point remains controlled stress-only and cannot establish a continuous rating.

A passing average voltage is insufficient. Any local oscillation, repeated PMBus fault, phase-sharing excursion outside the qualified envelope, excessive PVIN ringing, or thermal-limit violation fails the gate even if the peak VCORE excursion remains inside +/-100 mV.

## Air versus Hydro

The electrical transient target is common to Air and Hydro. Both assemblies must be tested because board and VRM temperature can change capacitor ESR, effective capacitance, magnetics behavior and converter losses. Hydro ASIC cooling does not automatically qualify the VCORE power stage.

## Release rule

Dependency 5 remains open until the actual capacitor bank, magnetics, compensation/OCP settings, routed stackup/copper, source impedance and measured transient waveforms pass together. A synthetic load test must eventually be correlated with real BM1373 hashing load behavior. FREEAXE 21 remains not fabrication-ready or JLCPCB-ready from this document.