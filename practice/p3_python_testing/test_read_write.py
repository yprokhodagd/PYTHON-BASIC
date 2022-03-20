"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import os
import tempfile

from practice.p2_python_part_2.task_read_write import readwrite
from project_root import ROOT_DIR


def test_readwrite():
    # prepare
    files_names = ['file_1.txt', 'file_2.txt', 'file_3.txt']
    dest = "practice/p2_python_part_2"
    files = [os.path.join(ROOT_DIR, dest, f) for f in files_names]
    output_file = tempfile.TemporaryFile()

    # tested function
    readwrite(input_files=files, output_file=output_file)

    # check results
    output_file.seek(0)
    output_data = output_file.read().decode()
    assert output_data == '23, 78, 3'
