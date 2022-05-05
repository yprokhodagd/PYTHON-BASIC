import argparse
import json
import os
import tempfile
import unittest
from datetime import datetime
from unittest import mock

from parameterized import parameterized

from сapstone import CU


class TestClearPath(unittest.TestCase):
    DIR = "output1/"
    FILE = "myfile.json"

    def setUp(self):
        os.mkdir(self.DIR)  # create dir
        open(self.DIR + self.FILE, "x")  # create file

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count="",
                                                file_name=FILE,
                                                prefix="",
                                                data_lines="",
                                                clear_path="True",
                                                data_schema="",
                                                multiprocessing_="1"))
    def test_clear_path_is_on(self, mock_args):
        """Test for the “clear_path” action.

        --clear_path --path_to_save_files output/  --file_count 3 --file_name somefile --prefix random --data_lines 10 --multiprocessing 1 --data_schema
        """
        cu = CU()
        # cu.set_args([
        #     "--clear_path",
        #     "--path_to_save_files", self.DIR,
        #     "--multiprocessing", "1",
        # ])
        cu.main()

        # check that file is deleted with other files
        self.assertFalse(os.path.exists(self.DIR + self.FILE))

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count="",
                                                file_name=FILE,
                                                prefix="",
                                                data_lines="",
                                                clear_path="",
                                                data_schema="",
                                                multiprocessing_="1"))
    def test_clear_path_is_off(self, mock_args):
        """Test for the “clear_path” action.

        --clear_path --path_to_save_files output/  --file_count 3 --file_name somefile --prefix random --data_lines 10 --multiprocessing 1 --data_schema
        """
        cu = CU()
        # cu.set_args([
        #     "--multiprocessing", "1",
        #     "--path_to_save_files", self.DIR,
        # ])
        cu.main()

        # check that file is deleted with other files
        self.assertTrue(os.path.exists(self.DIR + self.FILE))

    def tearDown(self):
        # delete files and folder
        for file in os.listdir(self.DIR):
            if file.endswith(".json"):
                os.remove(os.path.join(self.DIR, file))
        os.rmdir(self.DIR)


class TestCU(unittest.TestCase):
    DIR = "output2/"
    FILE_COUNT = 5
    FILE_NAME = "testsavingfile.json"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count=FILE_COUNT,
                                                file_name=FILE_NAME,
                                                prefix="",
                                                data_lines="",
                                                clear_path="",
                                                data_schema="",
                                                multiprocessing_="1"))
    def test_saving_files(self, mock_args):
        """Test to check saving file to the disk."""

        cu = CU()
        # cu.set_args([
        #     "--multiprocessing", "1",
        #     "--file_name", self.FILE_NAME,
        #     "--file_count", str(self.FILE_COUNT),
        #     "--path_to_save_files", self.DIR,
        # ])
        cu.main()

        # check files count
        files = os.listdir(self.DIR)
        print(files)
        assert len(files) == self.FILE_COUNT

        for file in files:
            # check files name
            assert file.startswith(self.FILE_NAME)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count=FILE_COUNT,
                                                file_name=FILE_NAME,
                                                prefix="",
                                                data_lines="",
                                                clear_path="True",
                                                data_schema="",
                                                multiprocessing_="5"))
    def test_multiprocessing(self, mock_arg):
        """Write a test to check a number of created files if “multiprocessing” > 1."""

        cu = CU()
        # cu.set_args([
        #     "--multiprocessing", "5",
        #     "--file_name", self.FILE_NAME,
        #     "--file_count", str(self.FILE_COUNT),
        #     "--path_to_save_files", self.DIR,
        # ])
        cu.main()

        files = os.listdir(self.DIR)

        # check files count
        assert len(files) == self.FILE_COUNT

        for file in files:
            # check files name
            assert file.startswith(self.FILE_NAME)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count=FILE_COUNT,
                                                file_name=FILE_NAME,
                                                prefix="",
                                                data_lines="10",
                                                clear_path="True",
                                                data_schema="",
                                                multiprocessing_="1"))
    def test_data_lines(self, mock_args):
        """Write your own test."""

        DATA_LINES = "10"

        cu = CU()
        # cu.set_args([
        #     "--multiprocessing", "1",
        #     "--data_lines", DATA_LINES,
        #     "--file_name", self.FILE_NAME,
        #     "--file_count", "1",
        #     "--path_to_save_files", self.DIR,
        # ])
        cu.main()

        file = os.listdir(self.DIR)[0]
        with open(self.DIR + file, 'r') as f:
            lines = f.readlines()
            print(lines)

        assert len(lines) == int(DATA_LINES)


    # -------------test------------------
    DATA = "{\"tempfile\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\", \"age\": \"int:rand(1, 90)\"}"
    # create temp file
    tmp_input_file = tempfile.NamedTemporaryFile(delete=False)

    # write temp file as str
    with open(tmp_input_file.name, 'w') as f:
        f.write(DATA)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(path_to_save_files=DIR,
                                                file_count="1",
                                                file_name=FILE_NAME,
                                                prefix="",
                                                data_lines="1",
                                                clear_path="True",
                                                data_schema=tmp_input_file.name,
                                                multiprocessing_="1"))
    def test_with_temp_files(self, mock_args):

        cu = CU()
        # cu.set_args([
        #     "--multiprocessing", "1",
        #     "--data_lines", "1",
        #     "--file_name", self.FILE_NAME,
        #     "--file_count", "1",
        #     "--path_to_save_files", self.DIR,
        #     "--data_schema", tmp_input_file.name
        # ])
        cu.main()

    def tearDown(self):
        # delete files and folder
        for file in os.listdir(self.DIR):
            if file.endswith(".json"):
                os.remove(os.path.join(self.DIR, file))
        os.rmdir(self.DIR)


