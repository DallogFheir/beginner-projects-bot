from bpb import BPB
from utils.argparser import parser
from pathlib import Path
import os
import re


def main():
    version_pattern = re.compile(r"## Changelog\n\n- (\d+\.\d+\.\d+)")
    with open(Path(__file__).parent.parent / "README.md") as f:
        version = re.search(version_pattern, f.read())[1]
    USER_AGENT = f"script:beginner-projects-bot:v{version} (by /u/DallogFheir)"

    args = parser.parse_args()

    bot = BPB(USER_AGENT, **vars(args))
    bot.start()


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
