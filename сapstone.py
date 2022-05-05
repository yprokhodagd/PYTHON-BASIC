import argparse
import configparser
import datetime
import json
import os
import re
import uuid
import logging
from multiprocessing import Pool
from os.path import isdir
from pathlib import Path
from random import randint, choice
import numpy


def run_data_schema(schema):
    # schema = """{"date": "timestamp:", "name": "str:rand", "type": "str:['client', 'partner', 'government']", "age": "int:rand(1, 90)"}"""
    # schema = """{"foo": "int: ['client', 'partner', 'government']"}"""
    # schema = """{"age": "str:rand"}"""
    # schema = """{"name": "str:cat"}"""
    # schema = {"name": "timestamp:"}

    if not type(schema) == dict:
        schema = json.loads(schema)  # convert str to dict

    for key in schema:
        value = type_value = schema[key]
        gen_value = None
        if ":" in schema[key]:
            type_value = schema[key].split(":")[0]
            gen_value = schema[key].split(":")[1]
            if type_value not in ['timestamp', 'int', 'str']:
                logging.error(f"Schema type '{value}' is incorrect")
                exit(1)

        if type_value == "timestamp":
            if gen_value in {"", None}:
                schema[key] = ""
            elif gen_value.startswith("rand("):
                logging.error("rand(from, to) is possible to use only with “int” type")
                exit(1)
            elif gen_value:
                warning = "timestamp does not support any values"
                logging.warning(warning)
            schema[key] = datetime.datetime.now().timestamp()

        elif type_value == "str":
            if gen_value in {"", None}:
                schema[key] = ""
            elif gen_value == "rand":
                schema[key] = str(uuid.uuid4())
            elif gen_value.startswith("rand("):
                logging.error("rand(from, to) is possible to use only with “int” type")
                exit(1)
            elif "rand" in gen_value:
                schema[key] = str(uuid.uuid4())
            elif gen_value.startswith('['):
                value_list = json.loads(gen_value.replace("'", '"'))
                schema[key] = choice(value_list)
            else:
                schema[key] = gen_value

        elif type_value == "int":
            if gen_value in {"", None}:
                schema[key] = "None"
            elif gen_value == "rand":
                schema[key] = randint(0, 10000)
            elif gen_value.startswith("rand("):
                from_to = re.findall(r'\d+', gen_value)
                schema[key] = randint(int(from_to[0]), int(from_to[1]))
            elif gen_value.startswith('['):
                value_list = json.loads(gen_value.replace("'", '"'))
                schema[key] = choice(value_list)
            else:
                logging.error(f'"{gen_value}" is not of "int" type')
                exit(1)

        elif '[' in type_value or type(type_value) == list:
            value_list = json.loads(value.replace("'", '"'))
            schema[key] = choice(value_list)

    return schema


