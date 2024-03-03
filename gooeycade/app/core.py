from pathlib import Path
import sys
import arcade
import logging
from functools import singledispatchmethod


log = logging.getLogger(__name__)

from .component import Component, ComponentManager


class GooeyApp(arcade.Window, ComponentManager):
    def __init__(self, components_root: Path):
        arcade.Window.__init__(
            self, 1280, 720, "Gooey Cade", gl_version=(4, 3), resizable=True
        )
        ComponentManager.__init__(self)

        self._views = {}
        self._default_view = None
        self._last_view = None

        self.load_components(components_root, blacklist=["MetaView"])

    @property
    def views(self):
        return self._views

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.show_view("pause")

    def start(self, default_view=None):
        if default_view is not None:
            if default_view not in self.views:
                raise ValueError(f"View '{default_view}' does not exist.")

            self._default_view = default_view
        log.info(
            "Starting Gooey Cade\nViews: %s", [v.name for v in self.views.values()]
        )
        for view in self.views.values():
            view.setup()

        self.center_window()
        self.show_view(self._default_view)

        arcade.run()

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._last_view = self._current_view or self._default_view or view

        super().show_view(self.views[view])

    def set_default_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

        self._default_view = view

    def add_view(self, view, reloadable_path=None):
        """Adds a view to the app."""
        if reloadable_path is not None:
            self.add_component_path(view, reloadable_path)

        if view.name in self._views:
            log.warning("View '%s' already exists, overwriting.", view.name)
            del self._views[view.name]
            # force GC

        self._views[view.name] = view

        if self._default_view is None:
            self._default_view = view.name

    def update_view(self, vname):
        """Updates a view."""
        self.show_view("pause")
        if self.can_reload(vname):
            p = self.get_component_path(vname)
            log.info("Reloading view '%s' from %s", vname, p)
            self.add_view(self.load_component(p)(), reloadable_path=p)
            log.info("Updated view '%s'", self.views[vname])
            self.views[vname].setup()

    def update_views(self):
        """Updates the views."""
        for view in self.views.values():
            self.update_view(view)

    def load_components(
        self, components_root: Path, whitelist=None, blacklist=None, append_to_sys=True
    ):
        found = self.find_all_cm_paths(components_root)
        
        if append_to_sys and components_root not in sys.path:
            sys.path.append(str(components_root))

        if whitelist:
            found = {name: path for name, path in found if name in whitelist}
        if blacklist:
            found = {name: path for name, path in found if name not in blacklist}

        components = []
        for p in found.values():
            c = self.load_component(p)
            self.add_view(c(), reloadable_path=p)
            components.append(c)

        return components

