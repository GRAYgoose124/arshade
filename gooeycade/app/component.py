import arcade
import time
from pathlib import Path


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
        return self.__class__.__name__

    @property
    def title(self):
        return self.name.replace("View", "").lower()

    @property
    def path(self):
        pass


class ShaderViewComponent(Component):
    def __init__(self):
        super().__init__()
        self._hidden_pause = False
        self._pause_shader = False

    def __unpause(self):
        self._pause_shader = False
        self._hidden_pause = False

    def on_show(self):
        if self._hidden_pause:
            self.__unpause()

        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        if not self._pause_shader:
            self._hidden_pause = True
            self._pause_shader = time.time()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self._pause_shader:
                self.__unpause()
            else:
                self._pause_shader = time.time()
