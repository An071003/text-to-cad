"""Watch Gear & Pinion Generator for build123d.

Provides parameterized functions to generate:
1. Horological toothed wheels with spokes, rim, hub, and center hole.
2. High-precision pinions with leaves and arbors.
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


def make_watch_wheel(
    teeth: int,
    module: float,
    rim_thickness: float = 0.20,
    hub_diameter: float = 1.20,
    arbor_hole: float = 0.50,
    spoke_count: int = 4,
    spoke_width: float = 0.40,
    recess_depth: float = 0.0,
):
    """Generate a realistic horological gear wheel with teeth, rim, spokes, and hub."""
    pitch_radius = (teeth * module) / 2.0
    addendum = 0.95 * module
    dedendum = 1.25 * module
    outer_radius = pitch_radius + addendum
    root_radius = max(pitch_radius - dedendum, hub_diameter / 2.0 + 0.2)
    rim_inner_radius = root_radius - 0.45 * (root_radius - hub_diameter / 2.0)

    with BuildPart() as wheel:
        # Base outer disc with teeth root
        with BuildSketch():
            Circle(radius=outer_radius)
        extrude(amount=rim_thickness)

        # Cut tooth spaces
        tooth_angle = 360.0 / teeth
        tooth_cut_width = math.pi * module * 0.52  # Space between teeth
        cut_depth = addendum + dedendum

        # Cut grooves for teeth
        with BuildSketch(wheel.faces().sort_by().last):
            with PolarLocations(radius=pitch_radius, count=teeth):
                Rectangle(tooth_cut_width, cut_depth * 1.5)
        extrude(amount=-rim_thickness, mode=Mode.SUBTRACT)

        # Cut spoke openings if the wheel is large enough (root_radius > 1.8 mm)
        if root_radius > 1.8 and spoke_count > 0:
            window_r_mid = (rim_inner_radius + hub_diameter / 2.0 + 0.3) / 2.0
            window_dr = (rim_inner_radius - (hub_diameter / 2.0 + 0.3))
            with BuildSketch(wheel.faces().sort_by().last):
                with PolarLocations(radius=window_r_mid, count=spoke_count):
                    # Circular sector opening approximation
                    opening_w = (2.0 * math.pi * window_r_mid / spoke_count) - spoke_width
                    if opening_w > 0.4 and window_dr > 0.4:
                        Rectangle(opening_w, window_dr)
            extrude(amount=-rim_thickness, mode=Mode.SUBTRACT)

        # Center arbor hole
        if arbor_hole > 0:
            with BuildSketch(wheel.faces().sort_by().last):
                Circle(radius=arbor_hole / 2.0)
            extrude(amount=-rim_thickness, mode=Mode.SUBTRACT)

    return wheel.part


def make_pinion(
    leaves: int,
    module: float,
    length: float = 1.20,
    arbor_diameter: float = 0.50,
    pivot_diameter: float = 0.15,
    pivot_length: float = 0.30,
):
    """Generate a horological pinion with leaves, arbor shaft, and fine pivots."""
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
        flute_width = math.pi * module * 0.48
        with BuildSketch(pinion.faces().sort_by().last):
            with PolarLocations(radius=pitch_radius, count=leaves):
                Rectangle(flute_width, (addendum + dedendum) * 1.5)
        extrude(amount=-length, mode=Mode.SUBTRACT)

        # Lower arbor pivot
        if pivot_diameter > 0 and pivot_length > 0:
            with BuildSketch(pinion.faces().sort_by().first):
                Circle(radius=pivot_diameter / 2.0)
            extrude(amount=-pivot_length)

        # Upper arbor pivot
        if pivot_diameter > 0 and pivot_length > 0:
            with BuildSketch(pinion.faces().sort_by().last):
                Circle(radius=pivot_diameter / 2.0)
            extrude(amount=pivot_length)

    return pinion.part
