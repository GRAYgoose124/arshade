""" Currently based on https://api.arcade.academy/en/latest/tutorials/gpu_particle_burst/index.html"""
import math
import arcade
import arcade.gl

from pathlib import Path

from array import array
from dataclasses import dataclass
import random
import time


MIN_FADE_TIME = 0.25
MAX_FADE_TIME = 1.5
PARTICLE_COUNT = 3000


@dataclass
class Burst:
    """ Track for each burst. """
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float


class ShaderView(arcade.View):
    def __init__(self):
        super().__init__()
        self.burst_list = []

        # Load shader
        shader_root = Path(__file__).parent.parent.parent.parent / "shaders" / "basic"
        self.program = self.window.ctx.load_program(
            vertex_shader= shader_root / "vert.glsl",
            fragment_shader= shader_root / "frag.glsl",
        )
        self.window.ctx.enable_only(self.window.ctx.BLEND)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        self.window.ctx.point_size = 2 * self.window.get_pixel_ratio()
        for burst in self.burst_list:
            # Update uniforms
            self.program['time'] = time.time() - burst.start_time
            # Render
            burst.vao.render(self.program, mode=self.window.ctx.POINTS)

    def on_update(self, dt):
        """ Update game """
        temp_list = self.burst_list.copy()

        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
               self.burst_list.remove(burst)
               
    def on_key_press(self, key, modifiers):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ User clicks mouse """

        def _gen_initial_data(initial_x, initial_y):
            """ Generate data for each particle """
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                speed = abs(random.gauss(0, 1)) * .5
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed

                red = random.uniform(0.5, 1.0)
                green = random.uniform(0, red)
                blue = 0

                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)

                yield initial_x
                yield initial_y

                yield dx
                yield dy

                yield red
                yield green
                yield blue

                yield fade_rate


        # Recalculate the coordinates from pixels to the OpenGL system with
        # 0, 0 at the center.
        x2 = x / self.window.width * 2. - 1.
        y2 = y / self.window.height * 2. - 1.

        # Get initial particle data
        initial_data = _gen_initial_data(x2, y2)

        # Create a buffer with that data
        buffer = self.window.ctx.buffer(data=array('f', initial_data))

        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f f',
                                                         ['in_pos',
                                                          'in_vel',
                                                          'in_color',
                                                          'in_fade_rate'])
        # Create our Vertex Attribute Object
        vao = self.window.ctx.geometry([buffer_description])

        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)