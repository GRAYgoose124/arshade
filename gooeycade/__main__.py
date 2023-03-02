import arcade

from .app.core import GooeyApp


def main():
    app = GooeyApp()
    arcade.run()


if __name__ == "__main__":
    main()