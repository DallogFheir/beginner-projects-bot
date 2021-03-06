from bpb import BPB
from utils.argparser import parser
import re

# region CONFIG
version_pattern = re.compile(r"## Changelog\n\n- (\d+\.\d+\.\d+)")
with open("README.md") as f:
    version = re.search(version_pattern, f.read())[1]
USER_AGENT = f"script:beginner-projects-bot:v{version} (by /u/DallogFheir)"

args = parser.parse_args()
# endregion

# region KEYBOARD LISTENER
try:
    from pynput import keyboard

    def on_release(key):
        if key.char == "s":
            bot.stop()

            # return to stop listener
            return False

    keyboard.Listener(on_release=on_release).start()
except ImportError:
    pass
# endregion

bot = BPB(USER_AGENT, **vars(args))
bot.start()
