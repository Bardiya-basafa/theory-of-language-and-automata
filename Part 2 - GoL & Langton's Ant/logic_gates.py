import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
    Visual demonstration of logic gates using Conway's Game of Life.

    - Inputs are gliders inserted at fixed positions.
    - A Gosper glider gun provides a periodic stream of gliders.
    - Eaters and blocks are used to absorb or redirect gliders.
    - Output is detected by checking whether any live cells appear
      in a fixed “output region” of the grid.
    """

    # Positions are tuned for an N ≈ 400 grid
    INPUT_A_POS = (220, 80)
    INPUT_B_POS = (260, 80)
    OUTPUT_REGION_CENTER = (200, 300)

    def __init__(self, N: int = 400):
        """
        Initialize logic gates on an N×N Game of Life grid.
        """
        self.N = N
        self.gol = GameOfLife(N)

    # ----------------------------------------------------------------------
    # Utility helpers
    # ----------------------------------------------------------------------
    def reset(self) -> GameOfLife:
        """
        Reset the underlying GameOfLife instance to a clean grid.
        Keeps N and recreates the GameOfLife object.
        """
        self.gol = GameOfLife(self.N)
        return self.gol

    def _insert_pattern(self, pattern: np.ndarray, index: tuple[int, int]) -> None:
        """
        Insert a binary 2D pattern into self.gol.grid at (row, col),
        clipping safely at boundaries and preserving already-alive cells
        via np.maximum.

        Parameters
        ----------
        pattern : np.ndarray
            2D array of 0/1 representing a Life pattern.
        index : (row, col)
            Top-left insertion index on the grid.
        """
        if pattern is None:
            return

        grid = self.gol.grid
        rows, cols = grid.shape
        pr, pc = pattern.shape
        row, col = index

        # Compute safe slice inside grid
        r_start = max(row, 0)
        c_start = max(col, 0)
        r_end = min(row + pr, rows)
        c_end = min(col + pc, cols)

        # If completely out of bounds, nothing to do
        if r_start >= r_end or c_start >= c_end:
            return

        # Corresponding slice in pattern
        pr_start = r_start - row
        pc_start = c_start - col
        pr_end = pr_start + (r_end - r_start)
        pc_end = pc_start + (c_end - c_start)

        subgrid = grid[r_start:r_end, c_start:c_end]
        subpattern = pattern[pr_start:pr_end, pc_start:pc_end]

        # Preserve any already alive cells
        grid[r_start:r_end, c_start:c_end] = np.maximum(subgrid, subpattern)

    # ----------------------------------------------------------------------
    # Primitive patterns
    # ----------------------------------------------------------------------
    def _glider_pattern(self) -> np.ndarray:
        """
        A basic 3×3 glider pattern that moves roughly down-right.

        Orientation can be tuned; here we choose a common variant:
        . 1 .
        . . 1
        1 1 1
        """
        return np.array(
            [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1],
            ],
            dtype=int,
        )

    def _gosper_gun_pattern(self) -> np.ndarray:
        """
        Gosper glider gun pattern as a 2D numpy array.
        This is a standard encoding; orientation is chosen so that
        the gun shoots gliders to the right.
        """
        # Representation adapted to a compact 2D array.
        gun = np.zeros((11, 38), dtype=int)

        # Left block
        coords = [
            (5, 1),
            (5, 2),
            (6, 1),
            (6, 2),
        ]

        # Right block
        coords += [
            (3, 35),
            (3, 36),
            (4, 35),
            (4, 36),
        ]

        # Central gun structure
        coords += [
            (5, 11),
            (5, 12),
            (6, 11),
            (6, 12),
            (4, 13),
            (3, 14),
            (3, 15),
            (4, 17),
            (5, 18),
            (6, 18),
            (7, 17),
            (5, 16),
            (6, 16),
        ]

        # Right emitter
        coords += [
            (3, 21),
            (4, 21),
            (5, 21),
            (3, 22),
            (4, 22),
            (5, 22),
            (2, 23),
            (6, 23),
            (1, 25),
            (2, 25),
            (6, 25),
            (7, 25),
            (3, 35),
            (4, 35),
            (2, 35),
            (5, 35),
        ]

        for r, c in coords:
            if 0 <= r < gun.shape[0] and 0 <= c < gun.shape[1]:
                gun[r, c] = 1

        return gun

    def _eater_pattern(self) -> np.ndarray:
        """
        A small eater-like pattern (Eater 1) that absorbs gliders.
        """
        eater = np.zeros((4, 4), dtype=int)
        coords = [
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 1),
            (2, 2),
            (3, 2),
        ]
        for r, c in coords:
            eater[r, c] = 1
        return eater

    def _reflector_block_pattern(self) -> np.ndarray:
        """
        Simple 2×2 block, used as a stable reflector/obstruction.
        """
        return np.array(
            [
                [1, 1],
                [1, 1],
            ],
            dtype=int,
        )

    # ----------------------------------------------------------------------
    # Pattern insertion wrappers
    # ----------------------------------------------------------------------
    def insert_glider(self, index: tuple[int, int] = (0, 0)) -> None:
        """
        Insert a glider pattern at a given position on the grid.
        """
        self._insert_pattern(self._glider_pattern(), index)

    def insert_gun(self, index: tuple[int, int] = (0, 0)) -> None:
        """
        Insert a Gosper glider gun at a given position.
        """
        self._insert_pattern(self._gosper_gun_pattern(), index)

    def insert_eater(self, index: tuple[int, int] = (0, 0)) -> None:
        """
        Insert an eater (glider absorber) at a given position.
        """
        self._insert_pattern(self._eater_pattern(), index)

    def insert_reflector_block(self, index: tuple[int, int] = (0, 0)) -> None:
        """
        Insert a small 2×2 block reflector/obstruction.
        """
        self._insert_pattern(self._reflector_block_pattern(), index)

    # ----------------------------------------------------------------------
    # Gate setups
    # ----------------------------------------------------------------------
    def setup_not_gate(self, input_a_present: bool) -> GameOfLife:
        """
        Visual NOT gate:

        - A glider gun sends a stream of gliders toward an output region.
        - If input A is *absent* (False), the stream continues and
          gliders reach the output region.
        - If input A is *present* (True), a glider is inserted that
          interferes with the stream, killing or diverting it, so
          output gliders do not reach the region.

        Parameters
        ----------
        input_a_present : bool
            Whether input A glider is present.

        Returns
        -------
        GameOfLife
            The underlying GameOfLife instance, ready to be evolved.
        """
        # Fresh grid
        self.reset()

        # Main gun aiming roughly rightwards
        self.insert_gun((200, 50))

        # Eater that cleans excess gliders further down the path
        self.insert_eater((210, 180))

        # Reflector block used to enforce geometry
        self.insert_reflector_block((190, 200))

        # Input A glider: if present, it disrupts the gun’s stream
        if input_a_present:
            self.insert_glider(self.INPUT_A_POS)

        return self.gol

    def setup_and_gate(
        self, input_a_present: bool, input_b_present: bool
    ) -> GameOfLife:
        """
        Visual AND gate:

        - A glider gun provides a periodic source.
        - Two input gliders A و B در مسیرهای جداگانه وارد می‌شوند.
        - فقط زمانی که هر دو هم‌زمان حضور داشته باشند، هندسهٔ
          برخوردها اجازه می‌دهد یک گلایدر به ناحیهٔ خروجی برسد.
        - اگر یکی از ورودی‌ها نباشد، یا گلایدر مربوطه حذف می‌شود
          یا برخوردها باعث نابودی خروجی می‌شوند.

        Parameters
        ----------
        input_a_present : bool
            Presence of input A glider.
        input_b_present : bool
            Presence of input B glider.

        Returns
        -------
        GameOfLife
            The underlying GameOfLife instance with gate set up.
        """
        # Fresh grid
        self.reset()

        # Main gun
        self.insert_gun((280, 100))

        # Inputs
        if input_a_present:
            self.insert_glider(self.INPUT_A_POS)
        if input_b_present:
            self.insert_glider(self.INPUT_B_POS)

        # Geometry: reflectors and eaters tuned to roughly act as AND
        self.insert_reflector_block((240, 160))
        self.insert_reflector_block((260, 180))

        self.insert_eater((250, 220))
        self.insert_eater((270, 220))

        return self.gol

    # ----------------------------------------------------------------------
    # Output detection
    # ----------------------------------------------------------------------
    def has_output_glider(self, window_radius: int = 8) -> bool:
        """
        Check whether there is any live cell near the output region center.

        This is a coarse detection: we don't identify a perfect glider
        pattern, just any activity in a window around OUTPUT_REGION_CENTER.

        Parameters
        ----------
        window_radius : int
            Radius of the square window around OUTPUT_REGION_CENTER.

        Returns
        -------
        bool
            True if any cell is alive in the window, False otherwise.
        """
        grid = self.gol.grid
        rows, cols = grid.shape
        center_r, center_c = self.OUTPUT_REGION_CENTER

        r_start = max(center_r - window_radius, 0)
        r_end = min(center_r + window_radius + 1, rows)
        c_start = max(center_c - window_radius, 0)
        c_end = min(center_c + window_radius + 1, cols)

        window = grid[r_start:r_end, c_start:c_end]
        return np.any(window)
