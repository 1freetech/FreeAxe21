# FREEAXE 21 Run 13 — Two-Domain PCB Placement Refinement

## Concrete placement decision

The shared Air/Hydro PCB remains **180 × 120 mm**. This is not because the four-regulator topology needs the old area; it is because 120 mm board height cleanly supports the current 120 mm-class forced-air cooling envelope while 180 mm width preserves separate input/protection and control/service areas outside the central cooling footprint. Board shrink is deferred until routed copper, connector clearance, and thermal hardware are physically validated.

The eight BM1373 positions remain a centered 4 × 2 cluster on 16 mm pitch. The electrical domains are now physical rows:

- **Domain A:** U1–U4, upper row.
- **Domain B:** U5–U8, lower row.

Each row gets one **two-device TPS546D24S stack** immediately adjacent to it: Domain A's pair above the upper row and Domain B's pair below the lower row. The nominal gap from ASIC package edge to regulator-zone edge is 9 mm, keeping the eventual high-current transition below the 15 mm placement target while preserving clearance from the shared 70 × 40 mm cold-plate contact rectangle.

The TPS546D24S itself is a 7 × 5 mm, 40 A device and supports multi-device stacking, but the 42 × 28 mm zones in this placement are deliberately larger because the final power stage also needs inductors, input/output capacitance, sensing, thermal vias, and spacing. The zones are not released footprints.

## Why rows, not columns

The current candidate power architecture has four BM1373s in series per regulated domain. A contiguous row minimizes the physical span of the domain ladder and makes it possible to keep each high-current power stage close to its own chain. It also prevents the two domains from interleaving spatially, which would complicate level shifting, fault isolation, copper pours, and debugging.

## Shared thermal/mechanical envelope

The ASIC body envelope remains 58 × 26 mm and is fully contained by the 70 × 40 mm shared thermal contact target. The 75 × 75 mm four-hole pattern is unchanged. Air and Hydro therefore still use exactly the same PCB coordinates and mounting points at this stage.

## Sourced versus derived

**Sourced/open-reference:** Gamma Hex uses six modern Bitmain ASICs arranged as two domains of three and a four-phase TPS546D24S regulator. TI specifies the TPS546D24S as 7 × 5 mm, 40 A, stackable, with PMBus telemetry.

**Derived for FREEAXE 21:** two rows of four BM1373s, 16 mm pitch, 9 mm nominal VRM-zone-to-ASIC-edge separation, 70 × 40 mm contact target, and retaining the 180 × 120 mm outline. These are layout decisions, not measured performance results.

**Still speculative/unvalidated:** the exact four-BM1373 series-domain copper/node implementation, BM1373 footprint/land pattern, stacked-regulator magnetics/compensation, and final current-carrying layer structure.

## What this invalidates / what becomes next

This replaces the old four-VRM-zone placement. Dependency 3 is now internally consistent with Run 12, but dependency 4 must be redone next: the 12 V input branch geometry, protection, connector loading and fuse model must be re-sized for **two** regulator branches rather than four. No routing, Gerber, CPL, or production BOM is authorized by this run.

## Sources

- Bitaxe Gamma Hex repository: https://github.com/bitaxeorg/bitaxeGammahex
- TI TPS546D24S product/data information: https://www.ti.com/product/TPS546D24S
