"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""


def readwrite(input_files, output_file):
    output = []
    for file in input_files:
        with open(file, 'r') as f:
            data = f.read()
            output.append(data)
    output = ", ".join(output)

    output_file.write(str.encode(output))


if __name__ == "__main__":
    pass
    # readwrite(['file_1.txt', 'file_2.txt', 'file_3.txt'], 'result.txt')
