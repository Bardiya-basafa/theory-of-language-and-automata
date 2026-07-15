# -*- coding: utf-8 -*-

"""Pygame visualizer for Langton's Ant.

This script uses the existing langton.py module for the simulation logic and
renders the grid plus the ant position in a pygame window.
"""

import argparse

import numpy as np
import pygame

from langton import LangtonsAnt

DEFAULT_RULES = {
    0: (1, "R"),
    1: (0, "L"),
}

MULTI_COLOR_RULES = {
    0: (1, "R"),
    1: (2, "L"),
    2: (3, "R"),
    3: (0, "L"),
}


CARDIOID_RULES = {
    0: (1, "L"),
    1: (2, "L"),
    2: (3, "R"),
    3: (0, "R"),
}

MAZE = {
    0: (1, "R"),
    1: (2, "L"),
    2: (3, "L"),
    3: (0, "R"),
}


GROWING_TRIANGLE_RULES = {
    0: (1, "R"),
    1: (2, "R"),
    2: (3, "L"),
    3: (4, "L"),
    4: (5, "L"),
    5: (6, "R"),
    6: (7, "L"),
    7: (8, "L"),
    8: (9, "L"),
    9: (10, "R"),
    10: (11, "R"),
    11: (0, "R"),
}


LOGARITHMIC_SPIRAL_RULES = {
    0: (1, "R"),
    1: (2, "L"),
    2: (3, "L"),
    3: (4, "L"),
    4: (5, "L"),
    5: (6, "R"),
    6: (7, "R"),
    7: (8, "R"),
    8: (9, "L"),
    9: (10, "L"),
    10: (11, "L"),
    11: (0, "R"),
    }


ARCHIMEDES_SPIRAL_RULES = {
    0: (1, "L"),
    1: (2, "R"),
    2: (3, "R"),
    3: (4, "R"),
    4: (5, "R"),
    5: (6, "L"),
    6: (7, "L"),
    7: (8, "L"),
    8: (9, "R"),
    9: (10, "R"),
    10: (0, "R"),
    }


PALETTE = [
    (8, 10, 20),        
    (245, 245, 245),    
    (66, 165, 245),     
    (255, 90, 95),      
    (80, 210, 130),     
    (190, 100, 255),    
    (255, 205, 60),     
    (40, 220, 210),     
    (255, 135, 50),     
    (255, 90, 190),     
    (120, 145, 255),    
    (175, 230, 70),     
    (220, 120, 75),     
    (120, 220, 255),    
]

def build_surface(grid, cell_scale, ant_position=None, ant_color=(220, 40, 40)):
    """Convert the ant grid into a pygame surface."""
    rows, cols = grid.shape
    surface = pygame.Surface((cols * cell_scale, rows * cell_scale))

    for r in range(rows):
        for c in range(cols):
            state = int(grid[r, c])
            color = PALETTE[state % len(PALETTE)]
            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(c * cell_scale, r * cell_scale, cell_scale, cell_scale),
            )

    if ant_position is not None:
        ant_r, ant_c = ant_position
        center = (
            ant_c * cell_scale + cell_scale // 2,
            ant_r * cell_scale + cell_scale // 2,
        )
        radius = max(2, cell_scale // 3)
        pygame.draw.circle(surface, ant_color, center, radius)

    return surface


def run_visualizer(ant, cell_scale=6, fps=60, max_steps=None, title="Langton's Ant"):
    """Run the pygame event loop for a Langton's Ant simulation."""
    pygame.init()

    grid = ant.get_states()
    screen = pygame.display.set_mode(
        (grid.shape[1] * cell_scale, grid.shape[0] * cell_scale)
    )
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()

    finished = False
    steps = 0
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        surface = build_surface(
            grid, cell_scale, ant_position=ant.get_current_position()
        )
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        ant.step()
        grid = ant.get_states()
        for _ in range(100):
            ant.step()
        if max_steps is not None and steps >= max_steps:
            finished = True

        clock.tick(fps)

    pygame.quit()


def parse_args():
    """Parse command-line options for the visualizer."""
    parser = argparse.ArgumentParser(description="Langton's Ant pygame visualizer")
    parser.add_argument("--size", type=int, default=300, help="Grid size (NxN)")
    parser.add_argument("--row", type=int, default=None, help="Starting row")
    parser.add_argument("--col", type=int, default=None, help="Starting column")
    parser.add_argument(
        "--cell-scale", type=int, default=3, help="Pixel scale per cell"
    )
    parser.add_argument("--fps", type=int, default=100000, help="Frames per second")
    parser.add_argument(
        "--steps", type=int, default=None, help="Maximum simulation steps"
    )
    parser.add_argument(
        "--multi-color",
        action="store_true",
        help="Use a simple four-color rule set instead of the default two-color rule set",
    )
    return parser.parse_args()


def main():
    """Create the ant and launch the visualizer."""
    args = parse_args()
    start_row = args.row if args.row is not None else args.size // 2
    start_col = args.col if args.col is not None else args.size // 2
    rules = ARCHIMEDES_SPIRAL_RULES

    ant = LangtonsAnt(args.size, (start_row, start_col), rules)
    run_visualizer(
        ant,
        cell_scale=args.cell_scale,
        fps=args.fps,
        max_steps=args.steps,
        title="Langton's Ant",
    )


if __name__ == "__main__":
    main()
