# Part 1: Turing Machines and the Busy Beaver Problem

This part focuses on implementing a complete Turing machine simulator and exploring fundamental concepts in computability theory.

## Overview

A **Turing Machine** is a mathematical model of computation that represents the simplest form of a computer. Despite its simplicity, it is a universal model of computation - any computable function can be implemented on a Turing machine.

This part consists of three main sections:

1. **Turing Machine Simulator**: Building a complete simulator with support for infinite tape and various computational operations
2. **Mathematical Computations**: Implementing addition and multiplication using unary representation
3. **Busy Beaver Problem**: Exploring the undecidable problem of finding machines that produce maximum output

## Project Components

### File Structure

```
Part 1 - Busy Beaver/
├── turing_machine.py              # Core Turing machine simulator class
├── busy_beaver.py                 # Busy Beaver implementations and utilities
├── student_test_turing.py         # Self-assessment test suite
├── test_turing_machine_example1.py # Example 1 test (simple machine)
├── test_turing_machine_example2.py # Example 2 test (more complex machine)
├── test_turing_adder.py           # Tests for unary addition machine
├── test_turing_multiplier.py      # Tests for unary multiplication machine
├── test_busy_beaver_2.py          # Tests for 2-card Busy Beaver
└── README.md                      # This file
```

## Section 1: Turing Machine Simulator

### Objective

Implement a complete Turing machine simulator in `turing_machine.py` that:
- Supports an initially infinite tape extending to the right (one-way infinite)
- Implements a Python Generator-based architecture for step-by-step computation
- Supports deterministic state transitions
- Provides debugging and visualization capabilities
- Later extends to support bidirectional (two-way) infinite tape

### Core Class Structure

The `TuringMachine` class must implement the following interface:

```python
class TuringMachine:
    def __init__(self, transitions, start_state='q0', 
                 accept_state='qa', reject_state='qr', blank_symbol=''):
        """
        Initialize the Turing machine.
        
        transitions: dictionary mapping (state, symbol) tuples to 
                   (next_state, write_symbol, direction) tuples
        start_state: initial state of the machine
        accept_state: state where machine accepts input
        reject_state: state where machine rejects input
        blank_symbol: symbol representing empty tape cells
        """
        pass
    
    def run(self, input_):
        """
        Run the simulator as a Python Generator.
        
        Yields tuples: (action, configuration) for each computational step
        
        action: 'Accept', 'Reject', or None
        configuration: dictionary with current tape state and position
        """
        pass
    
    def accepts(self, input_, step_limit=100):
        """Check if input is accepted (returns True/False/None)"""
        pass
    
    def rejects(self, input_, **kwargs):
        """Check if input is rejected (opposite of accepts)"""
        pass
    
    def debug(self, input_, step_limit=100, colored=False):
        """Print step-by-step machine configuration for debugging"""
        pass
```

### Configuration Dictionary Format

Each computational step produces a configuration dictionary:

```python
{
    'state': current_state_name,
    'left_hand_side': [symbols...],    # in reverse order (closest to head is last)
    'symbol': current_symbol_under_head,
    'right_hand_side': [symbols...]
}
```

### Implementation Details

- The simulator uses Python generators to yield computation steps one at a time
- This allows interactive debugging and step-by-step visualization
- Initial tape is one-way infinite (only extends right)
- Later extended to two-way infinite tape with dynamic expansion
- Transitions are represented as: (state, symbol) -> (new_state, write_symbol, direction)
- Directions are 'L' (left) or 'R' (right)

### Testing

Run the example test files to verify your implementation:

```bash
python test_turing_machine_example1.py
python test_turing_machine_example2.py
```

Tasks:
- List all states for each example machine
- Debug and display machine configuration for each transition
- Explain what computations each example machine performs

## Section 2: Mathematical Computations

### Objective

Implement Turing machines that perform basic mathematical operations using unary representation, where a number n is represented as n ones separated by zeros.

### Task 2a: Unary Addition

Implement a Turing machine that adds two numbers in unary representation.

**Format**: Two numbers separated by a zero delimiter (0), empty symbol is blank
- Input for 2+3: `110111` -> Output: `11111`
- Input for 3+4: `11101111` -> Output: `1111111`

**Test file**: `test_turing_adder.py`

Algorithm outline:
1. Replace the separator (0) with 1
2. Remove the trailing separator if needed
3. Accept when done

### Task 2b: Unary Multiplication

Implement a Turing machine that multiplies two numbers in unary representation.

**Format**: Two numbers separated by a zero delimiter (0), blank symbol for empty cells
- Input for 2*3: `110111` -> Output: `111111`
- Input for 3*5: `111011111` -> Output: `111111111111111`

**Test file**: `test_turing_multiplier.py`

Algorithm outline:
1. Iterate through the first number
2. For each 1 in the first number, append a copy of the second number
3. Clean up intermediate markers
4. Accept when done

### Implementation Notes

- You may use additional tape symbols for intermediate computations
- The zero (0) character separates the two input numbers
- Blank symbol ('') represents empty tape cells
- These basic machines demonstrate that Turing machines can perform universal arithmetic operations

## Section 3: Busy Beaver Problem

