# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

# create the Turing machine
transitions = {
    # going over the firs ones
    ("q0", "1"): ("q0", "1", "R"),
    # convert the middle zero to one
    ("q0", "0"): ("q1", "1", "R"),
    # again go over ones
    ("q1", "1"): ("q1", "1", "R"),
    # find the first blank at right and go back left
    ("q1", ""): ("q2", "", "L"),
    # conver the right most one to blank and accept
    ("q2", "1"): ("qa", "", "R"),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:", w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, colored=True)
        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 11111
    # 2 + 3 = 5

    # SHOULD ACCEPT
    run("11101111")
    # outputs 1111111
    # 3 + 4 = 7

    # SHOULD ACCEPT
    run("0111")
    # outputs 111
    # 0 + 3 = 3
