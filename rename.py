import re

def rename(filename, patterns):
  for pattern in patterns:
    prefix = pattern.get("prefix")
    transfers = pattern.get("transfers")
    suffix = pattern.get("suffix")

    if prefix:
      filename = re.sub(prefix, "", filename)

    for transfer in transfers:
      pattern = transfer.get("pattern")
      replace = transfer.get("replace")

      filename = re.sub(pattern, replace, filename)

    if suffix:
      filename = filename + suffix

  return filename


def main():
  patterns = [
    {
      "prefix": "^「(.*?)」：",
      "transfers": [
        { "pattern": "^「",    "replace": "$1" },
        { "pattern": "(.*)",  "replace": "$1_MAC" },
      ],
      "suffix": "_MAC"
    },
  ]

  filenames = ["「ファイル名1」.mp4", "「ファイル名2」.mp4"]

  for filename in filenames:
    new_filename = rename(filename, patterns)
    print(new_filename)


if __name__ == "__main__":
  main()
