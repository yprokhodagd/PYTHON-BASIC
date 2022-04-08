import os
from multiprocessing import Process
from random import randint

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def func1(array: list):
    for i in array:
        with open(str(i) + ".txt", 'w') as f:
            f.write(str(fib(i)))


def func2(result_file: str):
    with open(result_file, 'a') as result_file:
        for file in os.listdir():
            if file.endswith(".txt") and file != result_file.name:
                with open(file, "r") as f:
                    data = str(file.replace(".txt", "") + ", " + f.read() + "\n")
                    result_file.write(data)


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # run ordinary
    # func1(array=[randint(1, 5) for _ in range(5)])
    # func2(result_file="result.txt")

    # run in parrallel
    p1 = Process(target=func1, args=([randint(1, 5) for _ in range(5)], ))
    p2 = Process(target=func2, args=("result.txt",))
    p1.start()
    p2.start()
    p1.join()
    p2.join()