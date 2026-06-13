# Part 2: Cellular Automata - Conway's Game of Life and Langton's Ant

This part explores cellular automata as models of computation, demonstrating how simple local rules generate complex global behavior and ultimately universal computation.

## Overview

**Cellular Automata** are mathematical models consisting of a grid of cells, each with a finite set of states. The evolution of the entire system follows deterministic rules based on each cell's current state and its neighbors' states.

This part demonstrates emergence - a phenomenon where complex patterns and behaviors arise from simple local interactions. Remarkably, some cellular automata are Turing complete, capable of simulating any computable process.

This part consists of three main sections:

1. **Conway's Game of Life**: A famous two-dimensional cellular automaton with simple rules but complex behavior
2. **Langton's Ant**: A simpler cellular automaton representing a 2D Turing machine with chaotic yet structured dynamics
3. **Turing Completeness**: Building digital logic gates within Game of Life to prove universal computation

## Project Components

### File Structure

```
Part 2 - GoL & Langton's Ant/
├── conway.py                      # Game of Life implementation
├── langton.py                     # Langton's Ant implementation
├── langton_pygame.py              # GUI for Langton's Ant visualization
├── logic_gates.py                 # Logic gates using Game of Life gliders
├── pygame_gol.py                  # GUI for Game of Life visualization
├── pygame_viewer.py               # Pattern viewer utility
├── test_gameoflife_glider_simple.py
├── test_gameoflife_glider.py
├── test_gameoflife_glider_large.py
├── *.cells                        # Pattern files (RLE and Plaintext formats)
│   ├── ak94 gun.cells
│   ├── 3enginecordership gun 279x258.cells
│   ├── 7enginecordership spaceship.cells
│   ├── dragon spaceship.cells
│   ├── vacuumgun gun.cells
│   └── stargate oscillator.cells
├── doc.pdf                        # Original project documentation
└── README.md                      # This file
```

### Pattern Files

The `.cells` files contain pre-designed patterns in:
- **Plaintext format** (.cells): Simple 'b' (dead) and 'o' (alive) representations
- **RLE format** (.rle): Run-Length Encoded for compact storage of large patterns

These can be loaded into the simulator for visualization and study.

## Mathematical Foundations

### Cellular Automaton State Function

For a cell at position (i,j) in an N x N grid:

```
State at time t: s_t(c) ∈ {0, 1}
  0 = dead cell
  1 = alive cell

State transition function: δ: S^k × S → S
  where S = {0, 1} (state space)
  k = number of neighbors (typically 8 for Moore neighborhood)

Next state: s_{t+1}(c) = δ(s_t(c), Σ s_t(n) for n in Neighborhood(c))
```

The entire cellular automaton evolves synchronously - all cells update simultaneously based on the previous generation.

## Section 1: Conway's Game of Life

### Objective

Implement a complete Game of Life simulator in `conway.py` that supports:
- 2D grid evolution with Moore neighborhood (8-connected)
- Support for both finite and toroidal (wrapping) boundary conditions
- Efficient computation using convolution for large grids
- Pattern loading from RLE and Plaintext formats

### The Four Rules

Conway's Game of Life follows exactly four rules for cell state transitions:

1. **Underpopulation**: A live cell with fewer than 2 live neighbors dies (loneliness)
2. **Survival**: A live cell with 2 or 3 live neighbors survives
3. **Overpopulation**: A live cell with more than 3 live neighbors dies (overcrowding)
4. **Reproduction**: A dead cell with exactly 3 live neighbors becomes alive (birth)

Despite extreme simplicity, these rules produce incredibly complex behaviors.

### Core Class Structure

The `ConwayGameOfLife` class must support:

```python
class ConwayGameOfLife:
    def __init__(self, grid, finite=False):
        """
        Initialize Game of Life.
        
        grid: 2D numpy array (1=alive, 0=dead)
        finite: if False, use toroidal (wrapping) boundaries
        """
        pass
    
    def evolve(self):
        """Execute one generation using cell-by-cell iteration"""
        pass
    
    def update_grid_fast(self, grid):
        """Optimized update using 2D convolution for large grids"""
        pass
    
    def get_grid(self):
        """Return current state"""
        pass
    
    def tick(self):
        """Single generation step"""
        pass
```

