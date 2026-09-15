# FREEAXE 21 manufacturing release gate

Run 10 does **not** create Gerbers, drill files, a pick-and-place/CPL file, or a production BOM. Doing so before a routed and checked KiCad board would create false manufacturing confidence.

The common Air/Hydro design is allowed to advance to fabrication outputs only after all gates in `manufacturing/readiness.json` are true. In particular, a real KiCad schematic and board must exist; ERC and DRC must have no unresolved errors; footprints and pad numbering must be verified; the stackup and high-current copper must be selected/validated; the Air and Hydro mechanical/thermal assemblies must be checked; and the BOM must contain actual manufacturer part numbers rather than family placeholders.

KiCad's normal fabrication set includes per-layer Gerber files, Excellon drill files, and position files. Those are downstream outputs of the actual PCB design, not substitutes for it. The project should eventually generate them reproducibly with `kicad-cli` after the PCB passes DRC.

## Shared manufacturing strategy

Use one electrically identical base PCB whenever routing and mechanical checks allow it. Fit Air-specific fan/cooling hardware or Hydro-specific pump/flow/coolant hardware as variant assemblies. Do not fork the core schematic merely because the thermal assembly changes.

## Next engineering dependency

The next valid work is to construct and verify the real KiCad schematic hierarchy and footprints from authoritative/open sources, then run ERC. Only after that should the board be routed and DRC-driven fabrication outputs be generated.
