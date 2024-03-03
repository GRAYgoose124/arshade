import traceback
import arcade
import arcade.gui
import time
import pyglet
import logging
import numpy as np

from pyglet.math import Mat4
from pathlib import Path
from collections import namedtuple

from gooeycade.app.shader import ShaderViewComponent

from .mesh import MeshBuilder

logger = logging.getLogger(__name__)


class MeshView(ShaderViewComponent):
    """A view that renders a selected mesh."""

    def __init__(self):
        super().__init__()
        self._time = 0
        self._start_time = 0

        self.__mesh = None
        self._mesh_path = None

        self.__program = None
        self.__render_fbo = None

        self._ui_manager = None

        self.group_size = None

    def setup(self):
        self._time = 0
        self._start_time = time.time()
        self.group_size = namedtuple("ComputeGroup", ["x", "y", "z"])(x=12, y=12, z=1)

        # TODO GUI selector
        vertices = self.__load_mesh_from_file("toRus.obj", resize=1.0)

        # prepare graphics
        self.__program = self.__load_mesh_shader()
        self.__render_fbo = self.__build_render_fbo()

        if vertices is not None:
            self.__gen_octree(vertices)

        # UI
        self._ui_manager = arcade.gui.UIManager(self.window)
        self._ui_manager.add(self.__build_mesh_selector())

    def __gen_octree(self, vertices):
        octree_program = self.__load_octree_shader()
        octree_buffer = self.window.ctx.buffer(
            reserve=self.group_size.x * self.group_size.y, data=vertices
        )

        vertex_buffer = self.window.ctx.buffer(data=vertices)
        vertex_buffer.bind_to_storage_buffer(binding=0)
        octree_buffer.bind_to_storage_buffer(binding=1)
        octree_program.run(
            group_x=self.group_size.x,
            group_y=self.group_size.y,
            group_z=self.group_size.z,
        )
        # dummy normals and tex coords from vertex buffer
        normals = np.array(vertices, dtype=np.float32).reshape(-1, 3)
        tex_coords = np.array(vertices, dtype=np.float32).reshape(-1, 2)
        self.octree_geometry = self.window.ctx.geometry(
            [
                arcade.gl.BufferDescription(octree_buffer, "3f", ["in_position"]),
                arcade.gl.BufferDescription(
                    self.window.ctx.buffer(data=normals), "3f", ["in_normal"]
                ),
                arcade.gl.BufferDescription(
                    self.window.ctx.buffer(data=tex_coords), "2f", ["in_uv"]
                ),
            ]
        )
        logger.info(f"{self.octree_geometry.num_vertices=}")

    @property
    def time(self):
        """Returns the shader time."""
        return self._time

    @property
    def start_time(self):
        """Returns the shader start time."""
        return self._start_time

    @property
    def mesh(self):
        """Returns the mesh to be rendered."""
        return self.__mesh

    @property
    def mesh_path(self):
        """Returns the path to the mesh to be rendered."""
        return self._mesh_path

    @mesh_path.setter
    def mesh_path(self, path):
        """Sets the path to the mesh to be rendered and reloads the mesh."""
        self.__load_mesh_from_file(path)

    @property
    def manager(self):
        """Returns the UI manager."""
        return self._ui_manager

    def __load_mesh_from_file(self, path: Path | str, resize: float = 1.0):
        """Loads a mesh from a file. OBJ support only."""
        # TODO: better root control
        self._mesh_path = Path(__file__).parent / "meshes" / path

        try:
            self.__mesh, vertices = MeshBuilder(self.window).geometry_from_file(
                self._mesh_path, resize=resize
            )
        except (pyglet.model.codecs.ModelDecodeException, FileNotFoundError) as e:
            logger.warning(f"Failed to load mesh: {self.mesh_path}.")
            traceback.print_exc()
            self.__mesh = "BAD_MESH_FILE"
            vertices = None

        return vertices

    def __load_mesh_shader(self, vert=None, frag=None, geom=None, shader_root=None):
        """Loads a shader program for rendering the mesh."""
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
            vertex_shader=vs,
            geometry_shader=gs,
            fragment_shader=fs,
        )

        program["projection"] = Mat4.perspective_projection(
            self.window.aspect_ratio, 1.0, 10.0, 70
        )
        return program

    def __load_octree_shader(self, compute=None, shader_root=None):
        """Loads a shader program for octree calculation."""
        default_root = Path(__file__).parent / "shaders"
        if shader_root is None:
            shader_root = default_root

        if compute is not None:
            cs = (shader_root / compute).read_text()
        else:
            cs = (default_root / "octree_compute.glsl").read_text()

        cs = cs.replace("COMPUTE_SIZE_X", str(self.group_size.x))
        cs = cs.replace("COMPUTE_SIZE_Y", str(self.group_size.y))
        cs = cs.replace("COMPUTE_SIZE_Z", str(self.group_size.z))

        program = self.window.ctx.compute_shader(source=cs)
        return program

    def __build_render_fbo(self):
        """Builds the framebuffer object for off-screen rendering."""
        return self.window.ctx.framebuffer(
            color_attachments=[
                self.window.ctx.texture(
                    (self.window.width, self.window.height), components=4
                )
            ],
            depth_attachment=self.window.ctx.depth_texture(
                (self.window.width, self.window.height)
            ),
        )

    def __build_mesh_selector(self):
        """Builds the Mesh Viewer's selection GUI."""
        menu = arcade.gui.UIBoxLayout()

        label = arcade.gui.UITextArea(
            text="Mesh", font_size=24, text_color=arcade.color.WHITE
        )
        menu.add(
            arcade.gui.UIAnchorWidget(child=label, anchor_x="left", anchor_y="top")
        )

        return menu

    def on_draw(self):
        arcade.start_render()

        # TODO: Add a loading screen when no mesh is loaded and disable the mesh render.
        # Note: This should be alright because drawing only needs to be performed when a mesh is loaded.
        try:
            with self.__render_fbo:
                self.__render_fbo.clear()

                self.mesh.render(self.__program, mode=self.window.ctx.TRIANGLES)
                self.octree_geometry.render(self.__program, mode=self.window.ctx.LINES)

            self.window.ctx.copy_framebuffer(self.__render_fbo, self.window.ctx.screen)
        except AttributeError:
            pass

        self._ui_manager.draw()

    def on_update(self, delta_time):
        self._time += delta_time

        if self.mesh is None:
            # TODO: Add mesh to a ui manager and disable it when no mesh is loaded.
            self.__load_mesh_from_file("cube.obj", resize=0.1)
            return

        # update the model matrix
        model = Mat4.from_rotation(self.time / 2, (0, 1, 0)).translate((0, 0, -2.5))

        projection = Mat4.orthogonal_projection(-1, 1, -1, 1, -1, 1)

        self.__program["model"] = model

    def on_show(self):
        self.window.ctx.enable_only(self.window.ctx.BLEND, self.window.ctx.DEPTH_TEST)
        self._ui_manager.enable()

        return super().on_show()

    def on_hide_view(self):
        self._ui_manager.disable()
        return super().on_hide_view()

    def on_resize(self, width: int, height: int):
        # rebuild the FBO with the new size
        self.__render_fbo = self.__build_render_fbo()


# Component registration
ComponentView = MeshView
