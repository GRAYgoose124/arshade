import arcade
import logging

from .app.core import GooeyApp


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("arcade").setLevel(logging.INFO)
    
    app = GooeyApp()
    arcade.run()


if __name__ == "__main__":
    main()