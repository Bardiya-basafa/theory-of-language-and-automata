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

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
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
        pass

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        # Student TODO: Setup control glider and input glider(s)
        pass

    def run_and_gate(self, input_a_present, input_b_present):
        """
        Run the AND gate simulation for a specific number of steps and return the output.
        
        Args:
            input_a_present (bool): Input A state.
            input_b_present (bool): Input B state.
            
        Returns:
            bool: True if output is active (e.g. glider/block formed in output region), False otherwise.
        """
        # Student TODO: Evolve simulation and evaluate output
        pass

    def run_not_gate(self, input_a_present):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.
        
        Args:
            input_a_present (bool): Input A state.
            
        Returns:
            bool: True if output is active, False otherwise.
        """
        # Student TODO: Evolve simulation and evaluate output
        pass
