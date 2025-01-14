"""Main entry point for the application."""

##############################################################################
# Local imports.
from .app import Peplum


##############################################################################
def main() -> None:
    """Main entry point."""
    Peplum().run()


##############################################################################
if __name__ == "__main__":
    main()

### __main__.py ends here
