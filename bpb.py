#region IMPORTS
from comment_parser import CommentParser, texts
import concurrent.futures
from utils.logger import LOGGER_CONFIG
import logging
import logging.config
import os
import praw
import prawcore
import re
import time
import traceback
from typing import Union
#endregion

class BPB:
    url = "https://www.reddit.com"

    def __init__(self,user_agent:str,debug:bool=False,limit:Union[int,None]=None,logging_level:str="INFO"):
        '''
        A Reddit bot to respond to submissions on r/learnpython asking for beginner projects.

        Arguments:
        * user_agent
        * [optional] debug - for testing without actually editing/replying
        * [optional] limit - how many comments/submissions are checked
        '''

        # logging
        # get Pushbullet API key from env vars
        # if not found, from pushbullet file
        pb_api_key = os.environ.get("PB_API_KEY")
        if pb_api_key is None:
            with open("pushbullet") as f:
                pb_api_key = f.read()
        LOGGER_CONFIG.set_api_key(pb_api_key)

        logging.config.dictConfig(LOGGER_CONFIG)
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging_level)

        # reads config from env vars
        # if not found, from praw.ini
        self.reddit = praw.Reddit(user_agent=user_agent)

        self.sub = self.reddit.subreddit("learnpython")
        self.bot = self.reddit.redditor("BeginnerProjectsBot")
        self.logger.info(f"Initialized bot with debug={debug}, limit={limit}, logging level={logging_level}.")

        # import constants
        self.award_text = texts.AWARD_TEXT
        self.reply_to_praise_text = texts.REPLY_TO_PRAISE_TEXT
        self.reply_to_criticism_text = texts.REPLY_TO_CRITICISM_TEXT
        self.praise_pattern = texts.PRAISE_PATTERN
        self.criticism_pattern = texts.CRITICISM_PATTERN
        self.title_pattern = texts.TITLE_PATTERN
        self.upvotes_ranges = texts.UPVOTES_TEXTS
        self.reply_text = texts.MAIN_TEXT + "\n\n" + texts.SMALL_TEXT
        self.human_comment_text = texts.HUMAN_COMMENT_TEXT
        self.reply_to_competition_text = texts.REPLY_TO_COMPETITION_TEXT

        # config
        self.debug = debug
        self.debug_str = "(DEBUG MODE) " if debug else ""
        self.limit = limit

    # MAIN METHODS
    def start(self):
        '''
        Starts the bot's functionality in 2 threads.
        '''
        self.running = True

        with concurrent.futures.ThreadPoolExecutor() as e:
            submission_traverser = e.submit(self.traverse_new_submissions)
            self.logger.info("Initialized submission traverser thread.")

            comment_traverser = e.submit(self.traverse_own_comments)
            self.logger.info("Initialized comment traverser thread.")

            self.threads = [submission_traverser, comment_traverser]

            for thread in concurrent.futures.as_completed(self.threads):
                try:
                    thread_name = "comment traverser" if thread==comment_traverser else "submission traverser"
                    thread.result()
                except (prawcore.exceptions.ServerError, prawcore.exceptions.ResponseException):
                    self.logger.warning(f"ServerError happened in {thread_name}. Restarting...")
                    self.stop()
                    time.sleep(300)
                    self.start()
                except:
                    self.logger.critical(f"Unexpected exception happened in {thread_name}. {traceback.format_exc()}")
                    self.stop()
    
    def stop(self):
        self.running = False

        while any(thread.running() for thread in self.threads):
            pass

        self.logger.info("Stopped.")
    
    def traverse_new_submissions(self):
        '''
        Traverses new submissions in r/learnpython and replies to them.
        '''

        count = 0
        # pause_after to yield None and not stop the for loop
        for post in self.sub.stream.submissions(pause_after=1):
            # check if should still run
            if not self.running:
                break

            if post is None:
                continue

            count += 1
            limit_str = ""

            if self.limit is not None:
                limit_str = f" Submission count: {count}."

                if count > self.limit:
                    self.logger.debug("Stopped submission traverser thread.")
                    return
            
            self.logger.debug(f"Checking a new post: {self.url + post.permalink}.{limit_str}")

            # ignore if already upvoted (to make sure bot doesn't comment on the same post again)
            if self.check_title(post.title) and not post.likes:
                # for log
                cur_reply = post

                if not self.debug:
                    cur_reply = post.reply(self.reply_text)
                    post.upvote()

                self.logger.info(f"{self.debug_str}Replied to submission: {self.url + cur_reply.permalink}")
    
        self.logger.info("Correctly terminated submission traverser.")

    def traverse_own_comments(self):
        '''
        Traverses the bot's comments and edits or deletes them, and replies to "good bot" replies.
        '''
        
        count = 0
        while self.running:
            self.logger.debug(f"Started comment traverser loop.")

            for comment in self.bot.comments.new(limit=None):
                limit_str = ""
                count += 1
                if self.limit is not None:
                    limit_str = f" Comment count: {count}."

                    if count > self.limit:
                        self.logger.debug("Stopped comment traverser thread.")
                        return

                self.logger.debug(f"Checking a comment: {self.url + comment.permalink}.{limit_str}")

                # check if comment should be deleted
                if self.delete_downvoted_comment(comment):
                    continue
                
                # check if other bot replied
                self.reply_to_other_bot(comment.submission)

                # ignore reply to judgment/reply to other bot comments
                if comment.body not in (self.reply_to_praise_text, self.reply_to_criticism_text, self.reply_to_competition_text) and not comment.body.startswith(self.human_comment_text):
                    self.edit_comment(comment)
                
                self.reply_to_judgment(comment)

                # check if should still run
                if not self.running:
                    break

        self.logger.info("Correctly terminated comment traverser.")

    # COMMENT MANIPULATION METHODS
    def delete_downvoted_comment(self, comment : praw.models.Comment) -> bool:
        '''
        Deletes comment with score less than 0.
        '''

        if comment.score < 0:
            if not self.debug:
                comment.delete()
            
            self.logger.info(f"{self.debug_str}Deleted comment: {self.url+comment.permalink}.")

            # return for condition in traverse_own_comments
            return True

        return False
    
    def edit_comment(self, comment : praw.models.Comment):
        '''
        Edits comment if new comment text is different than old comment text.
        '''
        new_text = self.create_new_text(comment)
        if new_text != comment.body:
            if not self.debug:
                comment.edit(new_text)

            self.logger.info(f"{self.debug_str}Edited comment: {self.url + comment.permalink}.")
    
    def reply_to_judgment(self, comment : praw.models.Comment):
        '''
        Replies to "good bot"/"bad bot" comments in replies to the bot's comments.
        '''

        # needs to refresh to get replies
        comment.refresh()

        for reply in comment.replies:
            # ignore already upvoted replies
            if not reply.likes:
                if re.match(self.praise_pattern,reply.body):
                    # for log
                    cur_reply = reply

                    if not self.debug:
                        cur_reply = reply.reply(self.reply_to_praise_text)
                        reply.upvote()

                    self.logger.info(f"{self.debug_str}Replied to praise: {self.url + cur_reply.permalink}.")
                elif re.match(self.criticism_pattern,reply.body):
                    # for log
                    cur_reply = reply

                    if not self.debug:
                        cur_reply = reply.reply(self.reply_to_criticism_text)
                        reply.upvote()

                    self.logger.info(f"{self.debug_str}Replied to criticism: {self.url + cur_reply.permalink}.")
    
    def reply_to_other_bot(self, submission : praw.models.Submission):
        for comment in submission.comments:
            if comment.author=="BeginnerProjectBot" and not comment.likes:
                # for log
                cur_comment = comment

                if not self.debug:
                    cur_comment = comment.reply(self.reply_to_competition_text)
                    comment.upvote()

                self.logger.info(f"{self.debug_str}Replied to competition: {self.url + cur_comment.permalink}")
    
    # helpers
    def create_new_text(self,comment : praw.models.Comment) -> str:
        '''
        Creates new comment text based on the number of upvotes and received awards.
        '''

        parsed_comment = CommentParser(comment.body)
        
        # adds edits for upvotes
        for score, text in self.upvotes_ranges.items():
            if comment.score >= int(score) and text not in parsed_comment.edits:
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
