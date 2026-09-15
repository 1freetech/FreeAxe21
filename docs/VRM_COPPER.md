# Run 15 — two-domain VRM/copper refinement

This run updates dependency 5 after the power architecture changed to two four-ASIC domains.

The provisional VCORE copper geometry is 15 mm long, two parallel 2 oz copper layers,
20 mm effective width per layer. At 80 C copper the analytical path results are:

- 31.5 A/domain: 3.60 mV drop, 0.113 W loss
- 50.0 A/domain: 5.71 mV drop, 0.285 W loss
- 60.0 A/domain: 6.85 mV drop, 0.411 W loss

The 60 A point is a stress/qualification ceiling, not an expected operating current.
It is 75% of the 80 A nameplate capability of a two-device TPS546D24S stack.
The 400 W thermal envelope corresponds to 50 A/domain at a 4.0 V domain rail.

These numbers are bulk-copper calculations only. They do not include via constriction,
pad current crowding, spreading resistance, inductor DCR, regulator switching/conduction
loss, capacitor ripple, or PCB-to-air thermal resistance. Manufacturing remains blocked
until the exact stackup, routed polygons, vias, magnetics, compensation and thermal
measurements exist.
