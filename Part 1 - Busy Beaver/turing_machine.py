# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton."""

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
        # setting turing machine parameters
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

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
        # check if the input is str, if it is convert it to list
        if isinstance(input_, str):
            tape = list(input_)
        else:
            tape = input_

        # cacluating left and right tape of the current symbol using two lists (left list is invert)
        left = []
        if tape:
            symbol = tape[0]
            right = tape[1:]
        else:
            symbol = self.blank_symbol
            right = []

        current_state = self.start_state
        # returning the initial state
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
                # add the symbol to left handside tape and go right
                left.insert(0, symbol)
                if right:
                    symbol = right[0]
                    right.pop(0)
                else:
                    symbol = self.blank_symbol

            elif direction == "L":
                # add the symbol to right handside tape and go left
                right.insert(0, symbol)
                if left:
                    symbol = left[0]
                    left.pop(0)
                else:
                    symbol = self.blank_symbol

            else:
                # niether of R an L so it is bad input
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
        # creating the turing generator
        turing_gen = self.run(input_)

        # going through the step limits until machine halt
        for _ in range(step_limit):
            try:
                action, conf = next(turing_gen)
                if action == "Accept":
                    return True
                elif action == "Reject":
                    return False
            except StopIteration:
                break
        # logging that the machine did not halt
        logging.warning(
            "the step limit has reached and input not accepted nor rejected"
        )
        return None

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        # just returning the not of the accept result
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
        halted = False
        for step, (action, config) in enumerate(islice(self.run(input_), step_limit)):

            # getting config properties
            state = config["state"]
            left = config["left_hand_side"]
            right = config["right_hand_side"]
            symbol = config["symbol"]

            # make the left and right string (left should be revered)
            left = "".join(reversed(left))
            right = "".join(right)
            # construct the tape
            if colored:
                # adding color to the current symbol
                tape = f"{left}\033[91m{symbol}\033[0m{right}"
            else:
                tape = f"{left}{symbol}{right}"

            if action is None:
                print(f"step {step}, state: {state}, symbol: {symbol}")
                print(f"\ttape: {tape}")
                print()
            else:
                halted = True
                return
        # logging that machine did not halt
        if not halted:
            logging.warning("Debug stopped after reaching the step limit.")
