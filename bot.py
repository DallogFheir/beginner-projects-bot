from bpb import BPB
from utils.argparser import parser
import re

#region get version from README.md
regex = re.compile(r"""## Changelog

- (\d+\.\d+\.\d+)""")

with open("README.md") as f:
    version = re.search(regex,f.read()).group(1)
#endregion

USER_AGENT = f"script:beginner-projects-bot:v{version} (by /u/DallogFheir)"

args = parser.parse_args()

bot = BPB(USER_AGENT,**vars(args))
bot.start()
