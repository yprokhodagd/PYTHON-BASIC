"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""

import unittest
from unittest.mock import patch


def readnumber():
    number = input()
    if str(number).isdigit():
        return number
    else:
        raise Exception("not a number!")


class TestListSum(unittest.TestCase):

    @patch('builtins.input', return_value=1)
    def test_read_numbers_without_text_input(self, mock_input):
        result = readnumber()
        self.assertEqual(result, 1)

    @patch('builtins.input', return_value="text")
    def test_read_numbers_with_text_input(self, mock_input):
        with self.assertRaises(Exception) as context:
            readnumber()

        self.assertTrue("not a number!", context.exception)
