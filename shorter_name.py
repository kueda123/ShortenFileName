import os
import re

MAX_FILENAME_LENGTH = 255
MP4_EXTENSION = ".mp4"

# for UTF-8.JA_JP support
___UTF8_JA_JP_SUPPORT___ = True
DEFAULT_ENCODING = 'utf-8'
MAX_CHAR_LEN = 3

def get_adjusted_filename(basename, extension=MP4_EXTENSION, footer="", encoding=DEFAULT_ENCODING):
#if ___UTF8_JA_JP_SUPPORT___:
    #
    # Cut off at the character boundary of Japanese UTF-8 Kanji characters
    #
    _max_bytes = MAX_FILENAME_LENGTH - len(extension) - len(footer)
    encoded_basename = basename.encode(encoding)

    # Shave off the last positional character until 
    # it is less than or equal to the value of _max_bytes.
    while len(encoded_basename) > _max_bytes:
        encoded_basename = encoded_basename[:-1]

    # DECODE adjusted base name.
    try:
        _new_basename = encoded_basename.decode(encoding)
        return _new_basename + footer + extension
    except UnicodeDecodeError:
        # エラーが発生した場合、エラーメッセージを出力する
        print(f"***ERROR***: Could not DECODE file name,{encoded_basename}.")
        return ""
#else:
    # Base name of the file is truncated at the maximum length
    filename_length = len(basename) + len(extension)
    if filename_length > MAX_FILENAME_LENGTH:
        _new_basename = basename[:MAX_FILENAME_LENGTH - len(extension)]
    else:
        _new_basename = basename
    return _new_basename + extension

def rename_mp4_files(input_dir, output_dir):
    mp4_files = [
        os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(MP4_EXTENSION)
    ]


    for path in mp4_files:
        dir, filename = os.path.split(path)
        base, extension = os.path.splitext(filename)
        new_base = re.findall(r"「(.*?)」", base, flags=re.UNICODE)[0]
        new_filename = get_adjusted_filename(new_base, extension, footer="")
        new_path = os.path.join(output_dir, new_filename)

        # デバッグ用出力
        if ___DEBUG___:
            print(f"before: {path}")
            print(f"after : {new_path}")

        # 
        # os.rename(path, new_path)


if __name__ == "__main__":
    ___DEBUG___ = True
    input_dir = "/path/to/input/dir"
    output_dir = "/path/to/output/dir"
    rename_mp4_files(input_dir, output_dir)
