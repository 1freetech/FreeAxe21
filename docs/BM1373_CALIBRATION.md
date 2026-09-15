# FREEAXE 21 BM1373 calibration update — Run 11

## Concrete correction

The previous 21.52 TH/s Hydro number was derived from an 8-chip, 400 MHz frequency calculation. It is useful as a mathematical operating point, but it is not strong enough evidence for a current sustained-performance estimate. Run 11 therefore demotes that value from the sustained estimate.

The strongest public measured system anchor currently used by FREEAXE is a four-BM1373 Nexus S1 prototype independently reviewed at 10.3 TH/s locally after 15 minutes, 10.69 TH/s pool-side, and about 140 W at the wall. The review also reported approximately 55 dBA and hot regions around 78–82 C. This is still not a FREEAXE measurement and uses a different PCB, PSU and cooler, so only linear sensitivity calculations are permitted from it.

Eight-chip linearization of the measured local point gives 20.6 TH/s, 280 W wall, and 13.59 J/TH wall efficiency. At a provisional 90% PSU-to-board factor this corresponds to about 252 W board-side and 21 A from a 12 V input. These are design sensitivities, not guaranteed FREEAXE values.

The NMAxe firmware project reported on 2026-07-21 that its open BM1373 driver achieved approximately 6 TH/s per chip in testing. Eight chips would mathematically imply 48 TH/s, but no accompanying power, voltage, thermal or duration data are disclosed in that release note. FREEAXE therefore classifies it as evidence that large tuning headroom may exist, not as evidence for a sustained board rating.

## Revised sustained targets

- FREEAXE 21 Air: 20.0 TH/s current sustained-certification target. The 20.6 TH/s linearized anchor becomes its next validation point, not a guaranteed rating.
- FREEAXE 21 Hydro: 20.6 TH/s current best sustained estimate. The prior 30 TH/s objective remains experimental only.
- Any sustained claim above 20.6 TH/s now requires FREEAXE-specific accepted-share stability, wall/DC power, VRM temperature, ASIC/package temperature, and long-duration thermal soak measurements.

## Evidence classes

1. FREEAXE measured: highest authority, none exists yet.
2. Independently measured BM1373 system: current sustained-design anchor.
3. Open firmware/test claim without full conditions: tuning/ceiling evidence only.
4. Frequency-only or constant-efficiency extrapolation: engineering sensitivity only.

## Sources

- NMAxe BM1373 driver release evidence: https://github.com/NMminer1024/ESP-Miner-NMAxe
- Naja Duo open BM1373 reference, explicitly described as an untested prototype: https://github.com/bitaxeorg/naja-duo
- Independent Nexus S1 prototype review: https://thehobbyistminer.io/the-nexus-s1-surprised-everyone-with-10th-s-of-bm1373-power/
