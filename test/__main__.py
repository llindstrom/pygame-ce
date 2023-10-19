"""Load and run the Pygame test suite

python -c "import pygame.tests" [<test options>]

or

python test [<test options>]

Command line option --help displays a command line usage message.
"""

import sys
import argparse
import textwrap

if __name__ == "__main__":
    import os

    pkg_dir = os.path.split(os.path.abspath(__file__))[0]
    parent_dir, pkg_name = os.path.split(pkg_dir)
    is_pygame_pkg = pkg_name == "tests" and os.path.split(parent_dir)[1] == "pygame"
    if not is_pygame_pkg:
        sys.path.insert(0, parent_dir)
else:
    is_pygame_pkg = __name__.startswith("pygame.tests.")

if is_pygame_pkg:
    from pygame.tests.test_utils.run_tests import run_and_exit
    from pygame.tests.test_utils.test_runner import base_arg_parser
else:
    from test.test_utils.run_tests import run_and_exit
    from test.test_utils.test_runner import base_arg_parser

if is_pygame_pkg:
    test_pkg_name = "pygame.tests"
    prog = f"python -m {test_pkg_name}"
else:
    test_pkg_name = "test"
    prog = f"python {test_pkg_name}"


###########################################################################
# Set additional command line options
#
# Defined in test_runner.py as it shares options, added to here

arg_parser = argparse.ArgumentParser(
    prog=prog,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=f"Run all or some of the {test_pkg_name}.xxxx_test tests.",
    epilog=textwrap.dedent(
        f"""\
    [Example]

    $ {prog} -sd sprite threads

    Run the sprite and threads module tests isolated in subprocesses, dumping
    all failing tests info in the form of a dict.
    """
    ),
    parents=[base_arg_parser],
)
arg_parser.add_argument(
    "-d", "--dump", action="store_true", help="dump results as dict ready to eval"
)
arg_parser.add_argument("-F", "--file", help="dump results to a file")
arg_parser.add_argument(
    "-m",
    "--multi_thread",
    metavar="THREADS",
    type=int,
    help="run subprocessed tests in x THREADS",
)
arg_parser.add_argument(
    "-t",
    "--time_out",
    metavar="SECONDS",
    type=int,
    help="kill stalled subprocessed tests after SECONDS",
)
arg_parser.add_argument(
    "-f", "--fake", metavar="DIR", help="run fake tests in run_tests__tests/$DIR"
)
arg_parser.add_argument(
    "-p",
    "--python",
    metavar="PYTHON",
    help=f"path to python executable to run subproccesed tests\ndefault (sys.executable): {sys.executable}",
)
arg_parser.add_argument(
    "-I",
    "--interactive",
    action="store_true",
    help="include tests requiring user input",
)
arg_parser.add_argument("-S", "--seed", type=int, help="Randomisation seed")
arg_parser.add_argument("test", nargs="+", help="test name")

###########################################################################
# Set run() keyword arguments according to command line arguments.
# args will be the test module list, passed as positional arguments.

args = arg_parser.parse_args()
kwds = {}
if args.incomplete:
    kwds["incomplete"] = True
if args.usesubprocess:
    kwds["usesubprocess"] = True
else:
    kwds["usesubprocess"] = False
if args.dump:
    kwds["dump"] = True
if args.file:
    kwds["file"] = args.file
if args.exclude:
    kwds["exclude"] = args.exclude
if args.unbuffered:
    kwds["unbuffered"] = True
if args.randomize:
    kwds["randomize"] = True
if args.seed is not None:
    kwds["seed"] = args.seed
if args.multi_thread is not None:
    kwds["multi_thread"] = args.multi_thread
if args.time_out is not None:
    kwds["time_out"] = args.time_out
if args.fake:
    kwds["fake"] = args.fake
if args.python:
    kwds["python"] = args.python
if args.interactive:
    kwds["interactive"] = True
kwds["verbosity"] = args.verbosity


###########################################################################
# Run the test suite.
run_and_exit(*args.test, **kwds)
