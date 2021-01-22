import re

#region REPLY TEXT
MAIN_TEXT = """1. Create a bot to reply to "what are some beginner projects" questions on r/learnpython, using [PRAW](https://praw.readthedocs.io/en/latest/index.html).

Other than that, [here's](https://github.com/karan/Projects) a list of programming projects on Github. [Here's](https://web.archive.org/web/20180612183650if_/https://github.com/jorgegonzalez/beginner-projects) another archived list. Also check out [this resource](https://www.reddit.com/r/learnpython/wiki/index#wiki_tools_for_learning_python) in the subreddit wiki. Good luck!"""

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

#region REPLY TO JUDGMENT TEXTS
REPLY_TO_PRAISE_TEXT = """Praise for the food is praise for the cook.

Thanks from the programmer."""

REPLY_TO_CRITICISM_TEXT = """:(

I'm open to criticism, please message me and tell me what you don't like about me.
"""
#endregion

#region REPLY TO COMPETITION TEXT
REPLY_TO_COMPETITION_TEXT = """Great minds think alike!"""
#endregion

#region HUMAN COMMENT TEXT
HUMAN_COMMENT_TEXT = "beep boop I'm a human"
#endregion

#region REGEX PATTERNS
AWARD_TEXT = "Thank you for the (.*), kind stranger!"
AWARD_PATTERN = re.compile(AWARD_TEXT)

_title_text = r"""
    ^
    # ignore words
    (?!
    .*troubleshooting
    |
    \d # listicles like 10 beginner projects
    )

    .*

    (
    (
    (begg?inn?ers?(/?\w+)?|educational|simple|starter)\  # "beginner/intermediate"
    (\w*\ )?
    projects?
    (?!.*done) # ignore "my beginner project is done"
    )
    |
    (
    simple\ 
    programs?\ 
    ideas?
    )
    |
    (
    (projects?|programs?)\ 
    (ideas?\ )?
    (to\ do\ )?
    for\ 
    (a\ )?
    (complete\ )?
    (begg?inn?ers?|begg?inn?ing)
    )
    |
    (
    what\ 
    projects?\ 
    (can|for)\ 
    (a\ )?
    begg?inn?ers?
    )
    )
"""
TITLE_PATTERN = re.compile(_title_text,re.I|re.X)

_praise_text = "good bot[.!]?"
PRAISE_PATTERN = re.compile(_praise_text,re.I)

_criticism_text = "bad bot[.!]?"
CRITICISM_PATTERN = re.compile(_criticism_text,re.I)
#endregion
