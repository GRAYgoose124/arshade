from dataclasses import dataclass, field
import time
import arcade
import arcade.gl
import numpy as np
from pathlib import Path


@dataclass
class OctreeCalculator:
    window: arcade.Window
    mesh_vertices: np.ndarray  # Your mesh vertices
    octree_program: arcade.gl.ComputeShader = field(default=None, init=False)
    octree_buffer: arcade.gl.Buffer = field(default=None, init=False)

    def __post_init__(self):
        # Load your compute shader for octree calculation
        shader_root = Path(__file__).parent / "shaders"
        compute_shader_source = (shader_root / "octree_compute.glsl").read_text()
        self.octree_program = self.window.ctx.compute_shader(
            source=compute_shader_source
        )

        # Create a buffer for the mesh vertices
        self.vertex_buffer = self.window.ctx.buffer(
            data=self.mesh_vertices.astype("f4").tobytes()
        )

        # Reserve buffer for octree data (size depends on your octree structure)
        self.octree_buffer = self.window.ctx.buffer(reserve=1024)

    def calculate_octree(self):
        # Bind buffers to the compute shader
        self.vertex_buffer.bind_to_storage_buffer(binding=0)
        self.octree_buffer.bind_to_storage_buffer(binding=1)

        self.octree_program.run(group_x=256, group_y=1, group_z=1)

        octree_data = self.octree_buffer.read()
