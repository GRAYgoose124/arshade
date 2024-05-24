from collections import namedtuple
import arcade
import math
from pathlib import Path

from array import array
from dataclasses import dataclass, field
import random
import time

from .utils import get_shader_root


@dataclass
class AgentShader:
    """Agent shader"""

    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry


@dataclass
class Fluid:
    """Swarm of particles"""

    AGENT_COUNT: int = field(default=5000, init=False)

    window: arcade.Window

    program: arcade.gl.Program = field(default=None, init=False)
    compute_shader: arcade.gl.Program = field(default=None, init=False)
    group_size: namedtuple = field(
        default=namedtuple("ComputeGroup", ["x", "y", "z"])(x=256, y=1, z=1), init=False
    )

    # TODO: Use framebuffer instead of manual flipping.
    ssbo1: arcade.gl.Buffer = field(default=None, init=False)
    ssbo2: arcade.gl.Buffer = field(default=None, init=False)
    vao1: arcade.gl.Geometry = field(default=None, init=False)
    vao2: arcade.gl.Geometry = field(default=None, init=False)

    start_time: float = field(default=time.time(), init=False)

    def __post_init__(self):
        self.setup()

    def setup(self, selected_shader=None):
        initial_data = self._gen_initial_data(500, 500)

        self.ssbo1 = self.window.ctx.buffer(data=array("f", initial_data))
        self.ssbo2 = self.window.ctx.buffer(reserve=self.ssbo1.size)

        buffer_format = "4f 4x4 4f"
        attributes = ["in_vertex", "in_color"]
        self.vao1 = self.window.ctx.geometry(
            [arcade.gl.BufferDescription(self.ssbo1, buffer_format, attributes)],
            mode=self.window.ctx.TRIANGLES,
        )
        self.vao2 = self.window.ctx.geometry(
            [arcade.gl.BufferDescription(self.ssbo2, buffer_format, attributes)],
            mode=self.window.ctx.TRIANGLES,
        )

        shader_root = get_shader_root()
        self.program = self.window.ctx.load_program(
            geometry_shader=shader_root / "geom.glsl",
            vertex_shader=shader_root / "vert.glsl",
            fragment_shader=shader_root / "frag.glsl",
        )

        selected_compute_shader = selected_shader or "variants/compute.glsl"
        compute_shader_source = (shader_root / selected_compute_shader).read_text()
        compute_shader_source = compute_shader_source.replace(
            "COMPUTE_SIZE_X", str(Fluid.group_size.x)
        )
        compute_shader_source = compute_shader_source.replace(
            "COMPUTE_SIZE_Y", str(Fluid.group_size.y)
        )
        self.compute_shader = self.window.ctx.compute_shader(
            source=compute_shader_source
        )

    def _gen_initial_data(self, initial_x, initial_y):
        """Generate data for each particle"""
        radius = 3.0
        for i in range(Fluid.AGENT_COUNT):
            # Position/radius

            yield random.random() * self.window.width
            yield random.random() * self.window.height
            yield random.random() * self.window.height
            yield radius

            # Velocity
            yield 0.0
            yield 0.0
            yield 0.0
            yield 0.0  # vw (padding)

            # Color
            yield 1.0  # r
            yield 1.0  # g
            yield 1.0  # b
            yield 1.0  # a

    def render(self):
        self.ssbo1.bind_to_storage_buffer(binding=0)
        self.ssbo2.bind_to_storage_buffer(binding=1)

        # uniforms
        self.compute_shader["screen_size"] = self.window.get_size()
        # self.compute_shader["force"] = force
        # self.compute_shader["time"] = time.time() - self.start_time

        self.compute_shader.run(group_x=Fluid.group_size.x, group_y=Fluid.group_size.y)

        self.vao2.render(self.program)

        # flip buffers
        self.ssbo1, self.ssbo2 = self.ssbo2, self.ssbo1
        self.vao1, self.vao2 = self.vao2, self.vao1

    def on_update(self, delta_time):
        try:
            self.program["time"] = time.time() - self.start_time
        except KeyError:
            # glsl optimizes out unused uniforms :x
            pass
