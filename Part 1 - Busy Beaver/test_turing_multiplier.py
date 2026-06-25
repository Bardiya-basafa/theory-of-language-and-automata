# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

# create the Turing machine
transitions = {
    # start
    ("q0", "1"): ("get", "", "R"),
    # get
    ("get", "1"): ("right", "", "R"),
    ("get", "0"): ("cleanup", "", "R"),
    # right
    ("right", "1"): ("right", "1", "R"),
    ("right", "0"): ("read", "0", "R"),
    # read
    ("read", "1"): ("copy", "X", "R"),
    ("read", "X"): ("read", "X", "R"),
    # copy
    ("copy", "1"): ("moreCopy", "Z", "R"),
    ("copy", "Y"): ("lastCopy", "1", "R"),
    ("copy", ""): ("restart", "1", "L"),
    # moreCopy
    ("moreCopy", "1"): ("moreCopy", "1", "R"),
    ("moreCopy", "Y"): ("moreCopy", "Y", "R"),
    ("moreCopy", ""): ("findNext", "Y", "L"),
    # findNext
    ("findNext", "1"): ("findNext", "1", "L"),
    ("findNext", "Y"): ("findNext", "Y", "L"),
    ("findNext", "Z"): ("copy", "X", "R"),
    # lastCopy
    ("lastCopy", "1"): ("lastCopy", "1", "R"),
    ("lastCopy", "X"): ("lastCopy", "1", "R"),
    ("lastCopy", "Y"): ("lastCopy", "1", "R"),
    ("lastCopy", ""): ("restart", "1", "L"),
    # restart
    ("restart", "0"): ("restart", "0", "L"),
    ("restart", "1"): ("restart", "1", "L"),
    ("restart", "X"): ("restart", "X", "L"),
    ("restart", ""): ("get", "", "R"),
    # cleanup
    ("cleanup", "1"): ("cleanup", "1", "R"),
    ("cleanup", "X"): ("cleanup", "1", "R"),
    ("cleanup", ""): ("qa", "", "L"),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:", w)
        print("Accepted" if machine.accepts(w, step_limit=1000) else "Rejected")
        machine.debug(w, step_limit=1000, colored=True)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111
    # 2 * 3 = 6

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111
    # 3 * 4 = 12

    # SHOULD ACCEPT
    run("101111")
    # outputs 1111
    # 1 * 4 = 4

    # SHOULD ACCEPT
    run("1101111")
    # outputs 111111111111
    # 2 * 4 = 8
