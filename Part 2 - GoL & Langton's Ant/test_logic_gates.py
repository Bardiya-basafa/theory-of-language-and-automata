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
    life = GliderLogicGates()

    # life.setup_not_gate(False)
    lf = life.setup_and_gate(grid_size=200, input_a_present=True, input_b_present=True)
    lf2 = life.setup_not_gate(grid_size=200, input_a_present=False)
    # life.setup_not_gate(True)

    run_pygame_life(
        lf2,
        cell_scale=CELL_SCALE,
        fps=60,
        max_frames=10000,
        title="Game of Life - Logic gates",
    )


if __name__ == "__main__":
    main()
