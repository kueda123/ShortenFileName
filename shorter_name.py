import os
import re

MAX_FILENAME_LENGTH = 255
MP4_EXTENSION = ".mp4"
DEFAULT_ENCODING = 'utf-8'
MAX_CHAR_LEN = 3

def get_bytes_length(filename, encoding=DEFAULT_ENCODING):
    utf8_strings = filename.encode(encoding)
    return len(utf8_strings)

def get_adjusted_filename(basename, extension=MP4_EXTENSION, footer="", encoding=DEFAULT_ENCODING):
    #
    # Cut off at the character boundary of Japanese UTF-8 Kanji characters
    #
    extension_bytes = get_bytes_length(extension)
    footer_bytes = get_bytes_length(footer)
    _max_bytes = MAX_FILENAME_LENGTH - extension_bytes - footer_bytes
 
    # Shave off the last positional character until 
    # it is less than or equal to the value of _max_bytes.
    exceeded_bytes = get_bytes_length(basename, encoding) - _max_bytes
    if exceeded_bytes > 0:
        basename = basename[:-(exceeded_bytes // MAX_CHAR_LEN) ]
        while get_bytes_length(basename, encoding) > _max_bytes:
            basename = basename[:-1]
 
    return basename + footer + extension

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

        # os.rename(path, new_path)


if __name__ == "__main__":
    ___DEBUG___ = True
    input_dir = "/path/to/input/dir"
    output_dir = "/path/to/output/dir"
    rename_mp4_files(input_dir, output_dir)
