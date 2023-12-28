import os
import re

MAX_FILENAME_LENGTH = 255
MP4_EXTENSION = ".mp4"
DEFAULT_ENCODING = 'utf-8'

def get_bytes_length(filename, encoding=DEFAULT_ENCODING):
    """
    Returns the byte length of the filename
    """
    the_bytes = filename.encode(encoding)
    return len(the_bytes)

def has_4bytes_char(filename):
    """
    Search for 4-byte character strings
    """
    return re.findall(r"[\uD800-\uDBFF][\uDC00-\uDFFF]", filename)

def get_max_char_bytes(basename):
    """
    Get the maximum length of the charactor in Japanese UTF-8 characters.
    return:
        4: If it contains a 4-byte string,
        3: Others
    """
    # Get the maximum length of the charactor in Japanese UTF-8 characters.
    return 4 if any(ord(c) >= 1280 for c in basename) else 3

def truncate_filename_at_word_boundary(basename, max_basename_bytes):
    """
    Shorten the base name to the maximum character boundary
    """
    exceeded_bytes = get_bytes_length(basename) - max_basename_bytes
    if exceeded_bytes > 0:
        basename = basename[:-(exceeded_bytes//get_max_char_bytes(basename))]
        while get_bytes_length(basename, encoding) > exceeded_bytes:
            basename = basename[:-1]
    return basename

def remaining_bytes(footer, extension, encoding="utf-8"):
    """
    Returns the maximum remaining byte length

    Args:
        footer: Footer string
        extension: Extension string
        encoding: encoding

    Returns:
       Return byte length not already consumed by footer and extension
    """
    footer_bytes = footer.encode(encoding)
    extension_bytes = extension.encode(encoding)
    return MAX_FILENAME_LENGTH - len(footer_bytes) - len(extension_bytes)

def get_adjusted_filename(basename: str, extension: str = MP4_EXTENSION, 
                          footer: str = "", encoding: str = "utf-8") -> str:
    """
    Returns an adjusted filename that does not exceed the maximum length.
    The filename is truncated at the word boundary if it exceeds the maximum length.

    Args:
        basename: The base name of the filename.
        extension: The file extension.
        footer: A footer to be added to the filename.
        encoding: The encoding of the filename.

    Returns:
        The adjusted filename.
    """
    # Get the maximum length of the filename.
    max_basename_bytes = remaining_bytes(footer, extension,  encoding)

    # If the filename is longer than the maximum length, truncate it from the end.
    basename = truncate_filename_at_word_boundary(basename, max_basename_bytes)

    # Add the extension to the filename.
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
