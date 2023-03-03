import arcade
import math
from pathlib import Path

from array import array
from dataclasses import dataclass, field
import random
import time


@dataclass
class AgentShader:
    """ Agent shader """
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry


@dataclass
class Swarm:
    """ Swarm of particles """
    AGENT_COUNT: int = field(default=1000, init=False)
    program: arcade.gl.Program = field(default=None, init=False)

    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    quad_fs: arcade.gl.Geometry = field(default=None, init=False)
    start_time: float = field(default=time.time(), init=False)

    @staticmethod
    def _gen_initial_data(initial_x, initial_y):
        """ Generate data for each particle """
        # get triangle strip data
        for strip in range(0, Swarm.AGENT_COUNT):
            angle = random.uniform(0, 2 * math.pi)
            speed = abs(random.gauss(0, 1)) * .5
            dx = math.sin(angle) * speed
            dy = math.cos(angle) * speed

            red = random.uniform(0.5, 1.0)
            green = random.uniform(0, red)
            blue = random.uniform(0, green)

            yield initial_x
            yield initial_y

            yield dx - dx*0.1
            yield dy - dy*0.1

            yield red
            yield green
            yield blue

    @staticmethod
    def build(window: arcade.Window):
        # Center of screen
        x2 = window.width // 2
        y2 = window.height // 2

        # Get initial particle data
        initial_data = Swarm._gen_initial_data(500, 500)


        buffer = window.ctx.buffer(data=array('f', initial_data))
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f',
                                                         ['in_pos',
                                                          'in_vel',
                                                          'in_color'])
        vao = window.ctx.geometry([buffer_description])

        swarm = Swarm(buffer=buffer, vao=vao)
        swarm.quad_fs = arcade.gl.geometry.quad_2d_fs()

        shader_root = Path(__file__).parent.parent.parent.parent.parent / "shaders" / "swarm"
        swarm.program = window.ctx.load_program(
            vertex_shader= shader_root / "vert.glsl",
            fragment_shader= shader_root / "frag.glsl",
        )

        return swarm
    
    def render(self):
        self.quad_fs.render(self.program)