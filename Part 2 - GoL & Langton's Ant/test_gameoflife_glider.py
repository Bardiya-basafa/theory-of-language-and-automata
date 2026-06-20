"""
Game of life script with animated evolution
"""

import conway
from pygame_viewer import run_pygame_life

N = 64
CELL_SCALE = 10


def main():
    """Animate the vacuum gun in pygame."""
    life = conway.GameOfLife(N, fastMode=True)
    # life.insertBlinker((0, 0))
    life.insertGlider((0,0))
    # life.insertGliderGun((0,0))
    # life.insertFromFile("snail spaceship.cells", (0,20))
    # life.insertFromFile("dragon spaceship.cells", (0, 30))
    # life.insertFromFile("ak94 gun.cells", (0,0))
    # life.insertFromFile("vacuumgun gun.cells", (0,0))
    # life.insertFromFile("test.rle", (0,0))
    # life.insertFromFile("pulsar.rle", (0, 0))
    # life.insertFromFile("pulsar.cells", (0,0))

    # In a cellular automaton, a gun is a pattern with a main part that repeats periodically, like an oscillator,
    # and that also periodically emits spaceships. but here the gun is not emit periodically and the left end did not work.
    run_pygame_life(
        life,
        cell_scale=CELL_SCALE,
        fps=20,
        max_frames=240,
        title="Game of Life - Vacuum Gun",
    )


if __name__ == "__main__":
    main()
