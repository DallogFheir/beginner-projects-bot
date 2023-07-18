from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    "-d",
    "--debug",
    action="store_const",
    const=True,
    default=False,
    help="launch in debug mode (without actually replying/editing)",
)

parser.add_argument(
    "-l",
    "--limit",
    type=int,
    default=None,
    help="set how many comments/submissions are checked",
)

parser.add_argument(
    "-log",
    "--logging-level",
    type=str,
    default="INFO",
    choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    help="set logging level",
)
