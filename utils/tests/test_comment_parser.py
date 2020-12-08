import inspect
import unittest
from comment_parser import CommentParser
from comment_parser import texts

class TestCommentParser(unittest.TestCase):
    @staticmethod
    def replace_body(replacement):
        comment_body = f"{texts.MAIN_TEXT}\n<REPLACE>\n{texts.SMALL_TEXT}"

        return comment_body.replace("<REPLACE>",replacement)

    @classmethod
    def setUpClass(cls):
        def replace_award(award):
            return texts.AWARD_TEXT.replace("(.*)",award)

        # create example comments
        cls.comments = [
            {
                "replace_text" : "",
                "body" : cls.replace_body(""),
                "edits" : [],
                "last_edit_num" : None,
                "awards" : []
            },
            {
                "replace_text" : "\nedit. thanks\n",
                "body" : cls.replace_body("\nedit. thanks\n"),
                "edits" : ["thanks"],
                "last_edit_num" : 1,
                "awards" : []
            },
            {
                "replace_text" : f"\nedit. thank you\n\nedit2. {replace_award('Nothing')}\n",
                "body" : cls.replace_body(f"\nedit. thank you\n\nedit2. {replace_award('Nothing')}\n"),
                "edits" : ["thank you", replace_award('Nothing')],
                "last_edit_num" : 2,
                "awards" : ["Nothing"]
            },
            {
                "replace_text" : f"\nedit. arigatō\n\nedit2. {replace_award('Upvote')}\n\nedit3. спасибо\n\nedit4. {replace_award('Warm Words')}\n\nedit5. blahblah\n",
                "body" : cls.replace_body(f"\nedit. arigatō\n\nedit2. {replace_award('Upvote')}\n\nedit3. спасибо\n\nedit4. {replace_award('Warm Words')}\n\nedit5. blahblah\n"),
                "edits" : ["arigatō", replace_award('Upvote'), "спасибо", replace_award('Warm Words'), "blahblah"],
                "last_edit_num" : 5,
                "awards" : ["Upvote", "Warm Words"]
            }
        ]

        cls.parsers = [CommentParser(comment["body"]) for comment in cls.comments]

    def _test_data(self):
        # get caller function name without test_
        func_name = inspect.stack()[1][3].replace("test_","")

        for i, tup in enumerate(zip(self.comments, self.parsers)):
            comment, parser = tup

            self.assertEqual(comment[func_name],
            getattr(parser,func_name),
            msg=f"Test number {i}.")

    # TEST CASES
    def test_edits(self):
        self._test_data()

    def test_last_edit_num(self):
        self._test_data()

    def test_awards(self):
        self._test_data()

    def test_body(self):
        self._test_data()

    def test_add_edit(self):
        for i, tup in enumerate(zip(self.comments,self.parsers)):
            comment, parser = tup

            parser_copy = CommentParser(parser.body)
            last_edit_num = parser.last_edit_num or 0

            parser_copy.add_edit("thanksss so much")
            self.assertEqual(
                [*comment["edits"], "thanksss so much"],parser_copy.edits,
                msg=f"Test number {i}. 'thanksss so much'")
            self.assertEqual(
                self.replace_body(
                    f"{comment['replace_text']}\nedit{'' if last_edit_num==0 else last_edit_num+1}. thanksss so much\n"),
                parser_copy.body,
                msg=f"Test number {i}. 'thanksss so much'")

            parser_copy.add_edit("thanks again")
            self.assertEqual(
                [*comment["edits"], "thanksss so much", "thanks again"],
                parser_copy.edits,
                msg=f"Test number {i}. 'thanks again'")
            self.assertEqual(
                self.replace_body(
                    f"{comment['replace_text']}\nedit{'' if last_edit_num==0 else last_edit_num+1}. thanksss so much\n\nedit{last_edit_num+2}. thanks again\n"),
                parser_copy.body,
                msg=f"Test number {i}. 'thanks again'")
    
    def test_extract_edits(self):
        for i, comment in enumerate(self.comments):
            self.assertEqual(comment["edits"],CommentParser.extract_edits(comment["body"]),
            msg=f"Test number {i}.")