from __future__ import annotations
import json
from pathlib import Path

def load_layout(path: str | Path):
    return json.loads(Path(path).read_text())

def rect(zone):
    return (zone["x_mm"], zone["y_mm"], zone["x_mm"]+zone["w_mm"], zone["y_mm"]+zone["h_mm"])

def overlaps(a,b):
    ax1,ay1,ax2,ay2=rect(a); bx1,by1,bx2,by2=rect(b)
    return max(ax1,bx1) < min(ax2,bx2) and max(ay1,by1) < min(ay2,by2)

def point_inside_board(x,y,board,margin=0):
    return margin <= x <= board["width_mm"]-margin and margin <= y <= board["height_mm"]-margin

def cooler_hole_pitch(holes):
    xs=sorted(set(round(p[0],6) for p in holes)); ys=sorted(set(round(p[1],6) for p in holes))
    if len(xs)!=2 or len(ys)!=2: raise ValueError("expected square four-hole pattern")
    return xs[1]-xs[0], ys[1]-ys[0]

def asic_envelope(asics, package_mm=(10.0,10.0)):
    hw,hh=package_mm[0]/2,package_mm[1]/2
    xs=[a["x_mm"] for a in asics]; ys=[a["y_mm"] for a in asics]
    return (min(xs)-hw,min(ys)-hh,max(xs)+hw,max(ys)+hh)

def envelope_size(env): return (env[2]-env[0],env[3]-env[1])

def minimum_vrm_to_asic_edge_gap(layout, domain):
    zone=layout["zones"]["domain_a_vrm_pair" if domain=="A" else "domain_b_vrm_pair"]
    asics=[a for a in layout["asics"] if a["domain"]==domain]
    package_h=layout["shared"]["asic_package_nominal_mm"][1]
    if domain=="A":
        asic_top=max(a["y_mm"]+package_h/2 for a in asics)
        return zone["y_mm"]-asic_top
    asic_bottom=min(a["y_mm"]-package_h/2 for a in asics)
    return asic_bottom-(zone["y_mm"]+zone["h_mm"])