### Objective

Explore the Busy Beaver problem, which asks: What is the maximum number of 1s that a halting n-state Turing machine can write on its tape?

### Theoretical Background

The Busy Beaver problem is fundamentally related to the **Halting Problem**:

- **Undecidability**: There is no general algorithm to determine whether an arbitrary Turing machine will halt for a given input
- **Non-computability**: The Busy Beaver function BB(n) is non-computable - no Turing machine can compute it for all n
- **Rapid growth**: BB(n) grows faster than any computable function
  - BB(1) = 1
  - BB(2) = 6
  - BB(3) = 21
  - BB(4) = 107
  - BB(5) = 47,176,870
  - BB(6) > 10^36,534

### Busy Beaver Machine Format

Busy Beaver machines are represented as cards, where each card represents a state and its transitions:

```
Card A - 0: B1R - 1: B1L
Card B - 0: A1L - 1: H1R
```

This means:
- State A: If 0, write 1, move right to state B; if 1, write 1, move left to state B
- State B: If 0, write 1, move left to state A; if 1, write 1, move right to halt (H)

### Task 3a: Understanding Undecidability

Explain why finding Busy Beaver machines is difficult and why the problem is undecidable.

Key points to address:
- Connection to the Halting Problem
- Why brute force search becomes computationally infeasible
- What makes this problem fundamentally non-computable

### Task 3b: Implement Two-Way Infinite Tape

Modify `turing_machine.py` to support bidirectional infinite tape:

**Change**: The one-way infinite tape initially only extended right. Now implement support for a two-way infinite tape that dynamically expands left and right as needed.

- When the head moves left from the leftmost cell, the tape should expand dynamically
- No error or warning should occur
- Both finite and toroidal/wrapping boundary modes should be supported via `self.finite` flag

### Task 3c: Why Use Generators?

Explain the benefits of using Python generators in Turing machine simulation:

Considerations:
- Memory efficiency for long computations
- Interactivity and step-by-step debugging
- Suspension and resumption of computation
- Streaming output without storing entire history

### Task 3d: Run 2-Card Busy Beaver

Implement the example 2-card Busy Beaver machine in your simulator:

```
Card A - 0: B1R - 1: B1L
Card B - 0: A1L - 1: H1R
```

Starting with a blank tape, how many 1s does the machine produce?

**Test file**: `test_busy_beaver_2.py`

### Task 3e: Compare with Known Results

Compare your result with the best known 2-state machines from the Busy Beaver Wiki:

- Is your output correct?
- How does it compare to the optimal 2-state machine?
- Evaluate your result against established benchmarks

### Task 3f: Create 3 and 4-Card Busy Beaver Machines

Design and implement your own Busy Beaver machines with 3 and 4 states:

- You do not need to find the absolute optimal machines (BB(3) and BB(4))
- Just create machines that outperform the 2-state machines
- Show the number of 1s produced by each machine

### Task 3g: Attempt 5-Card Busy Beaver

Try to find or create a 5-state Busy Beaver machine:

- Justify whether your machine is new or explain why it halts
- Compare with known 5-state machines
- Provide reasoning for your design

### Task 3h: Research and Verify

Consult the Busy Beaver Wiki (https://www.sligocki.com/wiki/Busy_Beaver) and study the best known machines:

- Compare 2, 3, and 4-state champion machines
- Are your machines better than the known champions?
- Implement the champion machines and verify their output
- Compare results with your designs

**Reference machines locations**:
- 2-card champion: BB(2) = 6
- 3-card champion: BB(3) = 21
- 4-card champion: BB(4) = 107

## Running Tests

Self-assessment tests are available in `student_test_turing.py`:

```bash
python student_test_turing.py
```

This will validate your implementation against the specification.

## Implementation Tips

1. **Start Simple**: Begin with basic state transitions before implementing complex features
2. **Use Generators**: Embrace Python generators for clean, step-by-step simulation
3. **Debug Printing**: Implement clear debug output to visualize tape state
4. **Test Incrementally**: Test with simple inputs before complex computations
5. **Handle Edge Cases**: Consider tape boundaries, blank symbols, and state acceptance
6. **Extend Gradually**: First implement one-way tape, then extend to two-way

## Key Concepts to Understand

- **State Machines**: How finite states and transitions model computation
- **The Halting Problem**: Why some problems are undecidable
- **Universality**: Why Turing machines are universal (can compute any computable function)
- **Undecidability**: The Busy Beaver problem demonstrates limits of computation
- **Emergence**: Simple rules (transitions) produce complex behavior (long computations)

## References

- Moore, C., Mertens, S., 2011. The Nature Of Computation. Oxford University Press.
- Computerphile: Turing Machine Primer (YouTube)
- Computerphile: Busy Beaver Turing Machines (YouTube)
- Busy Beaver problem - Wikipedia
- Busy Beaver Wiki - https://www.sligocki.com/wiki/Busy_Beaver

## Supplementary Resources

- Visual Turing Machine Simulators
- Interactive Busy Beaver explorations
- Formal Theory of Computation texts

---

*For questions about Part 1, refer to the course documentation or consult with your instructors.*
