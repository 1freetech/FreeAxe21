# FREEAXE 21 VRM conduction-loss budget

Status: analytical qualification constraint; **not routed-PCB validation and not a fabrication release**.

## Scope

This gate applies to the shared FREEAXE 21 Air/Hydro two-domain VCORE architecture. It converts the existing 31.5 A reference, 50 A continuous-qualification point, and 60 A stress-only point into a simple measurable resistance/drop budget for each high-current VCORE path. It does not replace IPC-2152 analysis or hardware thermal testing.

## Derived path-resistance limits

For a path carrying domain current `I`, conduction loss is `P = I^2 R` and drop is `V = I R`.

| Domain current | 1 W path-loss budget | Drop | 2 W path-loss budget | Drop | 3 W path-loss budget | Drop |
|---:|---:|---:|---:|---:|---:|---:|
| 31.5 A reference | 1.008 mΩ | 31.7 mV | 2.016 mΩ | 63.5 mV | 3.023 mΩ | 95.2 mV |
| 50 A qualification | 0.400 mΩ | 20.0 mV | 0.800 mΩ | 40.0 mV | 1.200 mΩ | 60.0 mV |
| 60 A stress only | 0.278 mΩ | 16.7 mV | 0.556 mΩ | 33.3 mV | 0.833 mΩ | 50.0 mV |

These values are derived calculations, not measured board values.

## Working design constraint

Use **0.8 mΩ maximum end-to-end resistance per 50 A VCORE distribution path as the provisional layout target** from the regulator output measurement boundary to the defined domain load boundary. At 50 A this corresponds to 40 mV drop and 2 W of path conduction loss. This is a layout budget, not permission for any individual neck, via field, pad transition, plane segment, or connector to run hot.

The 60 A point remains stress-only. Holding the same 0.8 mΩ path at 60 A would dissipate 2.88 W and drop 48 mV, so stress testing must explicitly measure the resulting temperature rise rather than extrapolating the 50 A result.

## Resistance-budget decomposition required before layout sign-off

The measured/calculated end-to-end value must be decomposed so a local bottleneck cannot hide inside an acceptable total:

- regulator output pads and immediate copper escape;
- inductor pads and copper transitions;
- output-capacitor connection region;
- each plane/polygon segment;
- every via array carrying meaningful domain current;
- ASIC-domain feed necks and local spreading copper;
- return-current path over the same electrical boundary.

Kelvin/differential sense traces are excluded from the power-path resistance sum but must terminate at the intended load-sense point so regulator control does not compensate for an arbitrary section of copper drop.

## Validation sequence

1. Freeze the real PCB stackup and finished copper thickness.
2. Extract resistance from the actual routed geometry, including necks and via structures.
3. Calculate loss and voltage drop at 31.5 A, 50 A, and 60 A/domain.
4. Apply IPC-2152-based temperature-rise analysis to the actual geometry; do not substitute a generic trace-width table.
5. On prototype hardware, four-wire measure the same defined path boundary.
6. At 50 A/domain, log copper hot spots, via-field temperatures, inductor/regulator temperatures, VCORE at source and load, and PMBus versus independent current readings.
7. Run 60 A only as controlled stress testing with shutdown limits. Do not convert it into a continuous rating without a separate qualification decision.

## Variant rule

Air and Hydro use the same electrical resistance target. A cold plate reducing ASIC temperature does **not** prove acceptable VRM or PCB copper temperature. If either mechanical cooling implementation changes airflow/contact around the regulator or copper regions, that variant must demonstrate the same 50 A electrical/thermal gate independently.

## Release blocker

Dependency #5 remains open until the actual routed board demonstrates the resistance, current-density, voltage-drop, and thermal requirements above together with the unresolved magnetics, capacitor, compensation, OCP, connector/input-path, and hardware transient tests. FREEAXE 21 remains **not fabrication-ready**.