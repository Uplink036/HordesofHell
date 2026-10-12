from data.convert.simple_file import INPUT_FILE, convert_file_to_simple_format


def convert_data_files():
    convert_file_to_simple_format(INPUT_FILE, allow_existing=True)


if __name__ == "__main__":
    convert_data_files()