class TestSchema(unittest.TestCase):
    """Write a parameterized test for different data types."""

    DIR = "test_output/"
    FILE_NAME = "test_schema"

    @parameterized.expand([
        ("timestamp", int(datetime.now().timestamp())),
        ("str", ""),
        ("int", "None"),
        ("str:cat", "cat"),
    ])
    def test_data_types(self, act_value, expected_value):
        """Write a parameterized test for different data types"""

        data = str({"key": act_value}).replace("'", "\"")

        cu = CU()
        cu.set_args([
            "--clear_path",
            "--data_lines", "1",
            "--multiprocessing", "1",
            "--file_name", self.FILE_NAME,
            "--file_count", "1",
            "--path_to_save_files", self.DIR,
            "--data_schema", data
        ])
        cu.main()

        file = os.listdir(self.DIR)[0]
        with open(self.DIR+file, 'r') as f:
            data_from_file = json.loads(f.readline())
            actual_value = data_from_file["key"]

            if act_value == "timestamp":
                assert str(actual_value)[:9] == str(expected_value)[:9]
            else:
                assert actual_value == expected_value

    @parameterized.expand([
        ("filename1", "{\"date\": \"timestamp\",\"name\": \"str:rand\"}"),
        ("filename2", "{}"),
        ("filename3", "{\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"),
    ])
    def test_diff_data_schemas(self, filename, data):
        """Write a parameterized test for different data schemas."""

        cu = CU()
        cu.set_args([
            "--clear_path",
            "--data_lines", "1",
            "--multiprocessing", "1",
            "--file_name", filename,
            "--file_count", "1",
            "--path_to_save_files", self.DIR,
            "--data_schema", data
        ])
        cu.main()

        file = os.listdir(self.DIR)[0]

        # checkfile exist
        assert file.startswith(filename)

        with open(self.DIR+file, 'r') as f:
            data_from_file = json.loads(f.readline())

        # check values are not empty
        for k in data_from_file.keys():
            assert data_from_file[k] != ""

    def tearDown(self):
        # delete files and folder
        for file in os.listdir(self.DIR):
            if file.endswith(".json"):
                os.remove(os.path.join(self.DIR, file))
        os.rmdir(self.DIR)
