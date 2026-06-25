"""
Game of life script for simulating logic gates
"""

from logic_gates import GliderLogicGates
from pygame_viewer import run_pygame_life

N = 400
CELL_SCALE = 4


def main():
    """
    Animated logic gates
    """
    life = GliderLogicGates(N=N)

    life.setup_not_gate(True)

    run_pygame_life(
        life.gol,
        cell_scale=CELL_SCALE,
        fps=60,
        max_frames=400,
        title="Game of Life - Logic gates",
    )


if __name__ == "__main__":
    main()
