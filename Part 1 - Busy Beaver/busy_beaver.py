import sys


class Error(Exception):
    pass


class TuringMachine(object):
    def __init__(self, program, start, halt, init):
        self.program = program
        self.start = start
        self.halt = halt
        self.init = init
        self.tape = [self.init]
        self.pos = 0
        self.state = self.start
        self.set_tape_callback(None)
        self.tape_changed = 1
        self.movez = 0

    def run(self):
        tape_callback = self.get_tape_callback()
        while self.state != self.halt:
            if tape_callback:
                tape_callback(self.tape, self.tape_changed)

            lhs = self.get_lhs()
            rhs = self.get_rhs(lhs)

            new_state, new_symbol, move = rhs

            old_symbol = lhs[1]
            self.update_tape(old_symbol, new_symbol)
            self.update_state(new_state)
            self.move_head(move)

        if tape_callback:
            tape_callback(self.tape, self.tape_changed)

    def set_tape_callback(self, fn):
        self.tape_callback = fn

    def get_tape_callback(self):
        return self.tape_callback

    property(get_tape_callback, set_tape_callback)

    @property
    def moves(self):
        return self.movez

    def update_tape(self, old_symbol, new_symbol):
        if old_symbol != new_symbol:
            self.tape[self.pos] = new_symbol
            self.tape_changed += 1
        else:
            self.tape_changed = 0

    def update_state(self, state):
        self.state = state

    def get_lhs(self):
        under_cursor = self.tape[self.pos]
        lhs = self.state + under_cursor
        return lhs

    def get_rhs(self, lhs):
        if lhs not in self.program:
            raise Error('Could not find transition for state "%s".' % lhs)
        return self.program[lhs]

    def move_head(self, move):
        if move == "l":
            self.pos -= 1
        elif move == "r":
            self.pos += 1
        else:
            raise Error('Unknown move "%s". It can only be left or right.' % move)

        if self.pos < 0:
            self.tape.insert(0, self.init)
            self.pos = 0
        if self.pos >= len(self.tape):
            self.tape.append(self.init)

        self.movez += 1


beaver_programs = [
    {
        # 1-state Busy Beaver
        "a0": "h1r"
    },
    {
        # 2-state Busy Beaver
        "a0": "b1r",
        "b0": "a1l",
        "a1": "b1l",
        "b1": "h1r",
    },
    {
        # 3-state Busy Beaver
        "a0": "b1r",
        "a1": "c1l",
        "b1": "b1r",
        "b0": "a1l",
        "c0": "b1l",
        "c1": "h1r",
    },
    {
        # 4-state Busy Beaver
        "a0": "b1r",
        "a1": "b1l",
        "b0": "a1l",
        "b1": "c0l",
        "c0": "h1r",
        "c1": "d1l",
        "d0": "d1r",
        "d1": "a0r",
    },
    {
        # 5-state Busy Beaver
        "a0": "b1r",
        "a1": "c0l",
        "b0": "c1r",
        "b1": "b1r",
        "c0": "a1l",
        "c1": "b0r",
        "d0": "e0r",
        "d1": "h1r",
        "e0": "c1l",
        "e1": "a1r",
    },
    {
        # 6-state Busy Beaver
        # TODO: این دیکشنری در متن ارسالی ناقص بود (فقط عنوان کامنتش اومده بود).
        # ترنزیشن‌های حالت‌های a تا f رو اینجا اضافه کن، مثلاً:
        # "a0": "b1r",
        # "a1": "...",
        # ...
        # "f1": "...",
    },
]


def busy_beaver(n):
    def tape_callback(tape, tape_changed):
        if tape_changed:
            print("".join(tape))
            

    program = beaver_programs[n]

    print("Running Busy Beaver with %d states." % n)
    tm = TuringMachine(program, "a", "h", "0")
    tm.set_tape_callback(tape_callback)
    tm.run()
    print("Busy beaver finished in %d steps." % tm.moves)
    


def usage():
    # TODO: بدنه‌ی این تابع در متن ارسالی نبود.
    print("Usage: python turing_machine.py <n>")
    print("  n: number of states (1-6)")


def main():
    # TODO: بدنه‌ی تابع main هم در متن ارسالی نبود.
    if len(sys.argv) != 2:
        usage()
        return

    n = int(sys.argv[1]) 

    if n < 1 or n > 6:
        print("n must be between 1 and 6 inclusive")
        print()
        usage()
        return

    busy_beaver(n - 1)


if __name__ == "__main__":
    main()
