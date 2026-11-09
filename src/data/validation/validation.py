import re
from dataclasses import dataclass

import pandas as pd

ANYTHING_IN_ROW = r".*"


@dataclass
class CSVValidator:
    csv_path: str
    expected_columns: tuple[str, ...]
    expected_regex_per_column: tuple[str, ...]
    split_by: str = ","

    def assert_csv_header(self) -> bool:
        with open(self.csv_path, "r") as f:
            first_line = f.readline().strip()
            header = tuple(first_line.split(self.split_by))

        if header != self.expected_columns:
            raise ValueError(
                f"Unexpected CSV header: {header}. "
                f"Expected: {self.expected_columns}"
            )
        return True

    def assert_csv_rows(self) -> bool:
        with open(self.csv_path, "r") as f:
            for line in f.readlines()[1:]:
                values = line.strip().split(self.split_by)
                for value, regex in zip(values, self.expected_regex_per_column):
                    if not re.fullmatch(regex, value):
                        raise ValueError(
                            f"Unexpected value '{value}' in CSV row: {line.strip()}. "
                            f"Expected to match regex: {regex}"
                        )
        return True


@dataclass
class Rule:
    validator: CSVValidator
    header_error_message: str
    rows_error_message: str
    success_message: str

    def validate(self) -> bool:
        valid = False
        try:
            valid = self.validator.assert_csv_header()
        except ValueError as e:
            raise ValueError(f"{self.header_error_message} Details: {e}")
        try:
            valid = self.validator.assert_csv_rows()
        except ValueError as e:
            raise ValueError(f"{self.rows_error_message} Details: {e}")
        success_message_has_content = len(self.success_message) > 0
        if valid and success_message_has_content:
            print(self.success_message)
        return valid
