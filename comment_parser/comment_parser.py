#region IMPORTS
from comment_parser import texts
import re
from typing import List, Union
#endregion

class CommentParser:
    def __init__(self,comment_text : str):
        '''
        Parses a Reddit comment to extract awards. Automatically replaces the main text and small text with texts from a file.
        '''

        self.edits = self.extract_edits(comment_text)

        # imports constants
        self.main_text = texts.MAIN_TEXT
        self.small_text = texts.SMALL_TEXT
        self.award_pattern = texts.AWARD_PATTERN

    def add_edit(self,text : str):
        '''
        Adds an edit with passed text.
        '''

        self.edits.append(text)

    @property
    def last_edit_num(self) -> Union[None, int]:
        '''
        Returns the last edit number.
        '''

        return None if self.edits == [] else len(self.edits)

    @property
    def awards(self) -> List[str]:
        '''
        Returns awards mentioned in the edits.
        '''

        awards = []

        for edit_txt in self.edits:
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
        # check if edits exist so that no extra newlines are added
        edits = "\n\n" + "\n\n".join(
            f'edit{"" if num==0 else num+1}. {text}'
            for num, text in enumerate(self.edits)) if self.edits else ""
        middle = edits + "\n\n"

        full_txt = f"{self.main_text}{middle}{self.small_text}"

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

        edits = []
        if last_edit is not None:
            # get edits
            for line in lines[first_edit:last_edit+1]:
                # ignore empty lines
                if line:
                    edit_txt = re.search(r"edit\d*\. (.*)",line).group(1)

                    edits.append(edit_txt)
    
        return edits
