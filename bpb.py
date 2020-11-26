from comment_parser import CommentParser
from comment_parser.texts import AWARD_TEXT, PRAISE_PATTERN, REPLY_TO_PRAISE_TEXT, TITLE_PATTERN, UPVOTES_TEXTS
from concurrent.futures import ThreadPoolExecutor
import praw
import re
import time

class BPB:    
    def __init__(self):
        '''
        A Reddit bot to respond to submissions on r/learnpython asking for beginner projects.
        '''

        # reads config from env vars
        # if not found, from praw.ini
        self.reddit = praw.Reddit()

        self.sub = self.reddit.subreddit("learnpython")
        self.bot = self.reddit.redditor("BeginnerProjectsBot")

        # import constants
        self.award_text = AWARD_TEXT
        self.reply_to_praise_text = REPLY_TO_PRAISE_TEXT
        self.praise_pattern = PRAISE_PATTERN
        self.title_pattern = TITLE_PATTERN
        self.upvotes_ranges = UPVOTES_TEXTS

    # MAIN METHODS
    def start(self,limit=None):
        '''
        Starts the bot's functionality in 2 threads.
        '''

        with ThreadPoolExecutor() as e:
            self.submission_traverser = e.submit(self.traverse_new_submissions,limit)
            self.comment_traverser = e.submit(self.traverse_own_comments,limit)
            e.submit(self.check_status)
    def traverse_new_submissions(self,limit=None):
        '''
        Traverses new submissions in r/learnpython and replies to them.

        Takes an optional 'limit' paramter for debugging.
        '''

        # count for debugging if 'limit' is used
        count = 0
        
        for post in self.sub.stream.submissions():
            # ignore if already upvoted (to make sure bot doesn't comment on the same post again)
            if self.check_title(post.title) and not post.likes:
                post.upvote()
                cur_reply = post.reply(self.reply_text)

                # log
                print(f"Replied: https://www.reddit.com{cur_reply.permalink}")

            if limit is not None:
                if count >= limit:
                    break

                count += 1
    def traverse_own_comments(self,limit=None):
        '''
        Traverses the bot's comments and edits or deletes them, and replies to "good bot" replies.

        Takes an optional 'limit' parameter to debug.
        '''

        # count for debugging if 'limit' is used
        count = 0
        running = True

        while running:
            for comment in self.bot.comments.new(limit=None):
                if self.delete_downvoted_comment(comment):
                    continue
                # ignore reply to praise comments
                if comment.body != self.reply_to_praise_text:
                    self.edit_comment(comment)
                self.reply_to_praise(comment)

                if limit is not None:
                    if count >= limit:
                        running = False
                        break

                    count += 1

    # MAINTENANCE METHODS
    def check_status(self):
        while True:
            if self.comment_traverser.running():
                print("Checking comments working...")
            else:
                print("Checking comments broke!")

            if self.submission_traverser.running():
                print("Checking submissions working...")
            else:
                print("Checking submissions broke!")

            time.sleep(3600*24)

    # COMMENT MANIPULATION METHODS
    def delete_downvoted_comment(self, comment : praw.models.Comment) -> bool:
        '''
        Deletes comment with score less than 0.
        '''

        if comment.score < 0:
            comment.delete()
            
            # log
            print(f"Deleted: https://www.reddit.com{comment.permalink}")

            # return for condition in traverse_own_comments
            return True

        return False
    def edit_comment(self, comment : praw.models.Comment):
        '''
        Edits comment if new comment text is different than old comment text.
        '''
        new_text = self.create_new_text(comment)
        if new_text != comment.body:
            comment.edit(new_text)

            # log
            print(f"Edited: https://www.reddit.com{comment.permalink}")
    # helper
    def create_new_text(self,comment : praw.models.Comment) -> str:
        '''
        Creates new comment text based on the number of upvotes and received awards.
        '''

        parsed_comment = CommentParser(comment.body)
        
        # adds edits for upvotes
        for score, text in self.upvotes_ranges.items():
            if comment.score >= int(score) and text not in parsed_comment.edit_txts:
                parsed_comment.add_edit(text)

        # adds edits for awards
        for award in comment.all_awardings:
            name = award["name"]
            if name not in parsed_comment.awards:
                text = self.award_text.replace("(.*)",name)
                parsed_comment.add_edit(text)

        return parsed_comment.body

    def check_title(self,title : str) -> bool:
        '''
        Checks if the title of a post matches the title Regex pattern.
        '''

        # checks if title matches regex
        match = re.search(self.title_pattern,title)

        return False if match is None else True

    def reply_to_praise(self, comment : praw.models.Comment):
        '''
        Replies to "good bot" comments in replies to the bot's comments.
        '''

        # needs to refresh to get replies
        comment.refresh()

        for reply in comment.replies:
            # ignore already upvoted replies
            if re.match(self.praise_pattern,reply.body) and not reply.likes:
                cur_reply = reply.reply(self.reply_to_praise_text)
                reply.upvote()

                # log
                print(f"Replied to praise: https://www.reddit.com{cur_reply.permalink}")
