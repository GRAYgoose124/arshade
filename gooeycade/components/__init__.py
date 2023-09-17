from .mandala.view import MandalaView
from .meshviz.view import MeshView
from .swarm.view import SwarmView
from .wriggler.view import WrigglerView
from .tiler.view import TilerView

from .pause import PauseView
from .primary import PrimaryView

# Do not change these unless you know what you're doing:
core = [PauseView, PrimaryView]

all = core + [
    # Add your views here:
    MandalaView,
    MeshView,
    SwarmView,
    WrigglerView,
    TilerView,
]


def __root__(path):
    """Returns the components root path."""
    global root
    import sys, pathlib

    root = pathlib.Path(path)

    # append app to path so components can import relatively - dynamically.
    # This is used
    sys.path.append(str(root.parent))


__root__(__file__)


__all__ = [str(c.__name__) for c in all]
