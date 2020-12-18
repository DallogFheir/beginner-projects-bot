from pathlib import Path
import sys
import unittest

# add top-level folder to path
path = Path(__file__).parent.parent.parent
sys.path.append(str(path))

from tests import TestCommentParser, TestTexts

unittest.main()
