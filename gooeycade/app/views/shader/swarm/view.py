import arcade
import time

from .swarm import Swarm
from ..shader import ShaderView


class SwarmView(ShaderView):
    def __init__(self):
        super().__init__()

        self._swarm = Swarm.build(self.window)
        self._swarm.program["t0"] = 0
        self._swarm.program["t1"] = 1
        # Create textures and FBOs
        wh = self.window.width, self.window.height
        self.tex_0 = self.window.ctx.texture(wh)
        self.fbo_0 = self.window.ctx.framebuffer(color_attachments=[self.tex_0])

        self.tex_1 = self.window.ctx.texture(wh)
        self.fbo_1 = self.window.ctx.framebuffer(color_attachments=[self.tex_1])
        
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

        # Fill the textures with solid colours
        self.fbo_0.clear(color=(0.0, 0.0, 1.0, 1.0), normalized=True)
        self.fbo_1.clear(color=(1.0, 0.0, 0.0, 1.0), normalized=True)

        # Bind our textures to channels
        self.tex_0.use(0)
        self.tex_1.use(1)

        # Run the shader and render
        self.swarm.render()

    def __unpause(self):
        t = time.time() 
        self.swarm.start_time += abs(t - self._pause_shader)
        super().__unpause()
        