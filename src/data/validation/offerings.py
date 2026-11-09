import re
from pathlib import Path

import pandas as pd

from data.validation.validation import ANYTHING_IN_ROW, CSVValidator, Rule

DATA_DIR = Path(__file__).parent.parent
OFFERINGS_CSV_PATH = DATA_DIR / "offerings.csv"
EXPECTED_OFFERINGS_COLUMNS = ("Infernal Offering", "Bane", "Boon", "ID")
INFERNAL_OFFERING_REGEX = re.compile(r"^The [A-Z][a-z]+ (of )?[A-Z][a-z]+$")


class OfferingsValidator(CSVValidator):
    def __init__(self):
        super().__init__(
            csv_path=OFFERINGS_CSV_PATH,
            expected_columns=EXPECTED_OFFERINGS_COLUMNS,
            expected_regex_per_column=(
                INFERNAL_OFFERING_REGEX.pattern,
                ANYTHING_IN_ROW,
                ANYTHING_IN_ROW,
                ANYTHING_IN_ROW,
            ),
        )


class OfferingsRule(Rule):
    def __init__(self):
        super().__init__(
            validator=OfferingsValidator(),
            header_error_message="Unexpected offerings.csv header.",
            rows_error_message="Unexpected offerings.csv row values.",
            success_message=f"{OFFERINGS_CSV_PATH.name} validation passed successfully.",
        )


if __name__ == "__main__":
    OfferingsRule().validate()
