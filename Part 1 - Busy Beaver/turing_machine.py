# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

Accepting '#'
=============

>>> from turing_machine import TuringMachine

Instantiate the machine with particular transitions.

>>> one_hash = TuringMachine(
...     {
...         ('q0', '#'): ('saw_#', '#', 'R'),
...         ('saw_#', ''): ('qa', '', 'R'),
...     }
... )

Check whether it accepts a string:

>>> one_hash.accepts('#')
True

>>> one_hash.accepts('##')
False

Check whether it rejects a string:

>>> one_hash.rejects('#')
False

>>> one_hash.rejects('##')
True

"""

import logging
from itertools import islice


class TuringMachine:
    """Turing machine simulator class.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :blank_symbol: the special symbol that marks the tape cell to be empty.

    """

    def __init__(
        self,
        transitions,
        start_state="q0",
        accept_state="qa",
        reject_state="qr",
        blank_symbol="",
    ):
        # TODO: Implement the constructor. Initialize transitions, start_state, accept_state,
        # reject_state, blank_symbol, and any other helpful structures.
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        pass

    def run(self, input_):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.

        The action is either 'Accept', 'Reject' or None.

        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.

        """
        # TODO: Implement the simulator loop as a Python generator.
        # 1. Initialize the tape using two lists (left_hand_side and right_hand_side) and the current symbol.
        # 2. Yield the current step (action, configuration).
        # 3. Read transitions and update state, write symbols, and move the head ('L' or 'R').
        # 4. Handle tape expansion dynamically for both left and right directions (double-sided infinite tape).
        # 5. Log a warning using logging.warning() if the singly-infinite tape boundary is crossed before Part III.
        if isinstance(input_, str):
            tape = list(input_)
        else:
            tape = input_
        left = []
        if tape:
            symbol = tape[0]
            right = tape[1:]
        else:
            symbol = self.blank_symbol
            right = []

        current_state = self.start_state

        yield (
            None,
            {
                "state": current_state,
                "left_hand_side": list(left),
                "symbol": symbol,
                "right_hand_side": list(right),
            },
        )

        while True:

            # input accepted
            if current_state == self.accept_state:
                yield (
                    "Accept",
                    {
                        "state": current_state,
                        "left_hand_side": list(left),
                        "symbol": symbol,
                        "right_hand_side": list(right),
                    },
                )
                return

            # input rejected
            if current_state == self.reject_state:
                yield (
                    "Reject",
                    {
                        "state": current_state,
                        "left_hand_side": list(left),
                        "symbol": symbol,
                        "right_hand_side": list(right),
                    },
                )
                return

            # go in transition

            # current trasition can be made
            key = (current_state, symbol)
            if key not in self.transitions:
                # we are not in accept state and halt which means reject
                yield (
                    "Reject",
                    {
                        "state": current_state,
                        "left_hand_side": list(left),
                        "symbol": symbol,
                        "right_hand_side": list(right),
                    },
                )
                return

            next_state, write_symbol, direction = self.transitions[key]

            # write new symbol to input
            symbol = write_symbol

            # move head
            if direction == "R":
                left.insert(0, symbol)
                if right:
                    symbol = right[0]
                    right.pop(0)
                else:
                    symbol = self.blank_symbol

            elif direction == "L":
                right.insert(0, symbol)
                if left:
                    symbol = left[0]
                    left.pop(0)
                else:
                    symbol = self.blank_symbol

            else:
                yield (
                    "Bad Input",
                    {
                        "state": current_state,
                        "left_hand_side": list(left),
                        "symbol": symbol,
                        "right_hand_side": list(right),
                    },
                )
                return

            # move to next state
            current_state = next_state

            # yield the result
            yield (
                None,
                {
                    "state": current_state,
                    "left_hand_side": list(left),
                    "symbol": symbol,
                    "right_hand_side": list(right),
                },
            )

    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """
        # TODO: Run the generator up to step_limit and check the action of the final yielded state.
        # Remember to log a warning if the step_limit is reached without halting.

        turing_gen = self.run(input_)

        for _ in range(step_limit):
            try:
                action, conf = next(turing_gen)
                if action == "Accept":
                    return True
                elif action == "Reject":
                    return False
            except StopIteration:
                break

        logging.warning(
            "the step limit has reached and input not accepted nor rejected"
        )
        return None

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        # TODO: Determine rejection by checking if accepts() returns False.
        result = self.accepts(input_=input_)
        if result is None:
            return None

        return not result

    def debug(self, input_, step_limit=100, colored=False):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        # TODO: Loop over the steps yielded by run() up to step_limit and print the tape configuration.
        # E.g., print the state and the tape with the head highlighted in brackets like: left[symbol]right
        for step, (action, config) in enumerate(islice(self.run(input_), step_limit)):

            # getting config properties
            state = config["state"]
            left = config["left_hand_side"]
            right = config["right_hand_side"]
            symbol = config["symbol"]

            # make the left and right string (left should be revered)
            left = "".join(reversed(left))
            right = "".join(right)

            if colored:
                tape = f"{left}\033[91m{symbol}\033[0m{right}"
            else:
                tape = f"{left}{symbol}{right}"

            if action is None:
                print(f"step {step}, state: {state}, symbol: {symbol}")
                print(f"\ttape: {tape}")
                print()
            else:
                print(f"step {step}, state: {state}, symbol: {symbol}")
                print(f"\ttape: {tape}")
                print()
                halted = True
                return

            # logging.warning("Debug stopped after reaching the step limit.")
