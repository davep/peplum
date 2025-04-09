from argparse import Namespace

from peplum.app import Peplum

app = Peplum(Namespace(theme="textual-mono", pep=None, sort_by="~created"))
if __name__ == "__main__":
    app.run()
