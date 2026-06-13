# -*- coding: utf-8 -*-
"""
Student self-check test script for Turing Machine Simulator implementation.
Save this file as student_test_turing.py in your project directory and run it:
    python student_test_turing.py
"""

import sys
import logging

try:
    from turing_machine import TuringMachine
    print("✅ Successfully imported TuringMachine from turing_machine.py!")
except ImportError:
    print("❌ Error: Could not import TuringMachine from turing_machine.py.")
    print("Make sure turing_machine.py exists in the same folder and contains a class named TuringMachine.")
    sys.exit(1)


def test_basic_acceptance():
    print("\n--- Test 1: Basic Acceptance of a Single Symbol ---")
    # A simple machine that accepts a single '#' and rejects anything else
    transitions = {
        ('q0', '#'): ('saw_#', '#', 'R'),
        ('saw_#', ''): ('qa', '', 'R'),
    }
    
    try:
        machine = TuringMachine(transitions)
        
        # Test accepts
        assert machine.accepts('#') is True, "Should accept '#'"
        print("✅ Correctly accepted '#'")
        
        # Test rejects
        assert machine.rejects('##') is True, "Should reject '##'"
        print("✅ Correctly rejected '##'")
        
        assert machine.rejects('1') is True, "Should reject '1'"
        print("✅ Correctly rejected '1'")
        
        print("🎉 Test 1 passed successfully!")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        return False
    return True


def test_generator_structure():
    print("\n--- Test 2: Generator and Configuration Output Structure ---")
    transitions = {
        ('q0', '1'): ('q1', 'x', 'R'),
        ('q1', ''): ('qa', '', 'R'),
    }
    
    try:
        machine = TuringMachine(transitions)
        steps = list(machine.run('1'))
        
        # Verify generator yielded configurations
        assert len(steps) >= 2, "Generator should yield at least two steps (initial and final)"
        
        first_step = steps[0]
        assert isinstance(first_step, tuple) and len(first_step) == 2, "Each step must be a tuple of (action, configuration)"
        
        action, config = first_step
        assert action is None, "First action should be None as the machine is still running"
        
        expected_keys = {'state', 'left_hand_side', 'symbol', 'right_hand_side'}
        assert isinstance(config, dict) and expected_keys.issubset(config.keys()), \
            f"Configuration should be a dictionary with keys: {expected_keys}"
            
        print("✅ Generator yielded correctly structured tuples.")
        print("✅ Configuration dictionary matches the unified interface specification.")
        print("🎉 Test 2 passed successfully!")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        return False
    return True


def test_tape_boundary_single_sided():
    print("\n--- Test 3: Tape Boundary Behavior ---")
    # A machine that moves left from the initial cell q0 -> L -> q1 -> R -> qa
    transitions = {
        ('q0', '1'): ('q1', '1', 'L'),
        ('q1', '1'): ('qa', '1', 'R'),
    }
    
    try:
        machine = TuringMachine(transitions)
        
        # Note: If your double-sided tape is not implemented yet,
        # it should log a warning but still run without throwing syntax/runtime errors.
        print("Testing execution that triggers a leftward move from the first cell:")
        machine.accepts('1')
        print("✅ Test 3 ran without crashing.")
        print("🎉 Test 3 completed successfully!")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        return False
    return True


if __name__ == "__main__":
    print("==================================================")
    print("         TURING MACHINE SIMULATOR SELF-CHECK      ")
    print("==================================================")
    
    t1 = test_basic_acceptance()
    t2 = test_generator_structure()
    t3 = test_tape_boundary_single_sided()
    
    print("\n==================================================")
    if t1 and t2 and t3:
        print("🎉 CONGRATULATIONS! Your TuringMachine simulator passes all basic self-tests.")
        print("Ready for Part II and Part III! Next, try running the provided examples.")
    else:
        print("❌ Warning: Some self-tests failed. Please check your implementation in turing_machine.py.")
    print("==================================================")
