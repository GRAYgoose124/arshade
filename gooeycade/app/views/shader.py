""" Thanks to https://github.com/pvcraven/n-body for the example. """
import arcade
import arcade.gl
import time


class ShaderView(arcade.View):
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
