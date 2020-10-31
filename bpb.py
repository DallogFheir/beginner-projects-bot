import praw
import re

class Beginner_Projects_Bot:
    #region REPLY TEXTS
    reply_txt = "1. Create a bot to reply to \"what are some beginner projects\" questions on this subreddit, using [PRAW](https://praw.readthedocs.io/en/latest/index.html).\n\nOther than that, [here's](https://www.reddit.com/r/learnpython/wiki/index#wiki_tools_for_learning_python) a list of lists of beginner projects in the subreddit wiki. [Here's](https://github.com/jorgegonzalez/beginner-projects) another list on Github. Good luck!"
    small_txt = "\n\n^(Downvote me if the post wasn't a question about examples of beginner projects. Thank you.)"

    edit_txt = "\n\nedit"

    ranges_lst = [5, 10, 50, 100]
    upvotes_txt_lst = [
        "thanks for 5 upvotes!",
        "omg 10 upvotes!!!! Thank you!!",
        "50 upvotes??? 😲😲😲 Can we make it to 100?",
        "100 UPVOTES?????? I CAN DIE NOW"
    ]

    award_txt_start = "Thank you for the"
    award_txt_end = ", kind stranger!"
    #endregion
    #region REGEX PATTERN
    title_pattern = re.compile(r"""
    (
        (\bsimple\ program(s)?\ idea(s)?\b)
    ) |
    (
        (\bbeg(g)?i(n)?ner(s)?\b|\bsimple\b)
        \ 
        (\w*\ )?
        (\bproject(s)?\b)
    ) |
    (
        (\bproject(s)?\b|\bprogram(s)?\b)
        \ for\  
        (\bbeg(g)?i(n)?ner(s)?\b|\bbegi(n)?ning\b)
    )
    """,re.I|re.VERBOSE)
    #endregion
    
    def __init__(self,client_id,client_secret,user_agent,username,password):
        self.reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent,
                        username=username,
                        password=password)
        self.sub = self.reddit.subreddit("learnpython")
        self.bot = self.reddit.redditor("BeginnerProjectsBot")

    def comment(self):
        for post in self.sub.new(limit=None):
            if re.search(self.title_pattern,post.title):
                # if already upvoted, ignore
                if not post.likes:
                    cur_reply = post.reply(self.reply_txt+self.small_txt)
                    post.upvote()

                    # log
                    print("Replied: https://www.reddit.com"+cur_reply.permalink)

    def edit_comments(self):
        for comment in self.bot.comments.new(limit=None):
            # DELETES COMMENT IF DOWNVOTED
            if comment.score < 0:
                comment.delete()

                # log
                print("Deleted: https://www.reddit.com" + comment.permalink)

                continue

            # EDITS COMMENT IF UPVOTES AWARDS/GIVEN
            edited_body = comment.body

            # removes small_txt from comment body (added at end)
            edited_body = edited_body.replace(self.small_txt,"")

            # gets last edit number from comment
            edit_re = re.findall(r"edit(\d*).",comment.body)

            if not edit_re:
                # if no match, start at 1
                edit_count = 1
            elif len(edit_re)==1:
                # if one match = empty string, start at 2
                edit_count = 2
            else:
                # otherwise, start at number from comment + 1
                edit_count = int(edit_re[-1]) + 1

            # add thanks for upvotes, if not already in the comment
            for i, r in enumerate(self.ranges_lst):
                # checks if score is greater than given range and respective text is not in comment
                if comment.score >= r and self.upvotes_txt_lst[i] not in comment.body:
                    # checks if edit_count is 1, then makes it empty string
                    edit_count_str="" if edit_count==1 else str(edit_count)

                    edited_body += f"{self.edit_txt}{edit_count_str}. {self.upvotes_txt_lst[i]}"

                    edit_count+=1

            # ADD THANKS FOR AWARDS
            already_thanked = re.findall("Thank you for the (.*)?, kind stranger!",comment.body)

            for award in comment.all_awardings:
                if award["name"] not in already_thanked:
                    # checks if edit_count is 1, then makes it empty string
                    edit_count_str="" if edit_count==1 else str(edit_count)

                    edited_body += f'{self.edit_txt}{edit_count_str}. {self.award_txt_start} {award["name"]}{self.award_txt_end}'

                    edit_count+=1

            # adds small_txt back
            edited_body += self.small_txt

            # edits comment
            if edited_body!=comment.body:
                comment.edit(edited_body)

                # log
                print("Edited: https://www.reddit.com" + comment.permalink)