### Task 1a: Implement Core Rules

Implement the evolution mechanics in the `evolve` method:

**Requirements**:
- Implement all four rules with nested loops over rows and columns
- Handle both finite (`self.finite=True`) and toroidal (`self.finite=False`) boundary conditions
- When `finite=False`, boundaries wrap around (edges connect to opposite sides)
- Verify correctness with the Blinker pattern (alternates vertically/horizontally)

**Blinker Test**:
- A 3-cell horizontal line should oscillate with period 2
- Generation 0: `OOO` (three alive cells horizontally)
- Generation 1: Pattern rotates 90 degrees (three cells vertically)
- Generation 2: Returns to Generation 0

### Task 1b: Simulate a Glider

Run the simulator with a **Glider** pattern:

```
.OO
O..
.O.
```

The glider is a fundamental pattern that:
- Moves diagonally across the grid at speed c/4 (one cell every 4 generations)
- Maintains its shape while translating
- Represents a "spaceship" - a reusable signal

**Explanation**: Write a detailed explanation of how gliders can be used to:
- Transmit information/signals across the Game of Life universe
- Serve as building blocks for complex computational structures
- Interact with other patterns to create logic gates

### Task 1c: Debug the Gosper Glider Gun

The Gosper Glider Gun is an oscillating pattern that continuously emits a stream of gliders.

**Problem**: The provided `insertGliderGun` method has a minor coordinate error (asymmetric shift in the left block).

**Your Tasks**:
- Analyze the code to locate the error
- Correct the coordinates to fix the gun
- Verify that it produces an infinite stream of gliders

The corrected gun should generate gliders periodically, creating a never-ending stream moving across the grid.

### Task 1d: Implement RLE and Plaintext Parsers

Implement the `parse_pattern(filepath)` method to load patterns from files:

**Plaintext Format (.cells)**:
- Simple representation: 'b' for dead, 'o' for alive
- One row per line
- Easy to read but space-inefficient for large patterns

**RLE Format (.rle)**:
- Run-Length Encoded: numbers prefix symbols
- `3o` means three consecutive 'o's (alive)
- `$` marks end of row, `!` marks end of pattern
- Compact representation for large patterns

**Examples**:
- Plaintext Glider:
  ```
  .OO
  O..
  .O.
  ```
- RLE Glider: `bob$2bo$2o!`

**Implementation Requirements**:
- Support both formats automatically
- Handle multi-line RLE encodings
- Properly parse counts and symbols
- Load patterns into the grid correctly

### Task 1e: Fast Convolution Optimization

For large grids (N > 1024), cell-by-cell iteration becomes slow (O(N^2) per generation).

**Implement** `update_grid_fast(grid)` using 2D convolution:

**Approach**:
1. Use `scipy.signal.convolve2d` to count live neighbors efficiently
2. Apply a 3x3 kernel to sum neighbor states
3. Vectorize rule application
4. Support both finite and toroidal boundary modes

**Benefits**:
- Dramatically faster for large grids
- Leverages optimized library functions
- Still produces identical results to naive approach

**Kernel for neighbor counting**:
```
[1 1 1]
[1 0 1]
[1 1 1]
```

## Section 2: Langton's Ant

### Objective

Implement Langton's Ant simulator in `langton.py` that demonstrates:
- Simple deterministic rules producing chaotic behavior
- Eventual emergence of ordered, repeating patterns
- A 2D cellular automaton representing a 2D Turing machine

### The Ant Rules

The ant operates on a grid with two colors (initially white and black):

1. **On a White Cell**:
   - Change cell to black
   - Turn 90 degrees right (R)
   - Move forward one cell

2. **On a Black Cell**:
   - Change cell to white
   - Turn 90 degrees left (L)
   - Move forward one cell

Despite these simple rules, the ant produces remarkably complex behavior.

### Core Class Structure

The `LangtonsAnt` class must maintain:

