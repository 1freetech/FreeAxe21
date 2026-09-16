# FREEAXE 21 VRM local input-decoupling qualification

Status: analytical/layout qualification constraint; **not a BOM release, routed-PCB validation, or fabrication release**.

## Scope

This gate applies to the shared FREEAXE 21 Air/Hydro VCORE power stages and closes another part of dependency #5. It separates board-level 12 V bulk energy storage from the high-frequency local PVIN decoupling required at each stacked TPS546D24S phase.

## Sourced boundary

Texas Instruments specifies TPS546D24S for 2.95 V to 16 V PVIN and 40 A maximum output per converter. TI's current datasheet design procedure requires input capacitance to be selected with DC-bias effects considered, recommends no more than 500 mV input ripple, and requires at least 10 uF input capacitance for all designs. In TI's example, the calculated minimum is 67.3 uF with 5.5 mOhm maximum ESR; TI then uses four 22-uF/25-V ceramic capacitors plus two 100-uF/25-V low-ESR electrolytics, with small 6800-pF PVIN bypass capacitors placed close to the power stage to reduce high-frequency ringing.

Those component values belong to TI's example and are **not copied as FREEAXE values**. FREEAXE has a different output voltage, load, phase count, board geometry, transient spectrum, connector path, and thermal environment.

## FREEAXE design rule

Each TPS546D24S phase must have its own compact local PVIN ceramic/bypass network immediately adjacent to the converter power pins. Do not rely on a remote board-level bulk bank to close the high-di/dt switching loop.

For the shared two-phase-per-domain architecture:

- preserve physically symmetric local PVIN decoupling for the two stacked phases;
- minimize PVIN-capacitor-to-converter-to-ground loop area;
- provide local high-frequency bypass footprints at every phase;
- place additional domain/board bulk capacitance outside the high-frequency loop;
- use capacitor voltage ratings with explicit 12 V rail transient margin;
- calculate effective ceramic capacitance after DC-bias, temperature, and tolerance derating;
- include capacitor ESR/ESL and connector/source impedance in the input-ripple model;
- do not infer adequate input decoupling from total nominal uF alone.

## Qualification points

The final routed board must be evaluated at the existing electrical envelope:

1. 31.5 A/domain reference point;
2. 50 A/domain continuous qualification point;
3. 60 A/domain controlled stress only.

At each point, measure the 12 V rail at the board input and directly at each converter PVIN/GND boundary with appropriate high-bandwidth probing. Record steady ripple, transient droop/overshoot, ringing, local capacitor temperature, converter temperature, connector temperature, and any phase-to-phase asymmetry.

The design fails this gate if the converter-local waveform violates the regulator's input limits or the selected FREEAXE ripple/thermal margin even when the board-input voltage appears acceptable.

## Air/Hydro commonality

Air and Hydro retain the same electrical local-decoupling architecture and footprints. Hydro cooling of the ASICs does not qualify the PVIN capacitors or regulator region. If the Hydro cold plate obstructs natural/forced airflow over the VRM input network, or the Air duct changes that airflow materially, both variants must independently pass capacitor/regulator thermal measurements at 50 A/domain.

## Release blocker

No capacitor MPN/count is approved by this document. Dependency #5 remains open until the actual input capacitor bank, effective capacitance under 12 V bias, ESR/ESL, routed loop geometry, source/connector impedance, ripple, ringing, and thermal behavior are calculated and then verified on hardware together with the unresolved magnetics, output network, compensation, OCP, copper/current-density, and transient tests. FREEAXE 21 remains **not fabrication-ready**.