# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""

import numpy as np


class LangtonsAnt:
    """
    Create the LangtonsAnt class.

    Instruct students to:
    1. Implement the core rules:
       - If on a white square, toggle the color of the square and turn 90 degrees clockwise ('R'), then move forward one unit.
       - If on a black square, toggle the color of the square and turn 90 degrees counter-clockwise ('L'), then move forward one unit.
    2. Extend it to handle multi-color states (representing rulesets like RLR, LLRR, LRRRRRLLR, etc.).
       - A ruleset dictionary maps: {current_color: (next_color, turn_direction)}
       - Where turn_direction is 'R' or 'L'.
    3. Ensure wrapping at the boundaries (toroidal grid).
    """

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.

        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        self.grid = np.zeros((N, N), np.uint8)
        self.N = N
        self.ant_position = ant_position
        self.rules = rules
        self.current_dir = "U"

    def get_states(self):
        """
        Returns the current state grid of the cells.

        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).

        Returns:
            tuple: Current coordinates of the ant.
        """
        return self.ant_position

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        """
        r = self.ant_position[0]
        c = self.ant_position[1]
        color = self.grid[r, c]
        next_color, directions = self.rules[color]
        self.grid[r, c] = next_color
        # calculating the next postintion using current position
        for dir in list(directions):
            if dir == "R":
                if self.current_dir == "U":
                    c += 1
                    self.current_dir = "R"

                elif self.current_dir == "R":
                    r += 1
                    self.current_dir = "D"

                elif self.current_dir == "D":
                    c -= 1
                    self.current_dir = "L"

                elif self.current_dir == "L":
                    r -= 1
                    self.current_dir = "U"

            elif dir == "L":
                if self.current_dir == "U":
                    c -= 1
                    self.current_dir = "L"

                elif self.current_dir == "R":
                    r -= 1
                    self.current_dir = "U"

                elif self.current_dir == "D":
                    c += 1
                    self.current_dir = "R"

                elif self.current_dir == "L":
                    r += 1
                    self.current_dir = "D"

        self.ant_position = (r % self.N, c % self.N)

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()
