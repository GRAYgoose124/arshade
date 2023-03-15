import time
import arcade
import arcade.gl

from math import cos, sin
from array import array 
from pathlib import Path


class MandalaView(arcade.View):
    def __init__(self):
        super().__init__()
        self.__start_time = time.time()

        self.vao = self.__build_mandala_mesh()

        default_root = Path(__file__).parent / "shaders"
        self.program = self.window.ctx.load_program(vertex_shader=default_root / "vert.glsl", fragment_shader=default_root / "frag.glsl")
        self.program['time'] = 0.0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def __build_mandala_mesh(self):
        # create a vertex buffer object (VBO) containing the positions of the points
        def _gen_initial_data(N=10000):
            for i in range(N):
                angle = (i / N) * 2.0 * 3.14159
                radius = 0.5 + (i / N) * 0.5
                x = radius * cos(angle)
                y = radius * sin(angle)
                r = (cos(angle * 3.0) + 1.0) / 2.0
                g = (cos(angle * 5.0) + 1.0) / 2.0
                b = (cos(angle * 7.0) + 1.0) / 2.0

                yield x
                yield y

                yield r 
                yield g
                yield b

        initial_data =  _gen_initial_data()
        buffer = self.window.ctx.buffer(data=array('f', initial_data))

        # This will need to be rendered as points AND again as lines
        vao = self.window.ctx.geometry([arcade.gl.BufferDescription(buffer, "2f 3f", ["in_pos", "in_col"])])
        
        return vao
    
    def on_update(self, delta_time: float):
       self.program['time'] = time.time() - self.__start_time

    # draw the points and lines
    def on_draw(self):
        arcade.start_render()
        
        self.vao.render(program=self.program, mode=arcade.gl.LINE_STRIP)
        self.vao.render(program=self.program, mode=arcade.gl.TRIANGLE_FAN)

 
    def on_key_press(self, key, modifiers):
        pass
