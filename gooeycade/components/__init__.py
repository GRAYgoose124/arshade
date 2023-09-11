from .mandala.view import MandalaView
from .meshviz.view import MeshView
from .swarm.view import SwarmView
from .wriggler.view import WrigglerView
from .pause import PauseView
from .primary import PrimaryView

#### Start of Component Interface ####
# Provides a standard interface for hotloading app components.
#
# app = GooeyApp(components: {all: list[Component], root: str})
#
#
all = [
    MandalaView,
    MeshView,
    SwarmView,
    WrigglerView,
    PauseView,
    PrimaryView,
]
root = None
#### End of Component Interface ####


def __root__(path):
    """Sets the root path w/o importing pathlib to namespace."""
    global root
    import pathlib

    root = pathlib.Path(path)


__root__(__file__)


__all__ = [str(c.__name__) for c in all]
