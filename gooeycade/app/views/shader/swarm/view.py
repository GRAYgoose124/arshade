import arcade
import time

from .swarm import Swarm
from ..shader import ShaderView


class SwarmView(ShaderView):
    def __init__(self):
        super().__init__()

        self._swarm = Swarm(self.window)
        
        # TODO: on_show? on_hide_view?
        self.window.ctx.enable_only(self.window.ctx.BLEND)

    @property
    def swarm(self):
        return self._swarm
    
    @swarm.setter
    def swarm(self, swarm):
        self._swarm = swarm

    def on_draw(self):
        arcade.start_render()

        # Run the shader and render
        self.swarm.render()

    def __unpause(self):
        t = time.time() 
        self.swarm.start_time += abs(t - self._pause_shader)
        super().__unpause()
        