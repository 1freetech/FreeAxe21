# FREEAXE 21 Run 12 — corrected power-domain architecture

## Change

The prior candidate used four independently regulated two-ASIC series domains, each with a two-device TPS546D24S stack (eight regulators total). After Run 11 corrected the realistic eight-chip target to ~20.0 TH/s Air / ~20.6 TH/s Hydro and ~252 W provisional board-side power at the measured-anchor point, that architecture carried unnecessary regulator count and complexity.

The new candidate is **two independently regulated four-ASIC series domains**:

- D0: U1-U4 in series, powered by VRM0A + VRM0B as a stacked TPS546D24S pair.
- D1: U5-U8 in series, powered by VRM1A + VRM1B as a stacked TPS546D24S pair.
- Total: four TPS546D24S devices for eight ASICs.

This remains a candidate, not a proven BM1373 topology.

## Why the voltage window works mathematically

ESP-Miner's present BM1373 voltage menu spans 1000-1250 mV per chip. Four series ASICs therefore imply a 4.0-5.0 V domain command. TI specifies TPS546D24S VOUT up to 5.5 V through PMBus, so the full present firmware voltage menu fits inside the regulator's published output range.

## Conservative current sizing

The calculation intentionally treats all board power as VCORE load. This overstates actual VCORE current because ESP32, fans/pump, auxiliary converters and other losses are not subtracted.

At 1.00 V/chip (4.0 V/domain):

| Total board-power envelope | Per-domain power | Per-domain current | 80 A stack utilization |
|---:|---:|---:|---:|
| 252 W | 126 W | 31.5 A | 39.4% |
| 400 W | 200 W | 50.0 A | 62.5% |
| 480 W | 240 W | 60.0 A | 75.0% |

The 400 W row is the existing thermal design envelope, not an actual expected FREEAXE 21 draw. The 480 W row is only a sensitivity check.

## Evidence classes

**Manufacturer sourced:** TPS546D24S is a 40 A converter; TI supports stacking 2-4 devices up to 160 A, output command down to 0.25 V/up to 5.5 V, and PMBus output-current/output-voltage/internal-temperature telemetry.

**Open reference:** Gamma Hex uses six BM1370 ASICs arranged as two domains of three with a four-phase TPS546D24S regulator. This proves that the Bitaxe ecosystem uses multi-ASIC series voltage domains and stacked TPS546D24S regulation, but not that BM1373 will tolerate four ASICs per domain.

**Open prototype:** Naja Duo uses two BM1373 ASICs and its BOM contains two TPS546D24S parts. Its own README says the board is untested, so it remains a pinout/topology clue rather than validation.

**Derived:** the two-domain/four-chip arrangement, 4.0-5.0 V domain window, and current/headroom calculations are FREEAXE engineering derivations.

## Downstream invalidation

This upstream architecture change invalidates downstream assumptions that still encode four VCORE domains or eight TPS546D24S devices. The next engineering dependency is therefore PCB placement/dimensions again, followed by current-path, copper/VRM, control/level shifting, and thermal review. Manufacturing output remains blocked.
