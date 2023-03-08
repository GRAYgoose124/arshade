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

        self._time = 0

        self._mesh = MeshBuilder(self.window).geometry_from_file("meshes/torus.obj", resize=0.5)

        self.program = self.__load_mesh_shader()
        # TODO: on_show? on_hide_view? Issue: On Windows, it doesn't appear the arcade window has a depth buffer.

        # Lets render to an FBO with a depth attachment instead
        self.render_fbo = self.__build_render_fbo()

    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def __load_mesh_shader(self, vert=None, frag=None, geom=None, shader_root=None):
        default_root = Path(__file__).parent / "shaders"
        if shader_root is None:
            shader_root = default_root

        if vert is not None:
            vs = shader_root / vert
        else:
            vs = default_root / "vert.glsl"

        if frag is not None:
            fs = shader_root / frag
        else:
            fs = default_root / "frag.glsl"

        if geom is not None:
            gs = shader_root / geom
        else:
            gs = None

        program = self.window.ctx.load_program(
            vertex_shader   = vs,
            geometry_shader = gs,
            fragment_shader = fs,
        )

        program["projection"] = Mat4.perspective_projection(self.window.aspect_ratio, 1.0, 10.0, 70)
        return program

    def __build_render_fbo(self):
        return self.window.ctx.framebuffer(
            color_attachments=[self.window.ctx.texture((self.window.width, self.window.height), components=4)],
            depth_attachment=self.window.ctx.depth_texture((self.window.width, self.window.height))
        )

    def __draw_mesh(self):
        translate = Mat4.from_translation((0, 0, -2))
        rotate = Mat4.from_rotation(self._time / 2, (1, .5, 0))
        self.program["model"] = rotate @ translate

        with self.render_fbo:
            self.render_fbo.clear()
            self.mesh.render(self.program, mode=self.window.ctx.TRIANGLES)

        self.window.ctx.copy_framebuffer(self.render_fbo, self.window.ctx.screen)

    def on_draw(self):
        arcade.start_render()

        self.__draw_mesh()
    
    def on_update(self, delta_time):
        self._time += delta_time

    def on_show(self):
        self.window.ctx.enable_only(self.window.ctx.BLEND, self.window.ctx.DEPTH_TEST)

        return super().on_show()
    
    def on_resize(self, width: int, height: int):
        # rebuild the FBO with the new size
        self.render_fbo = self.__build_render_fbo()