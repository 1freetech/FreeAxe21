# FREEAXE 21 Run 16 — ASIC control refinement

Dependency 6 was rebuilt after the board changed to two four-chip VCORE domains.

The shared Air/Hydro control architecture remains an ESP32-S3 running an ESP-Miner/AxeOS-compatible
FREEAXE board profile and one logical eight-BM1373 UART chain. The chain crosses one voltage-domain
boundary. That boundary is explicitly a schematic blocker: its level translation must be adapted from
validated open hardware or proven by measurement, never guessed.

Hashing is fail-closed. Firmware must see all eight ASICs, healthy two-domain power telemetry, a healthy
UART, required telemetry, released reset, and the variant cooling interlock before work is enabled.
Air uses fan tach/temperature interlocks; Hydro uses flow, pump tach, and coolant-temperature interlocks.

The physical BM1373 reference-clock implementation remains deliberately unresolved. Firmware PLL control
does not prove the oscillator amplitude, board frequency, termination, or fanout network.

NMAxe's 2026 BM1373 driver report is useful evidence that public low-level BM1373 firmware exists and has
reached about 6 TH/s/chip in testing, but that result is not used as a FREEAXE sustained rating because
the associated electrical/thermal test conditions are not published.

Manufacturing remains blocked on the domain-crossing schematic, exact level-shifter components/passives,
clock network, eight-chip bench discovery, sustained accepted-share testing, and fault injection.
