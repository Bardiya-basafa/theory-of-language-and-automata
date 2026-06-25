# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.

"""

import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
    TODO: [Extension - Logic Gates]
    Instruct the student to:
    1. Initialize a grid and precisely place "Glider" streams (signals represented by gliders)
       such that their collision simulates:
       - An AND gate (produces a specific output pattern only when both inputs A and B are active).
       - A NOT gate (produces an output signal/glider only when input A is inactive).
    2. Prove the Turing completeness of Conway's Game of Life by demonstrating these logic gates.
    """

    def __init__(self, N=35, finite=False, fastMode=True):
        self.gol = GameOfLife(N=N, finite=finite, fastMode=fastMode)

    def setup_and_gate(self, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.

        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            input_b_present (bool): If True, place glider for Input B.

        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        # Student TODO: Setup glider(s) on the grid

        # Input A gun
        if input_a_present:
            self.gol.insertGliderGun((40, 5))

        # Input B gun
        if input_b_present:
            self.gol.insertGliderGun((5, 80))

        # reflect A stream toward collision
        self.gol.insertReflector((70, 40))

        # reflect B stream
        self.gol.insertReflector((40, 110))

        # collision target area
        # output glider emerges only if both arrive
        self.gol.insertBlock((100, 100))
        self.gol.insertBlock((110, 120))

    def setup_not_gate(self, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.

        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.

        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        # Student TODO: Setup control glider and input glider(s)
        if input_a_present:
            self.gol.insertGliderGun(index=(42, 40))

        self.gol.insertFromFile("not gate.cells", index=(60, 65))
