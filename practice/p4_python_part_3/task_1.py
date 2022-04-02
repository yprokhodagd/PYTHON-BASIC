"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2022-03-27')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2022-03-25')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime


def calculate_days(from_date: str) -> int:
    try:
        date2 = datetime.fromisoformat(from_date)
    except ValueError:
        print("WrongFormatException")
    else:
        date_diff = datetime.now() - date2
        day = str(date_diff).split("day")[0]
        return int(day)


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""


def test_calculate_days(freezer, capfd):
    freezer.move_to('2022-03-26')
    assert calculate_days('2022-03-27') == -1

    assert calculate_days('2022-03-25') == 1


def test_calculate_days_exception(freezer, capfd):
    calculate_days('10-07-2021')
    out, err = capfd.readouterr()
    assert out == "WrongFormatException\n"
