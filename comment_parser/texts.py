import re

#region REPLY TEXT
MAIN_TEXT = """1. Create a bot to reply to "what are some beginner projects" questions on r/learnpython, using [PRAW](https://praw.readthedocs.io/en/latest/index.html).

Other than that, [here's](https://www.reddit.com/r/learnpython/wiki/index#wiki_tools_for_learning_python) a list of lists of beginner projects in the subreddit wiki. [Here's](https://github.com/jorgegonzalez/beginner-projects) another list on Github. Good luck!"""

SMALL_TEXT = """^(Downvote me if the post wasn't a question about examples of beginner projects. Thank you.)"""
#endregion

#region UPVOTES TEXTS
UPVOTES_TEXTS = {
  "5": "thanks for 5 upvotes!",
  "10": "omg 10 upvotes!!!! Thank you!!",
  "50": "50 upvotes??? 😲😲😲 Can we make it to 100?",
  "100": "100 UPVOTES?????? I CAN DIE NOW"
}
#endregion

#region REPLY TO PRAISE TEXT
REPLY_TO_PRAISE_TEXT = """Praise for the food is praise for the cook.

Thanks from the programmer."""
#endregion

#region REGEX PATTERNS
AWARD_TEXT = "Thank you for the (.*), kind stranger!"
AWARD_PATTERN = re.compile(AWARD_TEXT)

_title_text = r"""(
    (\bsimple\ program(s)?\ idea(s)?\b)
) |
(
    (\bbeg(g)?i(n)?ner(s)?\b|\bsimple\b)
    \ 
    (\w*\ )?
    (\bproject(s)?\b)
    (?!.*done)
) |
(
    (\bproject(s)?\b|\bprogram(s)?\b)
    \ for\ 
    (\bbeg(g)?i(n)?ner(s)?\b|\bbegi(n)?ning\b)
)"""
TITLE_PATTERN = re.compile(_title_text,re.I|re.X)

_praise_text = "good bot[.!]?"
PRAISE_PATTERN = re.compile(_praise_text,re.I)
#endregion
