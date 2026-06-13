# -*- coding: utf-8 -*-
"""
Game of life script with animated evolution
"""
import conway
from pygame_viewer import run_pygame_life

N = 4096
CELL_SCALE = 2
VIEWPORT = (80, 336, 80, 336)


def main():
    """Animate the large gun in pygame using a cropped viewport."""
    life = conway.GameOfLife(N)
    # life.insertBlinker((0,0))
    # life.insertGlider((0,0))
    # life.insertGliderGun((0,0))
    # life.insertFromFile("dragon spaceship.cells", (0,100))
    # life.insertFromFile("ak94 gun.cells", (100,100))
    # life.insertFromFile("vacuumgun gun.cells", (100,100))
    # life.insertFromFile("stargate oscillator.cells", (100,100))
    # life.insertFromFile("7enginecordership spaceship.cells", (100,100))
    life.insertFromFile("3enginecordership gun 279x258.cells", (100, 100))

    # In a cellular automaton, a gun is a pattern with a main part that repeats periodically, like an oscillator,
    # and that also periodically emits spaceships. but here the gun is not emit periodically and the left end did not work.
    run_pygame_life(
        life,
        cell_scale=CELL_SCALE,
        fps=20,
        max_frames=24,
        viewport=VIEWPORT,
        title="Game of Life - Large Gun",
    )


if __name__ == "__main__":
    main()
