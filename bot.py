from bpb import BPB
from utils.argparser import parser

USER_AGENT = "script:beginner-projects-bot:v3.0.1 (by /u/DallogFheir)"

args = parser.parse_args()

bot = BPB(USER_AGENT,**vars(args))
bot.start()
