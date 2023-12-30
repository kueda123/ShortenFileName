import re

def test():
    filename = "「ファイル名1」.mp4"

    pattern = "^「(.*?)」.mp4$"

    m = re.match(pattern, filename)

    # m.group(1)

    print(m.group(1))

    # idx = 1; m.group(idx)

    idx = 1
    print(m.group(idx))


if __name__ == "__main__":
    test()
