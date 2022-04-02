"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math


def math_calculate(function: str, *args):
    try:
        method_to_call = getattr(math, function)
        return method_to_call(*args)
    except AttributeError:
        print("OperationNotFoundException")


"""
Write tests for math_calculate function
"""


def test_math_calculate():
    assert math_calculate('log', 1024, 2) == 10.0

    assert math_calculate('ceil', 10.7) == 11


def test_math_calculate_exception(capfd):
    math_calculate('unknown_function', 10.7)
    out, err = capfd.readouterr()
    assert out == "OperationNotFoundException\n"