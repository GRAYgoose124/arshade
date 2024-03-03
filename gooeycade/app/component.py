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

    def setup(self):
        """Called when the component is initialized."""
        pass

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

    def add_component_path(self, view, path):
        """Adds a component path."""
        if isinstance(view, Component):
            name = view.name
        elif isinstance(view, str):
            name = view
        else:
            raise TypeError(f"View must be a Component or a string, not {type(view)}.")

        self._component_paths[name] = path

    @staticmethod
    def discover_component_path(view, component_root: Path):
        """Returns the path to the component."""
        # get it by investigating the class's module
        cpath = component_root.parents[2] / view.__module__.replace(".", "/")
        cpath = cpath.with_suffix(".py")
        log.debug("Discovered component path: %s", cpath)
        if cpath.exists():
            return cpath
        else:
            log.warning(
                "Could not find actual component at discovered component path for %s",
                view,
            )
            return None

    @staticmethod
    def load_component(component_path: Path):
        """Loads a component from a path."""
        log.debug(
            "Loading %s component from %s", component_path.parent.stem, component_path
        )

        spec = importlib.util.spec_from_file_location(
            f"{component_path.parent.stem}.{component_path.stem}",
            component_path,
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.ComponentView
    
    @staticmethod
    def find_all_cm_paths(components_root: Path):
        """Finds all component modules.
        
        A component module must contain a class that inherits a Component.
        
        it must also alias that view class to ComponentView in the same module."""
        for path in components_root.rglob("*.py"):
            if path.stem == "__init__":
                continue
            
            with path.open("r") as f:
                found_view_class = False
                found_name = None
                for line in f:
                    if "class" in line and "View(" in line:
                        found_view_class = True
                        found_name = line.split("class")[1].split("(")[0].strip()
                    if "ComponentView" in line and "=" in line and found_view_class:
                        name = line.split("=")[1].strip()
                        assert name == found_name, f"Name mismatch: {name} != {found_name}"
                        yield name, path
                        break