import arcade.gl as gl
import numpy as np


class MeshBuilder:
    def __init__(self, window) -> None:
        self.window = window

    @staticmethod
    def build_mesh() -> gl.Geometry:
        return gl.geometry.cube()