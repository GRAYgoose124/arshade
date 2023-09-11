import arcade
import logging

from gooeycade.app.core import GooeyApp


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("arcade").setLevel(logging.INFO)

    app = GooeyApp()

    from gooeycade import components

    app.hotload_new_components(components.all, components.root)

    app.start()


if __name__ == "__main__":
    main()