class CU:
    def __init__(self):
        self.PRINT_ALL_TO_CONSOLE = False
        self.setup_log_config()
        self.set_args()

    def setup_log_config(self):
        logging.basicConfig(
            # filename='log.log',
            encoding='utf-8',
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler("log.log"),
                logging.StreamHandler()]
        )

    def set_args(self, argv=None):
        """
        Example of console command:
             python сapstone.py --clear_path --path_to_save_files output/  --file_count 5 --file_name somefile --prefix random --data_lines 10 --multiprocessing 5 --data_schema "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"

        """
        config = configparser.ConfigParser()
        config.read('config.ini')

        parser = argparse.ArgumentParser(description='Console Utility')
        parser.add_argument('--path_to_save_files', dest="path_to_save_files",
                            default=config['DEFAULT']['path_to_save_files'], required=False)
        parser.add_argument('--file_count', dest="file_count", default=config['DEFAULT']['file_count'], required=False)
        parser.add_argument('--file_name', dest="file_name", default=config['DEFAULT']['file_name'], required=False)
        parser.add_argument('--prefix', dest="prefix", default=config['DEFAULT']['prefix'],
                            choices=['count', 'random', 'uuid'], required=False)
        parser.add_argument('--data_schema', dest="data_schema", required=False,
                            default=config['DEFAULT']['data_schema'], help='Descr')
        parser.add_argument('--data_lines', dest="data_lines", default=config['DEFAULT']['data_lines'], required=False)
        parser.add_argument('--clear_path', action='store_true', required=False)
        parser.add_argument('--multiprocessing', dest="multiprocessing_", default=config['DEFAULT']['multiprocessing'],
                            required=False)

        args = parser.parse_args(argv)

        self.path_to_save_files = args.path_to_save_files

        if args.file_count:
            self.files_count = int(args.file_count)
        else:
            self.files_count = int(config['DEFAULT']['file_count'])

        self.file_name = args.file_name

        if args.prefix:
            self.prefix = args.prefix
        else:
            self.prefix = config['DEFAULT']['prefix']

        if args.data_lines:
            self.data_lines = int(args.data_lines)
        else:
            self.data_lines = int(config['DEFAULT']['data_lines'])

        if args.data_schema:
            self.data_schema = args.data_schema
        else:
            self.data_schema = config['DEFAULT']['data_schema']

        self.clear_path = args.clear_path
        self.processes_number = int(args.multiprocessing_)

    def check_files_count(self):
        logging.info('Check files number')
        if self.files_count < 0:
            logging.error("files_count < 0")
            exit(1)
        elif self.files_count == 0:
            for _ in range(self.data_lines):
                print(run_data_schema(self.data_schema))
            exit(0)

    def check_path_is_dir(self):
        """If path is not dir, it makes it dir, adding '/' """

        if self.path_to_save_files == "." or self.path_to_save_files is None:
            self.path_to_save_files = os.getcwd() + "/"

        if not self.path_to_save_files[-1] == "/":
            logging.error(f"{self.path_to_save_files} is not a directory")
            exit(1)

    def clear_dir(self):
        logging.info('Clear directories')

        if self.clear_path and isdir(self.path_to_save_files):
            folder = os.listdir(self.path_to_save_files)

            for file in folder:
                if file.endswith(".json"):
                    os.remove(os.path.join(self.path_to_save_files, file))

    def create_dir_for_files(self):
        if self.PRINT_ALL_TO_CONSOLE:
            return

        logging.info('Create new directories')
        try:
            os.makedirs(os.path.dirname(self.path_to_save_files), exist_ok=False)
        except FileExistsError:
            logging.warning('Folder already exists')

    def prepare_files_with_prefix(self):
        logging.info('Create files')
        prefix = self.prefix
        file_count = self.files_count

        if prefix == "count":
            self.files = [Path(self.path_to_save_files, f"{self.file_name}_{i}.json") for i in range(file_count)]
            print(self.files)
        elif prefix == "random":
            self.files = [Path(self.path_to_save_files,
                               f"{self.file_name}_{choice('abcde')}{randint(0, self.files_count)}{i}.json") for i in
                          range(file_count)]
        elif prefix == "uuid":
            self.files = [Path(self.path_to_save_files, f"{self.file_name}_{str(uuid.uuid4())}.json") for i in
                          range(file_count)]

    def write_files(self, file_list):
        for file in file_list:
            with open(file, 'a') as f:
                for _ in range(self.data_lines):
                    shm = run_data_schema(self.data_schema)
                    f.write(json.dumps(shm) + "\n")

    def precheck_schema(self, data_schema):

        try:
            with open(data_schema, "r") as f:
                self.data_schema = f.read()
                print('precheck', self.data_schema)
                logging.info("Schema is read from file")
        except:
            logging.info("Schema is read from console")
            try:
                if not type(data_schema) == dict:
                    json.loads(data_schema)  # convert str to dict
            except:
                logging.error("Failed to load schema. Schema maybe incorrect")
                exit(1)

    def write_files_multiprocess(self):
        if self.processes_number == 1:
            return self.write_files(self.files)

        logging.info(f'Creates files in parallel {self.processes_number}')
        pool = Pool(self.processes_number)
        equal_parts = numpy.array_split(self.files, self.processes_number)  # split all files to equal parts
        pool.map(self.write_files, equal_parts)

    def check_cpu_cores(self):
        logging.info('Check cpu cores')
        cpu_count = os.cpu_count()
        if self.processes_number <= 0:
            logging.error("multiprocessing should be > 0 ")
            exit(1)
        elif self.processes_number > cpu_count:
            self.processes_number = cpu_count

    def main(self):
        print(self.data_schema)
        logging.info("-------New run------")
        self.check_files_count()
        self.check_path_is_dir()
        self.clear_dir()
        self.create_dir_for_files()
        self.prepare_files_with_prefix()
        self.check_cpu_cores()
        self.precheck_schema(self.data_schema)
        self.write_files_multiprocess()


if __name__ == '__main__':
    cu = CU()
    cu.set_args([
        "--file_count", "2",
        "--clear_path",
        "--path_to_save_files", "output/",
        "--file_name", "file",
        "--prefix", "random",
        "--data_lines", "10",
        "--multiprocessing", "5",
        "--data_schema",
        "{\"date\": \"timestamp\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}",
    ])
    cu.main()
