"""
Create virtual environment and pip install Faker only for this venv.

Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.

Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider

Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import unittest
from unittest.mock import Mock

from faker import Faker


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('NUMBER', type=int)
    parser.add_argument('--fake_address', type=str)
    parser.add_argument('--some_name', type=str)
    args = parser.parse_args()
    return args


def print_name_address(args: argparse.Namespace) -> None:
    list_of_dict = []
    faker = Faker()

    for i in range(args.NUMBER):
        name = faker.name()
        address = faker.address()

        if args.fake_address:
            address = args.fake_address
        if args.some_name:
            name = args.some_name

        list_of_dict.append({"some_name": name, "fake_address": address})

    return list_of_dict


"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


class TTT(unittest.TestCase):

    def test_print_name_address(self):
        m = Mock()
        m.NUMBER = 1
        res = print_name_address(m)
        print(res)
