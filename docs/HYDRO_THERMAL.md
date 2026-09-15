# FREEAXE 21 Hydro revalidation

The Hydro thermal model was revalidated against the current two-domain board and corrected performance model.

At 1.5 L/min water-reference flow and 30 C inlet:
- 252 W derived rated-reference load: coolant rise 2.42 C; outlet 32.42 C.
- 400 W thermal design envelope: rise 3.85 C; outlet 33.85 C.
- 480 W electrical stress point: rise 4.62 C; outlet 34.62 C.

The 400 W radiator/heat-exchanger qualification target is now expressed as UA >= 40 W/K at a 35 C mean coolant / 25 C ambient test condition. This replaces reliance on radiator size labels.

The full-cluster copper cold plate remains >=70x40 mm over the ASICs only. VRMs are not trapped under the cold plate and require their own thermal path. Exact TIM bondline, contact pressure, microchannel geometry, pressure drop, pump operating point and ASIC junction-to-plate resistance remain unresolved rather than guessed.

Protection remains fail-closed: <0.5 L/min, pump tach loss, sensor fault, or >=45 C coolant outlet shuts hashing down; 0.5-1.0 L/min throttles.

No sustained FREEAXE thermal rating is claimed until physical soak and flow-loss tests exist.
