# Assure this package is top level (not a subpackage of the test(s) package)
assert __name__ == "test_utils"

import sys
from pathlib import Path

my_dir = Path(__file__).resolve().parent
sys.path.append(str(my_dir))

from pygame_test_utils_extras import *
