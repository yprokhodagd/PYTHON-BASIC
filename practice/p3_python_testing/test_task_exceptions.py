"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import pytest

from practice.p2_python_part_2.task_exceptions import division


def test_division_ok(capfd):
    assert division(3, 2) == 1.5


def test_division_by_zero(capfd):
    division(3, 0)
    out, err = capfd.readouterr()
    assert out == 'Division by 0\nDivision finished\n'


def test_division_by_one(capfd):
    with pytest.raises(Exception, match=r"Deletion on 1 get the same result"):
        division(3, 1)
