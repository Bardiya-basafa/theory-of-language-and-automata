# -*- coding: utf-8 -*-
"""
Game of life simple script for checking init states and checking if the evolution is
implemented correctly.
"""
import conway
from pygame_viewer import run_pygame_life

N = 64
CELL_SCALE = 10


def main():
	"""Show the glider evolution in a pygame window."""
	life = conway.GameOfLife(N,fastMode=True)
	# life.insertBlinker((0,0))
	# life.insertGlider((0,0))        # It travels diagonally across the Life grid at a speed of c/4
	# life.insertGliderGun((0,0))     # Gosper glider gun consists of two queen bee shuttles stabilized by two blocks.
	# life.insertFromFile("pat-snail spaceship.cells", (0,30))
	# life.insertFromFile("pat-dragon spaceship.cells", (0,30))
	# life.insertFromFile("pat-ak94 gun.cells", (0,0))
	# life.insertFromFile("pat-vacuumgun gun.cells", (0,0))
	# life.insertFromFile("pat-stargate oscillator.cells", (0,0))
	# life.insertFromFile("pat-7enginecordership spaceship.cells", (0,0))

	run_pygame_life(life, cell_scale=CELL_SCALE, fps=8, max_frames=300, title="Game of Life - Glider Check")


if __name__ == "__main__":
	main()
