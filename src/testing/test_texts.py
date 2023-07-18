import inspect
from pathlib import Path
import unittest
from ..comment_parser import texts


class TestTexts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # loads test patterns from test_data
        text_dict = {}

        for file in (Path(__file__).parent / "test_data").iterdir():
            with open(file, encoding="utf-8") as f:
                text_dict[file.stem] = [line.strip() for line in f.readlines()]

        cls.text_dict = text_dict

    def _test_data(self, mode="to_match"):
        assertion = self.assertIsNotNone if mode == "to_match" else self.assertIsNone

        # get caller function name without test_, and corresponding data
        func_name = inspect.stack()[1][3].replace("test_", "")
        data = self.text_dict[func_name]
        # get globals from texts module
        # replace mode if exists
        # turn to upper for constants
        regex = vars(texts)[func_name.replace(f"_{mode}", "").upper()]

        for datum in data:
            assertion(regex.search(datum), msg=datum)

    # TEST CASES
    def test_title_pattern_to_match(self):
        self._test_data()

    def test_title_pattern_to_not_match(self):
        self._test_data(mode="to_not_match")

    def test_award_pattern(self):
        self._test_data()

    def test_praise_pattern(self):
        self._test_data()

    def test_criticism_pattern(self):
        self._test_data()
