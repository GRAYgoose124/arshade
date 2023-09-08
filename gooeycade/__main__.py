import arcade
import logging

from gooeycade.app.core import GooeyApp
from gooeycade.components import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("arcade").setLevel(logging.INFO)

    app = GooeyApp()

    app.add_views(
        {
            "mesh": MeshView(),
            "swarm": SwarmView(),
            "mandala": MandalaView(),
            "wriggler": WrigglerView(),
        }
    )
    app.start()


if __name__ == "__main__":
    main()
