# FREEAXE 21 input power path — Run 14 revalidation

Run 14 replaces the obsolete four-branch input distribution with the current shared two-domain architecture.

## Operating envelope versus hardware ceiling

The 4-circuit Molex Mega-Fit family remains the connector candidate: two +12 V contacts and two returns. Molex currently publishes up to 30 A per circuit and wire support through 10 AWG for the family. The design no longer treats 50 A as the expected continuous operating point.

- **42 A** — operational continuous design envelope for qualification
- **50 A** — connector/path validation ceiling
- **55 A** — short-duration screening point only; not a sustained operating target

At 42 A, each positive and return contact carries 21 A with ideal sharing. At the 50 A validation ceiling, each carries 25 A. Both remain below the family-level 30 A maximum, but exact housing/header/terminal combination and connector temperature rise still require qualification.

## Why 42 A

The core thermal envelope remains 400 W. At the minimum modeled input voltage of 10.8 V, 400 W corresponds to 37.04 A. A broader 450 W electrical qualification envelope corresponds to 41.67 A at 10.8 V, so 42 A covers the present core envelope plus a bounded fan/control/pump allowance without pretending that the 50 A connector limit is normal operation.

The external BM1373 reference linearization used elsewhere in the project is about 280 W wall for eight chips at ~20.6 TH/s. At 12 V that is only 23.33 A as a sensitivity point. It remains external-reference-derived, not a FREEAXE measurement.

## Two regulator branches

After input protection the 12 V trunk now divides into two symmetric VRM branches:

- Domain A: four BM1373 ASICs, 2x stacked TPS546D24S input stage
- Domain B: four BM1373 ASICs, 2x stacked TPS546D24S input stage
- auxiliary branch: controller, sensors and variant-specific cooling controls

A deliberately conservative 400 W input allocation at 10.8 V gives 18.52 A per ASIC branch if equally shared. A 450 W allocation gives 20.83 A per branch before auxiliary allocation. The branch routing target is therefore 22 A continuous per branch pending measured imbalance and converter efficiency.

## Main fuse thermal constraint

The 60 A / 32 V Littelfuse JCASE candidate remains provisional. Littelfuse's typical temperature-derating table shows roughly 51 A allowed at 65 C, 46 A at 85 C, and 38 A at 110 C for the 60 A fuse. Therefore:

- the 42 A continuous design envelope is thermally coherent through the published 85 C screening point;
- 42 A is **not** accepted at a 110 C fuse environment;
- the fuse/holder region must be kept at or below 85 C for this candidate, or the operating current/fuse architecture must be changed.

Final selection still requires measured startup/inrush and time-current coordination.

## Harness sensitivity

Using the existing provisional 6.6 mOhm loop-resistance sensitivity, 42 A produces 0.277 V drop and 11.64 W harness/contact loss. This is a sensitivity calculation only. Final validation requires measured resistance and connector/harness temperature rise with the exact 10 AWG assembly.

## Still unresolved

TVS part number, reverse-polarity implementation, inrush control, bulk capacitance, exact Mega-Fit part numbers, per-branch fuse/eFuse strategy, final stackup, routed copper geometry and electro-thermal current-density validation remain open. No fabrication or production-readiness claim is permitted from this run.
