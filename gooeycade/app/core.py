from pathlib import Path
import arcade
import logging
from functools import singledispatchmethod

from gooeycade.app.views import *

log = logging.getLogger(__name__)


class GooeyApp(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Gooey Cade", gl_version=(4, 3), resizable=True)

        self._views = {"primary": PrimaryView(), "pause": PauseView()}
        self._component_paths = {"primary": None, "pause": None}

        self._last_view = "primary"
        self._default_view = "primary"

    @property
    def views(self):
        return self._views

    def start(self):
        log.info(
            "Starting Gooey Cade\nViews: %s", [v.name for v in self.views.values()]
        )
        for view in self.views.values():
            view.setup()

        self.center_window()
        self.show_view(self._default_view)

        arcade.run()

    def show_view(self, view):
        # if view not in self.views:
        #     raise ValueError(f"View '{view}' does not exist.")

        # get the key of the current view
        if self._current_view is not None and type(self._current_view) in [
            type(x) for x in self._views.values()
        ]:
            key = {v: k for k, v in self._views.items()}[self._current_view]
            self._last_view = key

        super().show_view(self.views[view])

    def set_default_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._default_view = view

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_view("pause")

    def add_view(self, view, reloadable_path=None):
        """Adds a view to the app."""
        if reloadable_path is not None:
            self._component_paths[view.name] = reloadable_path

        self._views[view.name] = view

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

    def load_components(self, component_paths: list[Path]):
        """Loads components from a list of paths."""
        for p in component_paths:
            self.add_view(self.load_component(p), reloadable_path=p)

    def update_view(self, view):
        """Updates a view."""
        if self.can_reload(view):
            p = self.get_component_path(view)
            self.add_view(self.load_component(p), reloadable_path=p)
        view.setup()

    def update_views(self):
        """Updates the views."""
        for view in self.views.values():
            self.update_view(view)

    def hotload_new_components(
        self, components: list[arcade.View], component_root: Path
    ):
        """Given already loaded component modules, save the paths to them and
        reload them when needed."""
        for c in components:
            p = self.discover_component_path(c, component_root)
            print(c, p)
            self.add_view(c(), reloadable_path=p)
