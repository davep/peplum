"""Main entry point for the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from inspect import cleandoc
from typing import get_args as get_literal_values

##############################################################################
# Local imports.
from . import __doc__, __version__
from .app import Peplum
from .app.data import SortOrder


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The arguments.
    """

    # Build the parser.
    parser = ArgumentParser(
        prog="peplum",
        description=__doc__,
        epilog=f"v{__version__}",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s v{__version__}",
    )

    # Add --license
    parser.add_argument(
        "--license",
        "--licence",
        help="Show license information",
        action="store_true",
    )

    # Add --sort
    parser.add_argument(
        "-s",
        "--sort-by",
        help="Set the sort order for the PEPs; prefix with '~' for reverse order",
        choices=(
            *get_literal_values(SortOrder),
            *(f"~{order}" for order in get_literal_values(SortOrder)),
        ),
    )

    # Add --theme
    parser.add_argument(
        "-t",
        "--theme",
        help="Set the theme for the application (set to ? to list available themes)",
    )

    # The remainder is going to be the initial command.
    parser.add_argument(
        "pep",
        help="A PEP to highlight",
        nargs="?",
    )

    # Finally, parse the command line.
    return parser.parse_args()


##############################################################################
def show_themes() -> None:
    """Show the available themes."""
    for theme in sorted(Peplum(Namespace(theme=None)).available_themes):
        if theme != "textual-ansi":
            print(theme)


##############################################################################
def main() -> None:
    """Main entry point."""
    args = get_args()
    if args.license:
        print(cleandoc(Peplum.HELP_LICENSE))
    elif args.theme == "?":
        show_themes()
    else:
        Peplum(args).run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
