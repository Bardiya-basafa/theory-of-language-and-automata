# -*- coding: utf-8 -*-
"""Stream-based glider AND and NOT gates for Conway's Game of Life."""

from conway import GameOfLife


class _StreamingCircuit:
    """A GameOfLife-compatible wrapper that injects timed glider streams."""

    def __init__(self, life, injections, samples, detector):
        self.life = life
        self.injections = injections
        self.samples = samples
        self.detector = detector
        self.generation = 0
        self.outputs = []

    @property
    def grid(self):
        return self.life.grid

    def getStates(self):
        return self.life.getStates()

    def getGrid(self):
        return self.life.getGrid()

    def evolve(self):
        # A stream source launches the gliders assigned to this time slot.
        for pattern, origin in self.injections.get(self.generation, ()):
            base_r, base_c = origin
            for dr, dc in pattern:
                self.life.grid[base_r + dr, base_c + dc] = self.life.aliveValue

        self.life.evolve()
        self.generation += 1

        # Sample one Boolean output for each time slot.
        if self.generation in self.samples:
            slot = self.samples[self.generation]
            self.outputs.append((slot, bool(self.detector(self.life))))


class GliderLogicGates:
    """Simulate Boolean gates using synchronized streams of gliders."""

    # The two gliders move north-east and south-east. Their velocity vectors
    # are perpendicular, so the signal paths meet at 90 degrees.
    _NE_GLIDER = (
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 2),
    )
    _SE_GLIDER = (
        (0, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    )

    AND_TARGET = (15, 12)
    AND_STEPS = 36

    # The Gosper gun is part of the NOT circuit and naturally emits one
    # south-east glider every 30 generations. The first emitted glider reaches
    # the reference phase below at generation 91.
    NOT_GUN_ORIGIN = (10, 5)
    NOT_GUN_FIRST_SLOT = 91
    NOT_GUN_PERIOD = 30
    NOT_INPUT_ORIGIN = (50, 42)

    # Expected control-glider phase 34 generations after each input slot.
    NOT_OUTPUT_CELLS = frozenset(
        {
            (44, 54),
            (45, 52),
            (45, 54),
            (46, 53),
            (46, 54),
        }
    )
    NOT_STEPS = 34

    # 48 generations put successive AND gliders 12 diagonal cells apart,
    # enough separation for each pair to represent an independent time slot.
    STREAM_PERIOD = 48

    @staticmethod
    def _new_life(grid_size):
        if grid_size < 35:
            raise ValueError("grid_size must be at least 35")
        return GameOfLife(grid_size, finite=True, fastMode=True)

    @staticmethod
    def _place_glider(life, pattern, origin):
        base_r, base_c = origin
        for dr, dc in pattern:
            life.grid[base_r + dr, base_c + dc] = life.aliveValue

    @staticmethod
    def _bits(values):
        if isinstance(values, str):
            if not values or any(ch not in "01" for ch in values):
                raise ValueError("bit streams must contain only 0 and 1")
            return [ch == "1" for ch in values]
        return [bool(value) for value in values]

    @staticmethod
    def _run(circuit, final_generation):
        while circuit.generation < final_generation:
            circuit.evolve()
        circuit.outputs.sort(key=lambda item: item[0])
        return [value for _, value in circuit.outputs]

    def _and_output_present(self, life):
        r, c = self.AND_TARGET
        return (
            life.grid[r, c] == life.aliveValue
            and life.grid[r, c + 1] == life.aliveValue
            and life.grid[r + 1, c] == life.aliveValue
            and life.grid[r + 1, c + 1] == life.aliveValue
        )

    def _not_output_present(self, life):
        return all(
            life.grid[r, c] == life.aliveValue for r, c in self.NOT_OUTPUT_CELLS
        )

    def setup_and_stream(self, a_stream, b_stream, grid_size=35, period=None):
        """Create an AND gate that accepts synchronized streams of input bits."""
        a_bits = self._bits(a_stream)
        b_bits = self._bits(b_stream)
        if len(a_bits) != len(b_bits):
            raise ValueError("AND input streams must have the same length")

        period = self.STREAM_PERIOD if period is None else int(period)
        if period < 44:
            raise ValueError("period must be at least 44 generations")

        life = self._new_life(grid_size)
        injections = {}
        samples = {}

        for slot, (a_bit, b_bit) in enumerate(zip(a_bits, b_bits)):
            launch_time = slot * period
            packets = []
            if a_bit:
                packets.append((self._NE_GLIDER, (23, 2)))
            if b_bit:
                packets.append((self._SE_GLIDER, (3, 0)))
            injections.setdefault(launch_time, []).extend(packets)

            sample_time = launch_time + self.AND_STEPS
            samples[sample_time] = slot

        return _StreamingCircuit(
            life,
            injections,
            samples,
            self._and_output_present,
        )

    def setup_not_stream(self, a_stream, grid_size=120, period=None):
        """Create a NOT gate driven by a real Gosper-gun control stream."""
        a_bits = self._bits(a_stream)

        # The Gosper gun and its collision/output lanes need a larger board.
        life = self._new_life(max(grid_size, 120))
        life.insertGliderGun(self.NOT_GUN_ORIGIN)

        injections = {}
        samples = {}

        for slot, a_bit in enumerate(a_bits):
            control_time = self.NOT_GUN_FIRST_SLOT + slot * self.NOT_GUN_PERIOD

            # The control bit is emitted naturally by the gun. Only an input
            # value of 1 launches an artificial NE glider. Its collision with
            # the corresponding control glider annihilates both of them.
            if a_bit:
                injections[control_time] = [
                    (self._NE_GLIDER, self.NOT_INPUT_ORIGIN)
                ]

            samples[control_time + self.NOT_STEPS] = slot

        return _StreamingCircuit(
            life,
            injections,
            samples,
            self._not_output_present,
        )

    def run_and_stream(self, a_stream, b_stream, period=None):
        """Return the AND result for every synchronized input time slot."""
        a_bits = self._bits(a_stream)
        circuit = self.setup_and_stream(a_bits, b_stream, period=period)
        actual_period = self.STREAM_PERIOD if period is None else int(period)
        end = (len(a_bits) - 1) * actual_period + self.AND_STEPS
        return self._run(circuit, end)

    def run_not_stream(self, a_stream, period=None):
        """Return the NOT result for every Gosper-gun output time slot."""
        a_bits = self._bits(a_stream)
        circuit = self.setup_not_stream(a_bits)
        end = (
            self.NOT_GUN_FIRST_SLOT
            + (len(a_bits) - 1) * self.NOT_GUN_PERIOD
            + self.NOT_STEPS
        )
        return self._run(circuit, end)

    # These four methods keep the original template interface unchanged.
    def setup_and_gate(
        self, grid_size=35, input_a_present=False, input_b_present=False
    ):
        life = self._new_life(grid_size)
        if input_a_present:
            self._place_glider(life, self._NE_GLIDER, (23, 2))
        if input_b_present:
            self._place_glider(life, self._SE_GLIDER, (3, 0))
        return life

    def setup_not_gate(self, grid_size=120, input_a_present=False):
        # Keep the template method, but build its control signal with a real
        # Gosper gun instead of inserting a control glider directly.
        return self.setup_not_stream(
            [input_a_present], grid_size=max(grid_size, 120)
        )

    def run_and_gate(self, input_a_present, input_b_present):
        life = self.setup_and_gate(
            input_a_present=input_a_present,
            input_b_present=input_b_present,
        )
        for _ in range(self.AND_STEPS):
            life.evolve()
        return bool(self._and_output_present(life))

    def run_not_gate(self, input_a_present):
        circuit = self.setup_not_gate(input_a_present=input_a_present)
        end = self.NOT_GUN_FIRST_SLOT + self.NOT_STEPS
        output = self._run(circuit, end)
        return bool(output[0])


def _text_bits(values):
    return "".join("1" if value else "0" for value in values)


def _print_examples(a_stream, b_stream):
    gates = GliderLogicGates()
    and_output = gates.run_and_stream(a_stream, b_stream)
    not_output = gates.run_not_stream(a_stream)

    print("Stream-based gates")
    print(f"A       = {a_stream}")
    print(f"B       = {b_stream}")
    print(f"A AND B = {_text_bits(and_output)}")
    print(f"NOT A   = {_text_bits(not_output)}")


def _show_stream(gate, a_stream, b_stream, period):
    from pygame_viewer import run_pygame_life

    gates = GliderLogicGates()
    if gate == "and":
        circuit = gates.setup_and_stream(a_stream, b_stream, period=period)
        # A 2x2 block is a still life, so keep the animation running until
        # the user closes the window and let Conway's rules preserve it.
        frames = None
        title = f"Streaming AND: A={a_stream}, B={b_stream}"
        cell_scale = 14
        fps = 12
    else:
        circuit = gates.setup_not_stream(a_stream)
        # The Gosper gun keeps firing forever. The animation therefore runs
        # until the user closes the pygame window.
        frames = None
        title = f"Streaming NOT with Gosper gun: A={a_stream}"
        cell_scale = 6
        fps = 30

    run_pygame_life(
        circuit,
        cell_scale=cell_scale,
        fps=fps,
        max_frames=frames,
        title=title,
    )
    circuit.outputs.sort(key=lambda item: item[0])
    print("Output =", _text_bits(value for _, value in circuit.outputs))


def _read_bit_stream(prompt):
    """Read a non-empty binary stream interactively."""
    while True:
        value = input(prompt).strip()
        if value and all(bit in "01" for bit in value):
            return value
        print("Invalid input; try again.")


def main():
    """Ask for the gate and streams, then start the animation."""
    while True:
        answer = input("Which gate do you want (AND/NOT): ").strip().lower()
        if answer in ("and", "And", "AND"):
            gate = "and"
            break
        if answer in ("not", "Not", "NOT"):
            gate = "not"
            break

    period = GliderLogicGates.STREAM_PERIOD

    if gate == "not":
        a_stream = _read_bit_stream("Value of input stream? ")
        _show_stream("not", a_stream, None, period)
        return

    a_stream = _read_bit_stream("Value of stream A? ")
    while True:
        b_stream = _read_bit_stream("Value of stream B? ")
        if len(a_stream) == len(b_stream):
            break
        print("Length of streams should be equall; try again.")

    _show_stream("and", a_stream, b_stream, period)


if __name__ == "__main__":
    main()
