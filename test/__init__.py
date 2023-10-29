"""Pygame unit test suite package

Exports function run()

To run an installed pygame package's test suite run the command line command:

python -m pygame.tests [<test options>]

Command line option --help displays a usage message.

The xxxx_test submodules of the tests package are unit test suites for
individual parts of Pygame. Each can also be run as a main program. This is
useful if the test is interactive.

For Pygame development the test suite can be run from a Pygame distribution
root directory by with the command line:

python -m test [<test options]

"""
import sys
from pathlib import Path

my_dir = str(Path(__file__).resolve().parent)
if my_dir not in sys.path:
    sys.path.insert(0, my_dir)
is_pygame_pkg = __name__ = "pygame.tests"
import test_utils
from run_tests import run
