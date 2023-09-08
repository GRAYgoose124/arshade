import arcade
import logging

from gooeycade.app.views import *

log = logging.getLogger(__name__)


class GooeyApp(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Gooey Cade", gl_version=(4, 3), resizable=True)

        self._views = {"primary": PrimaryView()}
        self._views["pause"] = PauseView()

        self._last_view = "primary"
        self._default_view = "primary"

    @property
    def views(self):
        return self._views

    def start(self):
        log.info("Starting Gooey Cade\nViews: %s", self.views.values())
        for view in self.views.values():
            view.setup()

        self.center_window()
        self.show_view(self._default_view)

        arcade.run()

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")

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

    def add_views(self, view_dict):
        self._views.update(view_dict)
