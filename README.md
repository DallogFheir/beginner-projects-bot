# beginner-projects-bot

r/learnpython bot for beginner project resources.

- checks new submissions in the r/learnpython subreddit and replies to those asking for some beginner projects
- edits the comment to thank for upvotes and/or awards
- deletes the comment if downvoted

## Changelog

- 3.5.0
  - added logging through Pushbullet
- 3.4.0
  - added replying to competition
- 3.3.0
  - added a proper method to stop the bot
  - added a block to catch ServerError
- 3.2.3
  - prevented bot from editing comments starting with "beep boop I'm a human"
- 3.2.2
  - added more unit tests
- 3.2.1
  - fixed wrong edit numbers
- 3.2.0
  - bot now responds to "bad bot" comments too
  - fixed dead link
  - fixed edit numbers starting at 1
- 3.1.0
  - added logging
  - added unit testing for Regex patterns
  - added support for command line arguments
- 3.0.1
  - fixed text constants and extra newline
  - removed unecessary prints
- 3.0.0
  - remodeled the structure of the package
  - bot now responds to "good bot" replies to its comments
- 2.1.0
  - changed bot to use stream provided by PRAW
- 2.0.0
  - recreated the bot with a more OOP approach
- 1.1.2
  - fixed Regex pattern so that the bot doesn't react to "help with a simple program" and similar
- 1.1.1
  - moved "please downvote me" text to the end of the comment
- 1.1.0
  - bot now asks Redditors to downvote its comment if it replied to a wrong submission, and deletes the comment if downvoted to -1
  - bot now sleeps after exceeding the Reddit rate limit
- 1.0.0
  - bot replies to submissions about beginner projects in Python with links to lists of such projects
  - bot edits its comments after receiving a certain number of upvotes, or receiving awards
