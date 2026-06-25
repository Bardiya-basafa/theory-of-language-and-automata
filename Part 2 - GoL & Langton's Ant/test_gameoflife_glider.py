"""
Game of life script with animated evolution
"""

import conway
from pygame_viewer import run_pygame_life

N = 200
CELL_SCALE = 8


def main():
    """Animate the vacuum gun in pygame."""
    life = conway.GameOfLife(N, fastMode=True)
    # life.insertBlinker((40, 40))
    # life.insertGlider((40,40))
    # life.insertGliderP60((40, 40), rotate=270)
    # life.insertBlock((10,10))
    # life.insertEater((10,10))
    # life.insertReflector((10,10))
    # life.insertGliderGun((0,0))
    # life.insertFromFile("pat-snail spaceship.cells", (0, 20))
    # life.insertFromFile("pat-dragon spaceship.cells", (10, 30))
    # life.insertFromFile("pat-ak94 gun.cells", (0,0))
    # life.insertFromFile("pat-vacuumgun gun.cells", (0,0))
    # life.insertFromFile("pat-test.rle", (0,0))
    # life.insertFromFile("pat-pulsar.rle", (50, 50))
    # life.insertFromFile("pat-pulsar.cells", (50,50))

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