```python
class LangtonsAnt:
    def __init__(self, grid_size, colors, rules, start_pos=(0,0), start_dir='U'):
        """
        Initialize Langton's Ant.
        
        grid_size: dimensions of the grid
        colors: list of color states (e.g., ['white', 'black'])
        rules: transition rules for each color
        start_pos: (row, col) starting position
        start_dir: initial direction (U/R/D/L = Up/Right/Down/Left)
        """
        pass
    
    def step(self):
        """Execute one step of the ant's movement"""
        pass
    
    def run(self, steps):
        """Execute multiple steps"""
        pass
    
    def get_grid(self):
        """Return current grid state"""
        pass
```

### Task 2a: Implement Basic Ant

Implement the `LangtonsAnt` class:

**Requirements**:
- Track ant position as (row, column)
- Track ant direction as cardinal: North (U), East (R), South (D), West (L)
- Maintain grid of cell colors (0=white, 1=black initially)
- Implement the two basic rules for white and black cells

### Task 2b: Demonstrate Ant Behavior

Run simulations showing two key behaviors:

**1. Chaotic Behavior** (Initial 10,000+ steps):
- The ant moves seemingly randomly
- Creates asymmetric, irregular patterns
- No clear organization visible

**2. The Highway** (After ~10,000 steps):
- Suddenly transitions to a repeating pattern
- Forms a diagonal "highway" or "road"
- Pattern repeats with period ~10,000 steps
- Ant continues indefinitely in this organized state

This transition from chaos to order is a remarkable example of emergence.

### Task 2c: Multi-Color Support

Extend your implementation to support **multiple colors**:

**New Feature**:
- Rules are now a dictionary specifying turn direction for each color
- Example rules: `LLRR` means colors cycle: 0→L, 1→L, 2→R, 3→R
- Each cell cycles through colors: 0 -> 1 -> 2 -> ... -> max -> 0

**Multi-Color Rules Format**:
```
'LLRR': Turn left on colors 0,1 and right on colors 2,3
'RLR': Turn right on 0, left on 1, right on 2
```

**Demonstrate**:
- Show that multi-color ants produce complex, beautiful symmetric patterns
- Examples: triangular patterns, symmetrical designs
- Create interesting patterns with custom rules

## Section 3: Turing Completeness

### Objective

Demonstrate that Conway's Game of Life is Turing complete by implementing digital logic gates using gliders.

### Theoretical Background

**Turing Completeness**: A system is Turing complete if it can simulate any Turing machine, meaning it can compute any computable function.

To prove Turing completeness, it suffices to construct:
- AND gate: Outputs 1 only if both inputs are 1
- NOT gate: Outputs opposite of input
- These two gates can compose to create any Boolean function (universal gate set)

### Signal Representation

In Game of Life, signals are represented as **gliders**:
- **Bit 1**: Presence of a glider at a specific time/location
- **Bit 0**: Absence of a glider

Information flows as streams of gliders traveling specific paths.

### Core Implementation

The `logic_gates.py` file must implement:

```python
def setup_and_gate():
    """Create Game of Life grid configured with AND gate"""
    pass

def run_and_gate(input_a, input_b):
    """Execute AND gate with given inputs"""
    pass

def setup_not_gate():
    """Create Game of Life grid configured with NOT gate"""
    pass

def run_not_gate(input_a):
    """Execute NOT gate with given input"""
    pass
```

### Task 3a: Implement AND Gate

**Logic**:
- Two input glider streams (A and B)
- Paths positioned to intersect at 90-degree angles
- Output location (15, 12)

**Truth Table**:
- (0,0): No gliders -> No collision -> Output = 0
- (1,0): Only A -> Passes through -> Output = 0
- (0,1): Only B -> Passes through -> Output = 0
- (1,1): Both gliders -> Collide -> Create 2x2 block -> Output = 1

**Physical Implementation**:
- Position glider sources such that paths cross perpendicularly
- When both arrive simultaneously, collision creates stable pattern (2x2 block)
- Block at target location represents output 1
- Empty space represents output 0

### Task 3b: Implement NOT Gate

**Logic**:
- One input signal (A) and one control signal (control)
- Control glider always generated and sent to output location
- Input glider positioned to intercept control glider

