from dataclasses import dataclass, field
import time
import arcade
import arcade.gl
import pyglet
from pyglet.math import Mat4, Vec3

from math import cos, sin, pi
from array import array 
from pathlib import Path

from ..shader import ShaderView

from .descriptions import ProgramDefinition, ParallelSpiralOrbit, SinCosOrbit


class MandalaView(ShaderView):
    def __init__(self):
        super().__init__()
        self.__start_time = 0
        self.__program_has_time_uniform = True
        self.__modelview_enabled = False
        self.__modelview_orthogonal = True
        self.description = None

        self.vao = None
        self.program = None

        self.setup()

    def setup(self):
        self.__start_time = time.time()
        
        # TODO: This should be configurable, but initial_data isn't properly set when rebuilt from json (because it's tied to the subclass :X)
        # descr = ProgramDefinition.from_json(Path(__file__).parent / "configs" / "parallel.json")
        descr = ParallelSpiralOrbit()

        self.description = descr
        self.__start_time += descr.time_offset

        self.__modelview_enabled = descr.modelview_enabled
        self.vao = self.__build_mesh(description=descr)

        default_root = Path(__file__).parent / "shaders"
        self.program = self.window.ctx.load_program(vertex_shader=default_root / descr.vert_shader, 
                                                    fragment_shader=default_root / "frag.glsl")
       
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
        self.window.ctx.enable_only(self.window.ctx.PROGRAM_POINT_SIZE)
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
            theta = sin(self.program['time'] * self.description.rotation_speed * (1/self.description.speed)) * 2 * pi
            model = Mat4.from_rotation(theta*cos(self.program['time']), Vec3(-.1, 1., .5)).translate(Vec3(0, 0.2* theta, 0))#.scale(Vec3(2, 2, 2))
            view = Mat4().look_at(Vec3(0, 0, -3), Vec3(0, 0, 0), Vec3(1, 1, 1))

            if self.__modelview_orthogonal:
                projection = Mat4().orthogonal_projection(-2.5, 2.5, -2.5, 2.5, -5, 5)
            else:
                projection = Mat4().perspective_projection(45, -5, 5, 100)

            try:
                model = model @ view @ projection 
                
                self.program["model"] = model
            except KeyError:
                self.__modelview_enabled = False

    # draw the points and lines
    def on_draw(self):
        arcade.start_render()

        mode = self.description.render_modes[0]
        if mode is not None:
            self.vao.render(program=self.program, mode=mode)
        
        mode = self.description.render_modes[1]
        if mode is not None:
            self.vao.render(program=self.program, mode=mode)

 
    def on_key_press(self, key, modifiers):
        pass
