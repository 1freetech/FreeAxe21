# FREEAXE 21 VRM magnetics window

Status: dependency 5 analytical constraint only. This does not select a production inductor and does not make the board fabrication-ready.

## TI-derived constraints

TPS546D24S is a 40 A per-device buck converter that supports 2x-4x stacking/current sharing. TI documents 12 selectable switching frequencies from 225 kHz to 1.5 MHz, selectable internal compensation, differential remote sensing, and PMBus VOUT/IOUT/die-temperature telemetry. TI's datasheet design procedure explicitly calculates the output inductor per phase because load current is divided across phases. In the datasheet worked example, TI uses 550 kHz as a moderate efficiency/size compromise; that example's 120 nH result is application-specific and is **not** copied into FREEAXE 21.

Sources:
- https://www.ti.com/product/TPS546D24S
- https://www.ti.com/lit/ds/symlink/tps546d24s.pdf

## FREEAXE 21 analytical window

For the current two-phase-per-domain model at 12 V input, approximately 4 V domain output and the 50 A/domain qualification point, each phase averages 25 A. The existing analytical sweep covers 0.47, 0.68 and 1.0 uH at 400, 600 and 800 kHz.

The provisional center point remains 0.68 uH / 600 kHz because it yields approximately 6.54 A peak-to-peak inductor ripple, about 26.1% of the 25 A phase-average current. This is close to the conventional 30% ripple design coefficient used in TI's worked design procedure while avoiding the unsupported assumption that TI's example inductance transfers directly to FREEAXE.

This point is a **design-analysis center**, not an approved BOM selection. A real inductor must still pass saturation current, RMS current, DCR loss, temperature rise, footprint/height, supply-chain and conducted/radiated EMI checks at the final switching frequency.

## Freeze rule

Do not freeze the VCORE magnetics until all of these are known together:

1. final per-domain voltage range used by the four-BM1373 chain;
2. measured sustained and transient domain current;
3. selected TPS546D24S switching frequency and phase synchronization;
4. selected internal compensation setting and output capacitance/ESR network;
5. candidate inductor Isat and Irms ratings with thermal derating;
6. routed copper/via geometry and measured regulator/inductor temperature;
7. stable eight-chip accepted-share soak at the intended Air and Hydro operating points.

Air and Hydro continue to use the same electrical magnetics target unless physical thermal testing proves a variant-specific placement or derating requirement.