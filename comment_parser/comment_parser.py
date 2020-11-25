#region IMPORTS
from comment_parser.texts import AWARD_PATTERN, MAIN_TEXT, SMALL_TEXT
import re
from typing import Union
#endregion

class CommentParser:
    def __init__(self,comment_text : str):
        '''
        Parses a Reddit comment to extract awards. Automatically replaces the main text and small text with texts from a file.
        '''

        self.edits = self.extract_edits(comment_text)

        # imports constants
        self.main_text = MAIN_TEXT
        self.small_text = SMALL_TEXT
        self.award_pattern = AWARD_PATTERN

    def add_edit(self,text : str):
        '''
        Adds an edit with passed text.
        '''

        next_edit_num = self.last_edit_num + 1 if self.last_edit_num is not None else 0

        self.edits[next_edit_num] = text

    @property
    def last_edit_num(self) -> Union[None, int]:
        '''
        Returns the last edit number.
        '''

        return None if self.edits == {} else list(self.edits.keys())[-1]

    @property
    def edit_txts(self) -> list:
        '''
        Returns the texts of edits.
        '''

        return self.edits.values()

    @property
    def awards(self) -> list[str]:
        '''
        Returns awards mentioned in the edits.
        '''

        awards = []

        for edit_txt in self.edit_txts:
            match = re.search(self.award_pattern, edit_txt)

            if match is not None:
                awards.append(match.group(1))

        return awards

    @property
    def body(self) -> str:
        '''
        Returns the full text body of the comment.
        '''

        # edit0. should be edit.
        edits = "\n\n" + "\n\n".join(
            f'edit{"" if num==0 else num}. {text}'
            for num, text in self.edits.items()) + "\n\n"

        full_txt = f"{self.main_text}{edits}{self.small_text}"

        return full_txt

    @staticmethod
    def extract_edits(text : str) -> str:
        '''
        Extracts edits from the comment body.
        '''

        lines = text.split("\n")

        # gets indices from first "edit" to last one
        first_edit = None
        last_edit = None
        for index, line in enumerate(lines):
            if line.startswith("edit"):
                if first_edit is None:
                    first_edit = index

                last_edit = index
            # gets the ending small text index
            elif line.startswith("^"):
                small_txt_index = index

        edits = {}
        if last_edit is not None:
            # splits edits into number : text dict
            # { None : "thanks", 1 : "thanks2"} etc.
            for line in lines[first_edit:last_edit+1]:
                # ignore empty lines
                if line:
                    edit_num, edit_txt = re.search(r"edit(\d)*\. (.*)",line).groups()

                    # replaces None with 0 for getting next edit number easily
                    edits[int(edit_num) if edit_num is not None else 0] = edit_txt
    
        return edits
