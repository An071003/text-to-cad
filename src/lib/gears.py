"""Watch Gear & Pinion Generator for build123d.

Provides parameterized functions to generate:
1. Horological toothed wheels with fine spokes, stepped rim, hub, and center hole.
2. High-precision steel pinions with leaves, arbors, and conical pivots.
"""

import math
from build123d import (
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Location,
    Locations,
    Mode,
    PolarLocations,
    Polygon,
    Rectangle,
    Rot,
    extrude,
    fillet,
)
from cadgen import srgb


def make_watch_wheel(
    teeth: int,
    module: float,
    rim_thickness: float = 0.20,
    hub_diameter: float = 1.20,
    arbor_hole: float = 0.50,
    spoke_count: int = 4,
    spoke_width: float = 0.35,
    recess_depth: float = 0.04,
):
    """Generate a realistic horological gear wheel with teeth, stepped rim, fine spokes, and hub."""
    pitch_radius = (teeth * module) / 2.0
    addendum = 0.95 * module
    dedendum = 1.25 * module
    outer_radius = pitch_radius + addendum
    root_radius = max(pitch_radius - dedendum, hub_diameter / 2.0 + 0.2)
    rim_inner_radius = root_radius - 0.40 * (root_radius - hub_diameter / 2.0)

    with BuildPart() as wheel:
        # Base outer disc with teeth root
        with BuildSketch():
            Circle(radius=outer_radius)
        extrude(amount=rim_thickness)

        # Cut tooth spaces (cycloidal approximation)
        tooth_cut_width = math.pi * module * 0.50  # Precise tooth-to-space ratio
        cut_depth = addendum + dedendum

        # Cut grooves for teeth
        with BuildSketch(Location((0, 0, 0))):
            with PolarLocations(radius=pitch_radius, count=teeth):
                Rectangle(tooth_cut_width, cut_depth * 1.4)
        extrude(amount=rim_thickness, mode=Mode.SUBTRACT)

        # Recessed web (stepped rim face for high-horology aesthetics)
        if recess_depth > 0 and root_radius > 1.8:
            with BuildSketch(Location((0, 0, rim_thickness - recess_depth))):
                Circle(radius=rim_inner_radius + 0.1)
                Circle(radius=hub_diameter / 2.0 + 0.15, mode=Mode.SUBTRACT)
            extrude(amount=recess_depth, mode=Mode.SUBTRACT)

        # Cut spoke openings if the wheel is large enough
        if root_radius > 1.8 and spoke_count > 0:
            window_r_mid = (rim_inner_radius + hub_diameter / 2.0 + 0.25) / 2.0
            window_dr = (rim_inner_radius - (hub_diameter / 2.0 + 0.25))
            with BuildSketch(Location((0, 0, 0))):
                with PolarLocations(radius=window_r_mid, count=spoke_count):
                    opening_w = (2.0 * math.pi * window_r_mid / spoke_count) - spoke_width
                    if opening_w > 0.35 and window_dr > 0.35:
                        Rectangle(opening_w, window_dr)
            extrude(amount=rim_thickness, mode=Mode.SUBTRACT)

        # Center arbor hole
        if arbor_hole > 0:
            with BuildSketch(Location((0, 0, 0))):
                Circle(radius=arbor_hole / 2.0)
            extrude(amount=rim_thickness, mode=Mode.SUBTRACT)

    part = wheel.part
    part.color = srgb("#E5C07B")  # Warm golden brass
    part.cad_material = {"roughness": 0.22, "metalness": 0.90}
    return part


def make_pinion(
    leaves: int,
    module: float,
    length: float = 1.20,
    arbor_diameter: float = 0.50,
    pivot_diameter: float = 0.16,
    pivot_length: float = 0.35,
):
    """Generate a horological steel pinion with polished leaves, arbor shaft, and conical pivots."""
    pitch_radius = (leaves * module) / 2.0
    addendum = 1.0 * module
    dedendum = 1.25 * module
    outer_radius = pitch_radius + addendum
    root_radius = max(pitch_radius - dedendum, arbor_diameter / 2.0 + 0.05)

    with BuildPart() as pinion:
        # Solid pinion body
        with BuildSketch():
            Circle(radius=outer_radius)
        extrude(amount=length)

        # Flutes between leaves
        flute_width = math.pi * module * 0.46
        with BuildSketch(Location((0, 0, 0))):
            with PolarLocations(radius=pitch_radius, count=leaves):
                Rectangle(flute_width, (addendum + dedendum) * 1.5)
        extrude(amount=length, mode=Mode.SUBTRACT)

        # Lower arbor pivot
        if pivot_diameter > 0 and pivot_length > 0:
            with BuildSketch(Location((0, 0, 0))):
                Circle(radius=pivot_diameter / 2.0)
            extrude(amount=-pivot_length)

        # Upper arbor pivot
        if pivot_diameter > 0 and pivot_length > 0:
            with BuildSketch(Location((0, 0, length))):
                Circle(radius=pivot_diameter / 2.0)
            extrude(amount=pivot_length)

    part = pinion.part
    part.color = srgb("#ECEFF4")  # Polished hardened steel
    part.cad_material = {"roughness": 0.12, "metalness": 0.96}
    return part
