"""Dam-break wall geometry and quantum initial conditions."""

SIZE = 16
EAST = (1, 5, 8)
NORTH = (2, 5, 6)
SOUTH = (4, 7, 8)

# Each reservoir is a rectangle with power-of-two side lengths and aligned bounds.
# Walls are inclusive (x_min, x_max, y_min, y_max) rectangles.
CASES = {
    "01-narrow-gate": (
        "Narrow central gate", (4, 0, 4, 16), EAST,
        [(9, 10, 0, 6), (9, 10, 9, 15)],
    ),
    "02-full-collapse": (
        "Full dam collapse across the channel", (4, 4, 4, 4), EAST,
        [],
    ),
    "03-side-breach": (
        "Breach at one end", (4, 0, 4, 16), EAST,
        [(9, 10, 4, 15)],
    ),
    "04-twin-breaches": (
        "Twin breaching jets", (4, 0, 4, 16), EAST,
        [(9, 10, 0, 1), (9, 10, 5, 10), (9, 10, 14, 15)],
    ),
    "05-northbound-release": (
        "Northbound reservoir release", (0, 4, 16, 4), NORTH,
        [(0, 4, 9, 10), (11, 15, 9, 10)],
    ),
    "06-southbound-release": (
        "Southbound release through an offset breach", (8, 8, 8, 4), SOUTH,
        [(0, 8, 5, 6), (13, 15, 5, 6)],
    ),
    "07-staggered-dams": (
        "Staggered dams", (4, 0, 4, 16), EAST,
        [(8, 9, 0, 3), (8, 9, 10, 15), (12, 13, 0, 5), (12, 13, 12, 15)],
    ),
    "08-island-split": (
        "Breach flow splits around an island", (4, 0, 4, 16), EAST,
        [(8, 9, 0, 3), (8, 9, 12, 15), (12, 13, 6, 9)],
    ),
    "09-narrow-canal": (
        "Dam release into a straight canal", (4, 4, 4, 4), EAST,
        [(8, 9, 0, 3), (8, 9, 9, 15), (10, 15, 2, 3), (10, 15, 9, 10)],
    ),
    "10-offset-outlet": (
        "Release into a basin with an offset outlet", (4, 8, 4, 4), EAST,
        [(8, 9, 0, 6), (8, 9, 13, 15), (12, 13, 5, 13)],
    ),
}
