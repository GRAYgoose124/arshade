import logging
from pathlib import Path

from gooeycade.app.core import GooeyApp


log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("arcade").setLevel(logging.INFO)

    app = GooeyApp(1280, 720, "Gooey Cade", gl_version=(4, 3), resizable=True)

    app.start(components_path=Path(__file__).parent / "components")


if __name__ == "__main__":
    main()
