import inspect
from pathlib import Path
import unittest
import texts

class TestTexts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text_dict = {}

        for file in Path("test_data").iterdir():
            with open(file,encoding="utf-8") as f:
                text_dict[file.stem] = [line.strip() for line in f.readlines()]

        cls.text_dict = text_dict

    def _get_data(self):
        # get _test_data's caller's name, removes "test_"
        func_name = inspect.stack()[2][3].replace("test_","")
        data = self.text_dict[func_name]

        return data, func_name

    def _test_data(self,mode="to_match"):
        assertion = self.assertIsNotNone if mode=="to_match" else self.assertIsNone

        data, func_name = self._get_data()
        # get globals from texts module
        # replace mode if exists
        # turn to upper for constants
        regex = vars(texts)[func_name.replace(f"_{mode}","").upper()]
        
        for datum in data:
            assertion(regex.search(datum),msg=datum)

    # TEST CASES
    def test_title_pattern_to_match(self):
        self._test_data()

    def test_title_pattern_to_not_match(self):
        self._test_data(mode="to_not_match")

    def test_award_pattern(self):
        self._test_data()

    def test_praise_pattern(self):
        self._test_data()

if __name__=="__main__":
    unittest.main()
