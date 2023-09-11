from .mandala.view import MandalaView
from .meshviz.view import MeshView
from .swarm.view import SwarmView
from .wriggler.view import WrigglerView


all = [MandalaView, MeshView, SwarmView, WrigglerView]


def __root__(path):
    """Returns the root path."""
    global root
    import pathlib

    root = pathlib.Path(path)


__root__(__file__)


__all__ = [str(c.__name__) for c in all]
