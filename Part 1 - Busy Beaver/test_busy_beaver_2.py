# -*- coding: utf-8 -*-
from turing_machine import TuringMachine

# create the Turing machine
bbeaver2 = TuringMachine(
    {
        ("a", "0"): ("b", "1", "R"),
        ("b", "0"): ("a", "1", "L"),
        ("a", "1"): ("b", "1", "L"),
        ("b", "1"): ("h", "1", "R"),
    },
    start_state="a",
    accept_state="h",
    reject_state="r",
    blank_symbol="0",
)
bbeaver3 = TuringMachine(
    {
        ("a", "0"): ("b", "1", "R"),
        ("a", "1"): ("c", "1", "L"),
        ("b", "1"): ("b", "1", "R"),
        ("b", "0"): ("a", "1", "L"),
        ("c", "0"): ("b", "1", "L"),
        ("c", "1"): ("h", "1", "R"),
    },
    start_state="a",
    accept_state="h",
    reject_state="r",
    blank_symbol="0",
)
bbeaver4 = TuringMachine(
    {
        ("a", "0"): ("b", "1", "R"),
        ("a", "1"): ("b", "1", "L"),
        ("b", "0"): ("a", "1", "L"),
        ("b", "1"): ("c", "0", "L"),
        ("c", "0"): ("h", "1", "R"),
        ("c", "1"): ("d", "1", "L"),
        ("d", "0"): ("d", "1", "R"),
        ("d", "1"): ("a", "0", "R"),
    },
    start_state="a",
    accept_state="h",
    reject_state="r",
    blank_symbol="0",
)
bbeaver5 = TuringMachine(
    {
        ("a", "0"): ("b", "1", "R"),
        ("a", "1"): ("c", "1", "L"),
        ("b", "0"): ("c", "1", "R"),
        ("b", "1"): ("b", "1", "R"),
        ("c", "0"): ("d", "1", "R"),
        ("c", "1"): ("e", "0", "L"),
        ("d", "0"): ("a", "1", "L"),
        ("d", "1"): ("d", "1", "L"),
        ("e", "0"): ("h", "1", "h"),
        ("e", "1"): ("a", "0", "L"),
    },
    start_state="a",
    accept_state="h",
    reject_state="r",
    blank_symbol="0",
)

if __name__ == "__main__":

    def run(input_):
        w = input_
        # the same as mine 4 ones
        # This is an optimal BB-2. 4 is the maximum number of 1s you can get for 2 states
        print("BB with 2 states")
        bbeaver2.debug(w, step_limit=1000)
        print()
        # 6
        print("BB with 3 states")
        bbeaver3.debug(w, step_limit=1000)
        print()
        # 13
        print("BB with 4 states")
        bbeaver4.debug(w, step_limit=1000)
        print()
        # This machine runs for 47176870 steps, writing 4098 1s, and then halts. So BB(5) is at least 47176870
        # print("BB with 5 states")
        # bbeaver5.debug(w, step_limit=47176870)
        # print()
        # The busy beaver function is defined so that
        # \Sigma(n) = max { \sigma(M) | M is a halting n-state 2-symbol Turing machine}
        # The maximum is unique if it exists, which it does (Rado proved this). This is just a number.
        #
        # Therefore \Sigma(n) is also unique, and so the discrete function \Sigma: N --> N is also unique.
        # The busy beaver function is a function which tells you the maximum score for all n-state Turing machines.
        # There is only one function. However, there are multiple Turing machines which attain this maximum
        # [4(n+1)]^2n so 5 state have 24^10 different TM with 5 states. (for each nonhalting state, there are two
        # transitions out, so there are 2n total transitions, and each transition have 2 possibilities for the symbol
        # being written, 2 possibilities for the direction to move - left or right, and (n+1) possibilities for what
        # states to go - including the halting state)

        # if we can calculate BB(n), we can solve the halting problem by converting the input program to
        # a machine of the required type and determining its size n, calculating BB(n) and running the machine.
        # If it runs more than BB(n) steps, then, by definition, it must run forever.

    run("00000000000000")  # 14 0

# bbeaver.debug('00000000000000', step_limit=1000)
