# Theory of Languages and Automata - Practical Project

A comprehensive practical project exploring the theory of computation through implementation of Turing machines and cellular automata.

## Project Overview

This project is part of the Theory of Languages and Automata (TLA) course at Iran University of Science and Technology (IUST), taught by Dr. Reza Entezari-Maleki and Dr. Farzaneh Ghayour Baghbani. The project was co-designed with Taha Biklariyan (https://github.com/Tahabik).

The project consists of two main parts that explore fundamental concepts in theoretical computer science:

1. **Part 1: Turing Machines and the Busy Beaver Problem** - Implementation of a complete Turing machine simulator with applications to mathematical computations and exploration of the undecidable Busy Beaver problem.

2. **Part 2: Cellular Automata and Universal Computation** - Implementation of two famous cellular automata (Conway's Game of Life and Langton's Ant) and proof of Turing completeness through digital logic gates.

## Course Information

- **University**: Iran University of Science and Technology (IUST)
- **Course**: Theory of Languages and Automata (TLA4042)
- **Instructors**: Dr. Reza Entezari-Maleki, Dr. Farzaneh Ghayour Baghbani
- **Semester**: 4042
- **Designers**: Milad Zarei Maleki, Taha Biklariyan

## Project Structure

```
.
├── Part 1 - Busy Beaver/          # Turing machines and Busy Beaver problem
│   ├── README.md                  # Part 1 documentation
│   ├── turing_machine.py          # Turing machine simulator
│   ├── busy_beaver.py             # Busy Beaver implementations
│   ├── student_test_turing.py     # Self-assessment tests
│   ├── test_turing_machine_example*.py
│   ├── test_turing_adder.py       # Unary addition test
│   ├── test_turing_multiplier.py  # Unary multiplication test
│   └── test_busy_beaver_2.py      # Busy Beaver test
│
├── Part 2 - GoL & Langton's Ant/  # Cellular automata
│   ├── README.md                  # Part 2 documentation
│   ├── conway.py                  # Game of Life implementation
│   ├── langton.py                 # Langton's Ant implementation
│   ├── logic_gates.py             # Logic gates using Game of Life
│   ├── pygame_gol.py              # GUI for Game of Life
│   ├── pygame_viewer.py           # Pattern viewer utility
│   ├── langton_pygame.py          # GUI for Langton's Ant
│   ├── test_gameoflife_glider*.py # Game of Life tests
│   └── *.cells                    # Pattern files (RLE/Plaintext format)
│
└── README.md                       # This file
```

## Key Concepts

### Part 1: Turing Machines

A **Turing Machine** is a mathematical model of computation that represents the simplest form of a computer. Key components include:

- **Finite state machine**: A set of states determining machine behavior
- **Tape**: An infinite or semi-infinite memory where symbols are read and written
- **Head**: A pointer that reads/writes symbols on the tape
- **Transition rules**: Rules that determine state changes based on current state and symbol

In this part, students implement:

- A complete Turing machine simulator with support for infinite bidirectional tape
- Mathematical computations: addition and multiplication using unary representation
- The **Busy Beaver problem**: finding Turing machines that produce the maximum number of 1s on their tape before halting, demonstrating the halting problem's undecidability

### Part 2: Cellular Automata

**Cellular Automata** are discrete computational models consisting of a grid of cells, each with a finite set of states. The next state of each cell depends only on its current state and neighboring cells.

#### Conway's Game of Life

A two-dimensional cellular automaton with four simple rules:

1. **Underpopulation**: A live cell with fewer than 2 live neighbors dies
2. **Survival**: A live cell with 2 or 3 live neighbors survives
3. **Overpopulation**: A live cell with more than 3 live neighbors dies
4. **Reproduction**: A dead cell with exactly 3 live neighbors becomes alive

Despite simple rules, it exhibits remarkable emergent behavior including Turing completeness.

#### Langton's Ant

A simple two-dimensional computational model representing a 2D Turing machine with chaotic and fascinating emergent behavior. The ant operates on a grid following simple rules based on cell colors and produces complex patterns.

#### Turing Completeness

The project demonstrates that both cellular automata are Turing complete by constructing digital logic gates (AND, NOT) using gliders in Conway's Game of Life. This proves that any computable function can be implemented in these systems.

## Learning Outcomes

Through this project, students will:

- Understand the fundamental model of Turing machines and their role in theoretical computer science
- Implement practical simulators for abstract computational models
- Explore the concept of universality and Turing completeness
- Investigate computability and undecidability through the Busy Beaver problem
- Witness emergence: how simple local rules lead to complex global behavior
- Gain insight into the equivalence of different computational models

## Technical Stack

- **Language**: Python 3
- **Visualization**: Pygame (for graphical simulations)
- **Scientific Computing**: NumPy, SciPy (for optimized cellular automata computation)
- **File Formats**: RLE (Run Length Encoded) and Plaintext for Game of Life patterns

## Getting Started

For detailed instructions on running and completing each part:

- See [Part 1 - Busy Beaver/README.md](Part%201%20-%20Busy%20Beaver/README.md) for Turing machine implementation
- See [Part 2 - GoL & Langton's Ant/README.md](Part%202%20-%20GoL%20&%20Langton's%20Ant/README.md) for cellular automata implementation

## References

- Moore, C., Mertens, S., 2011. The Nature Of Computation. Oxford University Press.
- Conway's Game of Life - Wikipedia and LifeWiki
- Langton's Ant - Wikipedia
- Busy Beaver Database and Problem

## Additional Resources

- Computerphile: Turing Machine Primer
- Computerphile: Busy Beaver Turing Machines
- Turing Completeness tutorials and visualizations
- Digital Logic Gates in Conway's Game of Life

---

*For questions or contributions, please contact the course instructors or project designers.*
