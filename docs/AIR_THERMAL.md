# FREEAXE 21 Air revalidation

The Air cooler is revalidated against the current two-domain board and corrected 20 TH/s target.

At 25 C ambient the complete heatsink-to-air path must demonstrate <=0.1786 K/W at the
252 W reference load, and <=0.1125 K/W at the 400 W thermal design envelope to keep the
heatsink base at or below 70 C.

Primary fan: Delta QFR1212GHE, 120x120x38 mm, 6000 RPM, 210.38 CFM free-air,
29.18 mmH2O zero-flow static pressure, 21.6 W, 64 dBA.
High-pressure alternative: Delta PFR1212UHE, 6600 RPM, 228.65 CFM, 30.63 mmH2O,
32.4 W, 65.5 dBA.
A lower-noise Delta AFB1212HHE reference is 2900 RPM, 120.07 CFM, 9.0 mmH2O,
5.52 W and 44 dBA, but is not accepted for the 400 W envelope without measured thermal proof.

Delta explicitly states maximum airflow is measured in free air and maximum pressure at
zero airflow. Therefore neither endpoint is treated as the operating airflow. The final
fan operating point requires the heatsink/duct pressure-drop curve or physical measurement.

Bulk-air rise sensitivity at 400 W using actual airflow, not free-air rating:
{'50': 14.22, '75': 9.48, '100': 7.11, '125': 5.69, '150': 4.74}

Protection remains fail-closed for fan tach or sensor loss. Base >=65 C throttles and
>=70 C shuts down; VRM >=90 C throttles and >=100 C shuts down.

20 TH/s remains the Air sustained-certification target, not a certified sustained result.
