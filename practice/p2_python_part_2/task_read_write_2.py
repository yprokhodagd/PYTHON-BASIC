"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=5):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def fill(output1, output2, ):
    words = generate_words()
    words_str = '\n'.join(words)

    words_revers = words[::-1]
    words_revers_str = ','.join(words_revers)

    output1.write(str.encode(words_str))
    output2.write(str.encode(words_revers_str))

    return words_str, words_revers_str

