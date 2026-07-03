# -*- coding: utf-8 -*-
"""
Langton's Ant with Multi-color Rulesets support.
"""

import numpy as np


class LangtonsAnt:
    """
    Enhanced Langton's Ant supporting multi-color rulesets (e.g., "RLR", "LLRR", "LRRRRRLLR").
    """

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.

        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict or str): Dictionary mapping {color: (next_color, 'R'/'L')}
                                 OR a ruleset string like "RLR", "LLRR", "LARRRRRLLR".
        """
        self.grid = np.zeros((N, N), np.uint8)
        self.N = N
        self.ant_position = ant_position
        self.current_dir = "U"  # Possible directions: 'U', 'R', 'D', 'L'

        # Convert string ruleset to the standardized transition dictionary
        if isinstance(rules, str):
            self.rules = {}
            num_colors = len(rules)
            for i, turn in enumerate(rules):
                next_color = (i + 1) % num_colors
                self.rules[i] = (next_color, turn.upper())
        else:
            self.rules = rules

    def get_states(self):
        """
        Returns the current state grid of the cells.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        """
        return self.ant_position

    def step(self):
        """
        Perform a single simulation step following the multi-color ruleset.
        """
        r, c = self.ant_position
        current_color = self.grid[r, c]

        # Retrieve next color state and turn direction
        next_color, turn_direction = self.rules[current_color]

        # Toggle/update color of the current square
        self.grid[r, c] = next_color

        # 1. Update ant orientation (turn R or L)
        dirs_clockwise = ["U", "R", "D", "L"]
        curr_idx = dirs_clockwise.index(self.current_dir)

        if turn_direction == "R":
            self.current_dir = dirs_clockwise[(curr_idx + 1) % 4]
        elif turn_direction == "L":
            self.current_dir = dirs_clockwise[(curr_idx - 1) % 4]

        # 2. Move forward one unit in the new direction
        if self.current_dir == "U":
            r -= 1
        elif self.current_dir == "D":
            r += 1
        elif self.current_dir == "R":
            c += 1
        elif self.current_dir == "L":
            c -= 1

        # Apply toroidal wrapping
        self.ant_position = (r % self.N, c % self.N)

    def update(self):
        """
        Alias for step() to support standard animation/engine.
        """
        self.step()
