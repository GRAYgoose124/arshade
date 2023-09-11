from pathlib import Path
import arcade
import logging
from functools import singledispatchmethod


log = logging.getLogger(__name__)

from .component import Component, ComponentManager


class GooeyApp(arcade.Window, ComponentManager):
    def __init__(self, components=None):
        arcade.Window.__init__(
            self, 1280, 720, "Gooey Cade", gl_version=(4, 3), resizable=True
        )

        ComponentManager.__init__(self)

        self._views = {}
        self._default_view = None

        if components is not None:
            self.hotload_new_components(components.all, components.root)

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
        self.show_view(self._default_view or "primary")

        arcade.run()

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._last_view = self._current_view

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

        if self._default_view is None:
            self._default_view = view.name

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
            self.add_view(c(), reloadable_path=p)
