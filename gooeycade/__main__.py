import arcade
import logging

from gooeycade.app.core import GooeyApp
from gooeycade import components


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("arcade").setLevel(logging.INFO)

    app = GooeyApp(components)

    app.start(default_view="primary")


if __name__ == "__main__":
    main()
