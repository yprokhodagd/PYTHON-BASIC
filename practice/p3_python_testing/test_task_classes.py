"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
from datetime import datetime

from practice.p2_python_part_2.task_classes import Teacher
from practice.p2_python_part_2.task_classes import Student


def test_names():
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    assert teacher.last_name == "Orlyakov"
    assert student.first_name == 'Vladislav'


def test_expired_homework():
    teacher = Teacher('Dmitry', 'Orlyakov')
    expired_homework = teacher.create_homework('Learn functions', 0)
    assert str(expired_homework.created).split('.')[0] == str(datetime.now()).split('.')[0]
    assert str(expired_homework.deadline) == "0:00:00"
    assert expired_homework.text == 'Learn functions'


def test_create_homework():
    teacher = Teacher('Dmitry', 'Orlyakov')
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    assert str(oop_homework.deadline) == "5 days, 0:00:00"
