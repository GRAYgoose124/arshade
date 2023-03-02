import arcade

from gooeycade.app.views.pause import PauseView
from gooeycade.app.views.primary import PrimaryView


class Application(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Gooey Cade")
        self._views = {
            "primary": PrimaryView(),
            "pause": PauseView(),
        }
        self._last_view = None

        self.show_view("primary")

    @property
    def views(self):
        return self._views

    def show_view(self, view):
        if view not in self.views:
            raise ValueError(f"View '{view}' does not exist.")
        
        # get the key of the current view
        if self._current_view is not None:
            key = {v: k for k, v in self._views.items()}[self._current_view]
            self._last_view = key

        super().show_view(self.views[view])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self._current_view == "pause":
                self.show_view(self._last_view)
            else:
                self.show_view("pause")