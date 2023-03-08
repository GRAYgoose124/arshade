import arcade
import time
from pyglet.math import Mat4
from arcade.experimental.texture_render_target import RenderTargetTexture

from pathlib import Path

from .mesh import MeshBuilder
from ..shader import ShaderView


class MeshView(ShaderView):
    def __init__(self):
        super().__init__()

        self.time = 0
        self._mesh = MeshBuilder(self.window).geometry_from_file("meshes/cube.obj", resize=0.5)
        shader_root = Path(__file__).parent / "shaders"
        self.mesh_view_program = self.window.ctx.load_program(
            vertex_shader   = shader_root / "vert.glsl",
            #geometry_shader = shader_root / "geom.glsl",
            fragment_shader = shader_root / "frag.glsl",
        )

        self.mesh_view_program["projection"] = Mat4.perspective_projection(self.window.aspect_ratio, 1.0, 10.0, 70)

        # TODO: on_show? on_hide_view? Issue: On Windows, it doesn't appear the arcade window has a depth buffer.
        self.window.ctx.enable_only(self.window.ctx.BLEND, self.window.ctx.DEPTH_TEST)

        # Lets render to an FBO with a depth attachment instead
        self.render_fbo = self.window.ctx.framebuffer(
            color_attachments=[self.window.ctx.texture((self.window.width, self.window.height), components=4)],
            depth_attachment=self.window.ctx.depth_texture((self.window.width, self.window.height))
        )

    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def on_draw(self):
        arcade.start_render()

        translate = Mat4.from_translation((0, 0, -2))
        rotate = Mat4.from_rotation(self.time / 2, (1, .5, 0))
        self.mesh_view_program["model"] = rotate @ translate

        # Run the shader and render
        with self.render_fbo:
            self.render_fbo.clear()
            self.mesh.render(self.mesh_view_program, mode=self.window.ctx.TRIANGLES)

        # Render the FBO to the screen
        self.window.ctx.copy_framebuffer(self.render_fbo, self.window.ctx.screen)

    def __unpause(self):
        self.mesh.start_time += abs(self.time - self._pause_shader)
        super().__unpause()
    
    def on_update(self, delta_time):
        self.time += delta_time

    def on_show(self):
        self.window.ctx.enable_only(self.window.ctx.BLEND, self.window.ctx.DEPTH_TEST)

        return super().on_show()
        