import re

def get_idx(replace):
    m1 = re.match(r"^\$([0-9]*)$", replace)
    if m1 is None:
        raise ValueError("置換文字列の値が数値に変換できません。")
    return int(m1.group(1))


def selecter(filename, patterns):
  for pattern in patterns:
    if re.match(pattern.get("prefix"), filename):
      return pattern

  return None


def do_replace(pattern, replace, filename):
    m = re.match(pattern, filename)
    if m is None:
        raise ValueError("The pattern `", pattern, "` was not matched.")
    group_idx = get_group_idx(replace)
    if group_idx > m.lastindex():
        raise ValueError("The group index `", group_idx, "` is out of range.")
    return m.group(group_idx)


def rename(filename, patterns):
    selected_pattern = selecter(filename, patterns)

    if selected_pattern:
        for i, transfer in enumerate(selected_pattern.get("transfers")):
            pattern = transfer.get("pattern")
            replace = transfer.get("replace")
            try:
                filename = do_replace(pattern, replace, filename)
            except ValueError as e:
                print("The pattern `", pattern, "` was not matched at `", i, "`.", file=sys.stderr)
                raise

        suffix = selected_pattern.get("suffix")
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
    {
      "prefix": "^「(.*?)」",
      "transfers": [
        { "pattern": "^「",    "replace": "$1" },
        { "pattern": "(.*)",  "replace": "$1_MAC" },
      ],
      "suffix": "_MAD"
    },  ]

  filenames = ["「ファイル名1」.mp4", "「ファイル名2」.mp4"]

  for filename in filenames:
    new_filename = rename(filename, patterns)
    print(new_filename)


if __name__ == "__main__":
  main()
