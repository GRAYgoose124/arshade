import arcade
from pathlib import Path


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
        return self._component_paths[view.name] is not None

    def get_component_path(self, view):
        """Returns the path to the component."""
        return self._component_paths[view.name]

    def discover_component_path(self, view, component_root: Path):
        """Returns the path to the component."""
        # get it by investigating the class's module
        return component_root.parents[2] / view.__module__.replace(".", "/")

    def load_component(self, component_path: Path):
        """Loads a component from a path."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            component_path.name, component_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.ComponentView
