import re

MAIN_TEXT = """1\\. Create a bot to reply to "what are some beginner projects" questions on r/learnpython, using [PRAW](https://praw.readthedocs.io/en/latest/index.html).

Other than that, here are some beginner project ideas:

* [a list of programming projects on Github](https://github.com/karan/Projects)
* [another list from Github](https://github.com/jorgegonzalez/beginner-projects)
* [a curated list of Python projects for beginners, intermediate & advance level programmers](https://www.theinsaneapp.com/2021/06/list-of-python-projects-with-source-code-and-tutorials.html)
* [Tech with Tim Youtube channel, full of Python projects](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lkJOu1AWab-nFtjDw7aPek)
* [resources in the subreddit wiki](https://www.reddit.com/r/learnpython/wiki/index#wiki_tools_for_learning_python)

Good luck!"""

SMALL_TEXT = """^(Downvote me if the post wasn't a question about examples of beginner projects. Thank you.)"""

UPVOTES_TEXTS = {
    "5": "thanks for 5 upvotes!",
    "10": "omg 10 upvotes!!!! Thank you!!",
    "50": "50 upvotes??? 😲😲😲 Can we make it to 100?",
    "100": "100 UPVOTES?????? I CAN DIE NOW",
}

REPLY_TO_PRAISE_TEXT = """Praise for the food is praise for the cook.

Thanks from the programmer."""

REPLY_TO_CRITICISM_TEXT = """:(

I'm open to criticism, please message me and tell me what you don't like about me."""

REPLY_TO_COMPETITION_TEXT = """Great minds think alike!"""

HUMAN_COMMENT_TEXT = "beep boop I'm a human"

AWARD_TEXT = "Thank you for the (.*), kind stranger!"
AWARD_PATTERN = re.compile(AWARD_TEXT)

_title_text = r"""
    ^
    # ignore words
    (?!
    .*choos(ing)?\ tools?\ for
    |
    .*troubleshooting
    |
    .*critique
    |
    .*help
    |
    .*struggling
    |
    .*feedback
    |
    .*hire
    |
    .*which\ library
    |
    .*having\ trouble
    |
    .*came\ across
    |
    .*(for\ )?my
    |
    \d # listicles like 10 beginner projects
    |
    top
    |
    blackjack
    |
    how # ignore questions like "how hard..."
    |
    is # ignore questions like "is it a good beginner project?"
    |
    .*error
    )

    .*
    (?<!as\ a\ )
    (
    (
    (begg?inn?ers?(/?\w+)?|educational|simple|starter|easy)\  # "beginner/intermediate"
    (\w*\ )?
    projects?
    (?!:) # ignore "Beginner project: <project>"
    (?!.*done) # ignore "my beginner project is done"
    (?!.*working.*on)
    )
    |
    (
    simple\ 
    programs?\ 
    ideas?
    )
    |
    (
    (projects?)\ 
    (ideas?\ )?
    (to\ do\ )?
    for\ 
    (just\ )?
    (a\ )?
    (complete\ )?
    (begg?inn?ers?|begg?inn?ing|starting)
    )
    |
    (
    what\ 
    projects?\ 
    (can|for)\ 
    (a\ )?
    begg?inn?ers?
    )
    |
    projects?\ 
    (ideas?\ )?
    to\ (learn|practi(c|s)e)
    )
"""
TITLE_PATTERN = re.compile(_title_text, re.I | re.X)

_praise_text = "good bot[.!]?"
PRAISE_PATTERN = re.compile(_praise_text, re.I)

_criticism_text = "bad bot[.!]?"
CRITICISM_PATTERN = re.compile(_criticism_text, re.I)
