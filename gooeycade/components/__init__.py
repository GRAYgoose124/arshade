from .mandala.view import MandalaView
from .meshviz.view import MeshView
from .swarm.view import SwarmView
from .wriggler.view import WrigglerView
from .tiler.view import TilerView

from .pause import PauseView
from .primary import PrimaryView


all = [
    # Do not change these unless you know what you're doing:
    PauseView,
    PrimaryView,
    # Add your views here:
    MandalaView,
    MeshView,
    SwarmView,
    WrigglerView,
    TilerView,
]


def __root__(path):
    """Returns the root path."""
    global root
    import pathlib

    root = pathlib.Path(path)


__root__(__file__)


__all__ = [str(c.__name__) for c in all]
