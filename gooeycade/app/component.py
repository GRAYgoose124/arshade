import arcade
import logging
import importlib.util

from pathlib import Path


log = logging.getLogger(__name__)


class Component(arcade.View):
    """Unused - documentation only."""

    def __init__(self):
        super().__init__()
        self._view_cls = None

    def get_component_spec(self):
        # get the path of the view class
        view_path = Path(self._view_cls.__module__.replace(".", "/"))

    @property
    def name(self):
        return self.__class__.__name__.replace("View", "").lower()

    @property
    def path(self):
        pass


class ComponentManager:
    def __init__(self):
        self._component_paths = {}

    def can_reload(self, view):
        """Returns whether the view can be reloaded."""
        if isinstance(view, Component):
            name = view.name
        elif isinstance(view, str):
            name = view
        else:
            raise TypeError(f"View must be a Component or a string, not {type(view)}.")

        return name in self._component_paths and self._component_paths[name] is not None

    def get_component_path(self, view):
        """Returns the path to the component."""
        if isinstance(view, Component):
            name = view.name
        elif isinstance(view, str):
            name = view
        else:
            raise TypeError(f"View must be a Component or a string, not {type(view)}.")

        return self._component_paths[name]

    def discover_component_path(self, view, component_root: Path):
        """Returns the path to the component."""
        # get it by investigating the class's module
        cpath = component_root.parents[2] / view.__module__.replace(".", "/")
        log.debug("Discovered component path: %s", cpath)
        if cpath.exists():
            return cpath
        else:
            return None

    def load_component(self, component_path: Path):
        """Loads a component from a path."""
        log.debug("Loading component from %s", component_path)
        spec = importlib.util.spec_from_file_location(
            component_path.name, component_path.parent
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.ComponentView
