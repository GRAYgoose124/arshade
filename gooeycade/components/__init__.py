from .mandala.view import MandalaView
from .meshviz.view import MeshView
from .swarm.view import SwarmView
from .wriggler.view import WrigglerView
from .pause import PauseView
from .primary import PrimaryView


all = [
    MandalaView,
    MeshView,
    SwarmView,
    WrigglerView,
    PauseView,
    PrimaryView,
]


def __root__(path):
    """Returns the root path."""
    global root
    import pathlib

    root = pathlib.Path(path)


__root__(__file__)


__all__ = [str(c.__name__) for c in all]
