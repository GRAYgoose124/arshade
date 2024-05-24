from pathlib import Path
import arcade
import time
import logging

from gooeycade.app.component import ShaderViewComponent

from .fluid import Fluid
from .utils import get_shader_variants

log = logging.getLogger(__name__)


class FluidView(ShaderViewComponent):
    def __init__(self):
        super().__init__()

        self._program = Fluid(self.window)

        # TODO: on_show? on_hide_view?
        self.window.ctx.enable_only(self.window.ctx.BLEND)

        self.shaders = list(get_shader_variants())
        self.current_shader = 0

    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, program):
        self._program = program

    def on_draw(self):
        arcade.start_render()

        # Run the shader and render
        self.program.render()

    def __unpause(self):
        t = time.time()
        self.program.start_time += abs(t - self._pause_shader)
        super().__unpause()

    def on_update(self, delta_time):
        self.program.on_update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self._pause_shader = time.time()
            super().__pause()
        elif key == arcade.key.TAB:
            self.current_shader = (self.current_shader + 1) % len(self.shaders)
            self.program.setup(Path("variants") / self.shaders[self.current_shader])
            log.info(f"Switched to shader {self.shaders[self.current_shader]}")
        else:
            super().on_key_press(key, modifiers)


ComponentView = FluidView