**Truth Table**:
- Input 0: Control glider passes unobstructed -> Output = 1 (presence)
- Input 1: Input glider intercepts control -> Mutual annihilation -> Output = 0 (absence)

**Physical Implementation**:
- Generate control glider on a fixed schedule
- If input is active, send input glider on collision course
- Gliders annihilate each other on collision
- Output location either has control glider (1) or not (0)

### Implications

Once AND and NOT gates are constructed:
- Can build NAND gate (inverted AND)
- NAND gates can compose to create any Boolean function
- AND + NOT gates can implement any circuit
- Therefore, Game of Life can compute any function Turing can compute
- This proves Game of Life is Turing complete

### Advanced Topics

With AND and NOT gates, students can explore:
- Building OR gates, XOR gates
- Creating memory elements (latches, flip-flops)
- Implementing small circuits (adders, multipliers)
- Towards a complete computer architecture in Game of Life

## Running and Visualization

### Game of Life GUI

Run the pygame visualization:

```bash
python pygame_gol.py
```

Features:
- Interactive grid visualization
- Step-by-step evolution
- Load saved patterns
- Pan and zoom

### Langton's Ant GUI

Visualize Langton's Ant behavior:

```bash
python langton_pygame.py
```

Features:
- Visual display of grid colors
- Ant position marker
- Multi-color rule visualization
- Step counter and pattern emergence

### Pattern Viewer

Browse pre-made patterns:

```bash
python pygame_viewer.py
```

Available patterns:
- Gosper Glider Gun
- Various spaceships
- Oscillators
- Other famous configurations

## Testing

Run test suites to verify implementations:

```bash
python test_gameoflife_glider_simple.py      # Basic glider test
python test_gameoflife_glider.py             # Advanced glider tests
python test_gameoflife_glider_large.py       # Large pattern tests
```

## Implementation Tips

1. **Start with Arrays**: Use NumPy for efficient 2D arrays
2. **Boundary Handling**: Carefully handle wrapping vs. finite boundaries
3. **Neighbor Counting**: Vectorize neighbor counting for efficiency
4. **Pattern Loading**: Test parsers with simple patterns first
5. **Visualization**: Debug with visual output before optimization
6. **Convolution**: Implement naive version first, then optimize with scipy
7. **Gate Design**: Study documented gate designs before implementing

## Key Concepts

- **Emergence**: Simple rules -> Complex behavior
- **Universality**: Different systems can compute the same things
- **Cellular Automata**: Discrete computation model with local interactions
- **Determinism**: Completely deterministic yet complex
- **Chaos and Order**: Transition from chaotic to periodic behavior
- **Turing Completeness**: Minimal requirements for universal computation

## References

- Moore, C., Mertens, S., 2011. The Nature Of Computation. Oxford University Press.
- LifeWiki: Comprehensive Game of Life resource
- Wikipedia: Conway's Game of Life, Langton's Ant
- "Digital Logic Gates on Conway's Game of Life" - Technical papers
- Computerphile: "Let's BUILD a COMPUTER in CONWAY's GAME of LIFE" (YouTube)
- SICP: Stream processing and cellular automata

## Pattern File Formats

### RLE Format Specification

**Header**:
```
x=m, y=n, rule=B3/S23
```

**Encoding**:
- `o` = alive cell
- `b` = dead cell
- `.` = end of row ($)
- `!` = end of pattern
- Numbers prefix symbols: `3o` = `ooo`

**Example** (Glider):
```
x=3, y=3, rule=B3/S23
bob$2bo$2o!
```

### Plaintext Format

**Structure**:
- Comments start with `!`
- Rows of 'o' (alive) and '.' (dead)
- Coordinates start at (0,0) top-left

**Example**:
```
! Glider
.oo
o..
.o.
```

## Supplementary Resources

- Visual Cellular Automata Explorers
- Interactive Game of Life implementations
- Langton's Ant simulations and variations
- Digital logic design texts
- Computation theory foundations

---

*For questions about Part 2, refer to the course documentation or consult with your instructors.*
