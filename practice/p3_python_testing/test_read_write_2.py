"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import tempfile

from practice.p2_python_part_2.task_read_write_2 import fill


def test_readwrite():
    output_file1 = tempfile.TemporaryFile()
    output_file2 = tempfile.TemporaryFile()

    text1, text2 = fill(output_file1, output_file2)

    output_file1.seek(0)
    assert output_file1.read().decode() == text1

    output_file2.seek(0)
    assert output_file2.read().decode() == text2