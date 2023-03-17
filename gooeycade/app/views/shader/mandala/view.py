import time
import arcade
import arcade.gl
import pyglet
from pyglet.math import Mat4

from math import cos, sin, pi
from array import array 
from pathlib import Path

sin_cos_orbit_description = "3f 3f", ["in_pos", "in_col"]
def sin_cos_orbit_initial_data(N=10000):
    """ Think a deconstructed spiral along the X/Y plane """
    for i in range(N):
        angle = (i / N) * 2.0 * 3.14159
        radius = 0.5 + (i / N) * 0.5
        x = radius * cos(angle)
        y = radius * sin(angle)
        z = 1.+ 1. / (i+1)
        r = (cos(angle * 3.0) + 1.0) / 2.0
        g = (cos(angle * 5.0) + 1.0) / 2.0
        b = (cos(angle * 7.0) + 1.0) / 2.0

        yield x
        yield y
        yield z

        yield r 
        yield g
        yield b

parallel_spiral_orbit_description = "f 3f 3f", ["in_id", "in_pos", "in_col"]
def parallel_spiral_orbit_initial_data(N=10000):
    """ This generates a set of points along a radius of a circle which are then rotated at different rates. """
    for i in range(N):
        # all points start at the same angle - 0.0
        angle = 0.0
        # each point is offset along the radius tiny gap between each point
        radius = (i / N)
        
        x = radius * cos(angle)
        y = radius * cos(angle)
        z = 0.0

        r = cos(i)
        g = sin(i)
        b = cos(i) * sin(i)

        yield i

        yield x
        yield y
        yield z

        yield r
        yield g
        yield b

class MandalaView(arcade.View):
    def __init__(self):
        super().__init__()
        self.__start_time = 0
        self.__program_has_time_uniform = True
        self.__modelview_enabled = False

        self.vao = None
        self.program = None

        self.setup()

    def setup(self):
        self.__start_time = time.time()

        self.vao = self.__build_mesh(_gen_initial_data=parallel_spiral_orbit_initial_data)

        default_root = Path(__file__).parent / "shaders"
        self.program = self.window.ctx.load_program(vertex_shader=default_root / "vert.glsl", fragment_shader=default_root / "frag.glsl")
       
        try:
            self.program['time'] = 0.0
            self.program['model'] = Mat4()
        except KeyError:
            pass

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.ctx.enable_only(self.window.ctx.PROGRAM_POINT_SIZE, self.window.ctx.DEPTH_TEST)
        self.setup()

    def on_hide_view(self):
        pass

    def __build_mesh(self, _gen_initial_data=sin_cos_orbit_initial_data):
        # create a vertex buffer object (VBO) containing the positions of the points

        initial_data =  _gen_initial_data()
        buffer = self.window.ctx.buffer(data=array('f', initial_data))

        # This will need to be rendered as points AND again as lines
        vao = self.window.ctx.geometry([arcade.gl.BufferDescription(buffer, *parallel_spiral_orbit_description)])
        
        return vao
    
    def on_update(self, delta_time: float):
        if self.__program_has_time_uniform:
            try:
                self.program['time'] = (time.time() - self.__start_time) * 0.1
            except KeyError:
                pass

        if self.__modelview_enabled:
            translate = Mat4.from_translation((0, 0, 0))
            rotate = Mat4.from_rotation(sin(self.program['time'] * 0.25) * 2 * pi, (0., 0., 1.)) 
            try:
                self.program["model"] = rotate @ translate
            except KeyError:
                self.__modelview_enabled = False

    # draw the points and lines
    def on_draw(self):
        arcade.start_render()

        self.vao.render(program=self.program, mode=arcade.gl.TRIANGLES)
        self.vao.render(program=self.program, mode=arcade.gl.LINE_STRIP)
        self.vao.render(program=self.program, mode=arcade.gl.POINTS)

 
    def on_key_press(self, key, modifiers):
        pass
