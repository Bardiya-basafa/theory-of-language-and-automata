import conway

from pygame_viewer import run_pygame_life

N = 100
CELL_SCALE = 10


def main():
    """Run the dragon spaceship demo in pygame."""
    life = conway.GameOfLife(N)
    # life.insertBlinker((0,0))
    # life.insertGlider((0,0))
    # life.insertGliderGunFixed((0,0))
    # life.insertFromFile("snail spaceship.cells", (0,30))
    #life.insertFromFile("dragon spaceship.cells", (0, 30))
    life.insertFromFile("ak94 gun.cells", (0, 0))
    # life.insertFromFile("vacuumgun gun.cells", (0,0))

    run_pygame_life(life, cell_scale=CELL_SCALE, fps=20, title="Game of Life - Dragon Spaceship")


if __name__ == "__main__":
    main()
