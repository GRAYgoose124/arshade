import arcade
import arcade.gl as gl
import numpy as np
import pyglet
import pyglet.gl

from pathlib import Path


class MeshBuilder:
    def __init__(self, window) -> None:
        self.window = window

    def geometry_from_file(self, path: str | Path, resize=1.0) -> gl.Geometry:
        """Load a mesh from a file."""
        path = Path(__file__).parent / path

        # m = pyglet.model.load(str(path))
        try:
            m = pyglet.model.codecs.obj.parse_obj_file(str(path))[0]
        except (IndexError, ValueError):
            raise ValueError(
                f"Could not load mesh from {path} - make sure it has a material!"
            )

        # vertices is a list of 3-tuples, but m.vertices is a list of floats, so we need to reshape it
        vertices = np.array(m.vertices, dtype=np.float32).reshape(-1, 3) * resize
        normals = np.array(m.normals, dtype=np.float32).reshape(-1, 3) * resize
        tex_coords = np.array(m.tex_coords, dtype=np.float32).reshape(-1, 2) * resize

        vertex_buffer = gl.BufferDescription(
            self.window.ctx.buffer(data=vertices), "3f", ["in_position"]
        )
        normal_buffer = gl.BufferDescription(
            self.window.ctx.buffer(data=normals), "3f", ["in_normal"]
        )
        tex_coord_buffer = gl.BufferDescription(
            self.window.ctx.buffer(data=tex_coords), "2f", ["in_uv"]
        )

        return (
            self.window.ctx.geometry([vertex_buffer, normal_buffer, tex_coord_buffer]),
            vertices,
        )

    def geometry_from_vbo():
        pass

    @staticmethod
    def build_mesh() -> gl.Geometry:
        return gl.geometry.cube()
