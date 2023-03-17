from dataclasses import dataclass, field
import time
import arcade
import arcade.gl
import pyglet
from pyglet.math import Mat4

from math import cos, sin, pi
from array import array 
from pathlib import Path

from .description import ProgramDefinition, ParallelSpiralOrbit, SinCosOrbit


class MandalaView(arcade.View):
    def __init__(self):
        super().__init__()
        self.__start_time = 0
        self.__program_has_time_uniform = True
        self.__modelview_enabled = False
        self.description = None

        self.vao = None
        self.program = None

        self.setup()

    def setup(self):
        self.__start_time = time.time()
        
        descr = ParallelSpiralOrbit(render_modes=(pyglet.gl.GL_LINE_STRIP, pyglet.gl.GL_POINTS))
        self.description = descr
        self.__start_time += descr.time_offset

        self.__modelview_enabled = descr.modelview_enabled
        self.vao = self.__build_mesh(description=descr)

        default_root = Path(__file__).parent / "shaders"
        self.program = self.window.ctx.load_program(vertex_shader=default_root / descr.vert_shader, fragment_shader=default_root / "frag.glsl")
       
        try:
            self.program['point_size'] = descr.point_size
            self.program['time'] = 0.0
            self.program['model'] = Mat4()
        except KeyError:
            pass

    def on_show(self):
        #self.__old_size = self.window.get_size()
        #self.window.set_size(1420, 1420)

        arcade.set_background_color(arcade.color.BLACK)
        self.window.ctx.enable_only(self.window.ctx.PROGRAM_POINT_SIZE, pyglet.gl.GL_LINE_SMOOTH, pyglet.gl.GL_BLEND)
        self.setup()

    def on_hide_view(self):
        pass
        #self.window.set_size(*self.__old_size)

    def __build_mesh(self, description: ProgramDefinition):
        # create a vertex buffer object (VBO) containing the positions of the points

        initial_data =  description.initial_data()
        buffer = self.window.ctx.buffer(data=array('f', initial_data))

        # This will need to be rendered as points AND again as lines
        vao = self.window.ctx.geometry([arcade.gl.BufferDescription(buffer, *description.description)])
        
        return vao
    
    def on_update(self, delta_time: float):
        if self.__program_has_time_uniform:
            try:
                self.program['time'] = (time.time() - self.__start_time) * self.description.speed
            except KeyError:
                pass

        if self.__modelview_enabled:
            translate = Mat4.from_translation((0, 0, 0))
            rotate = Mat4.from_rotation(sin(self.program['time'] * self.description.speed) * 2 * pi, (0., 0., 1.)) 
            try:
                self.program["model"] = rotate @ translate
            except KeyError:
                self.__modelview_enabled = False

    # draw the points and lines
    def on_draw(self):
        arcade.start_render()

        mode = self.description.render_modes[0]
        if mode is not None:
            self.vao.render(program=self.program, mode=mode)
        
        arcade.gl.LINE_STRIP
        mode = self.description.render_modes[1]
        if mode is not None:
            self.vao.render(program=self.program, mode=mode)

 
    def on_key_press(self, key, modifiers):
        pass
