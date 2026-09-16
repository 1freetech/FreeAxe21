# FREEAXE 21 VRM telemetry validation gate

This document advances dependency 5 for the shared FREEAXE 21 Air/Hydro PCB. It defines how TPS546D24S current telemetry may be used without allowing PMBus readings to substitute for independent electrical qualification.

## Sourced behavior

Texas Instruments documents that TPS546D24S uses SenseFET current sensing and internal VSHARE control for current balancing in stacked multiphase operation. Its telemetry subsystem directly measures input voltage, output voltage, output current, and die temperature; ADC conversion is under 500 us and telemetry values can update within 2 ms. TI also warns that current telemetry can over-report average inductor current when inductor current becomes nonlinear, including operation above inductor saturation current.

These are regulator capabilities, not proof that FREEAXE current readings are accurate under its final magnetics, layout, temperature, and ASIC load spectrum.

## FREEAXE qualification rule

PMBus IOUT is diagnostic telemetry only until correlated against calibrated external instrumentation on a populated prototype. It must not be used by itself to approve 50 A/domain continuous operation, set a final OCP threshold, infer copper loss, or claim ASIC efficiency.

For each four-BM1373 VCORE domain, validate at minimum:

- light-load/startup condition;
- 31.5 A/domain reference point;
- 50 A/domain continuous qualification point after thermal equilibrium;
- 60 A/domain only as a short controlled stress point after 50 A passes.

At each point record external domain current, PMBus IOUT, VCORE_SOURCE, VCORE_LOAD, regulator die temperature, inductor surface temperature, and phase-sharing behavior. Repeat enough samples to distinguish steady offset from noise and transient response.

## Inductor-saturation diagnostic

If PMBus current increasingly diverges high relative to calibrated external current as load or temperature rises, treat that as a possible magnetics/current-waveform fault rather than correcting it away in firmware. Check inductor ripple/current waveform, Isat margin, DCR heating, switching behavior, and regulator temperature before increasing load.

A telemetry calibration factor may only be introduced after the underlying power stage is shown to remain inside the selected inductor and regulator operating limits. Any correction must be documented by operating point and temperature range; one arbitrary scalar is not assumed valid over the full load range.

## Air/Hydro boundary

Air and Hydro use the same electrical telemetry architecture and acceptance method. Hydro cooling of the ASICs does not waive regulator/inductor telemetry validation. If the two mechanical assemblies produce materially different VRM or inductor temperatures, correlation data must be repeated in both because temperature can change the error behavior and available electrical margin.

## Release rule

`vrm_telemetry_validated` remains false until prototype PMBus data is correlated with calibrated external current/voltage measurements through the 50 A/domain qualification point and no unexplained load-dependent divergence remains. Until that test, PMBus values are useful engineering observations but are not release-grade metrology, and FREEAXE 21 remains not fabrication-ready.
