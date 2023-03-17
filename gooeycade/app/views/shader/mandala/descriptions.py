import json
import pyglet

from dataclasses import asdict, dataclass, field
from math import cos, sin

#TODO: configs
#TODO: uniforms / blocks

@dataclass
class ProgramDefinition:
    vert_shader: str | None = field(default=None, kw_only=True)
    description: tuple[str, list[str]] | None = field(default=None, kw_only=True)
    modelview_enabled: bool = False
    point_size: float = 1.0
    time_offset: float = 0.0
    speed: float = 1.0
    render_modes: tuple[int, int] = field(default=(pyglet.gl.GL_LINE_STRIP, pyglet.gl.GL_POINTS), kw_only=True)
    N: int = 1000

    def initial_data(self):
        N = self.N
        raise NotImplementedError
    
    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)
    
    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))
    
    def to_dict(self):
        return asdict(self)
    
    def to_json(self):
        return json.dumps(self.to_dict())

    
@dataclass
class ParallelSpiralOrbit(ProgramDefinition):
    vert_shader: str | None = field(default="parallel_spiral_orbit.glsl", kw_only=True)
    description: tuple[str, list[str]] | None = field(default=("f 3f 3f", ["in_id", "in_pos", "in_col"]))
    time_offset: float = 900.0
    point_size: float = 4.0
    speed: float = 0.0001
    render_modes: tuple[int, int] = field(default=(pyglet.gl.GL_LINE_STRIP, pyglet.gl.GL_POINTS), kw_only=True)
    modelview_enabled: bool = False
    N: int = 10000
    

    def initial_data(self):
        """ This generates a set of points along a radius of a circle which are then rotated at different rates. """
        N = self.N
        for i in range(N):
            angle = 0.0
            # outside point and inside point are fixed
            radius = ((N-(i + 1)) / N)
            
            x = radius * cos(angle)
            y = radius * cos(angle)
            z = 0.0

            r = cos(i)
            g = sin(i)
            b = 0.25 + cos(i) * sin(i)

            yield i

            yield x
            yield y
            yield z

            yield r
            yield g
            yield b


@dataclass
class SinCosOrbit(ProgramDefinition):
    vert_shader: str | None = field(default="sincos_orbit.glsl", kw_only=True)
    description: tuple[str, list[str]] | None = field(default=("f 3f 3f", ["in_id", "in_pos", "in_col"]), kw_only=True)
    render_modes: tuple[int, int] = field(default=(pyglet.gl.GL_POINTS, pyglet.gl.GL_TRIANGLE_STRIP), kw_only=True)
    modelview_enabled: bool = False
    point_size: float = 4.0
    speed: float = 1.0
    N = 1000

    def initial_data(self):
        """ Think a deconstructed spiral along the X/Y plane """
        N = self.N
        for i in range(N):
            angle = (i / N) * 2.0 * 3.14159
            radius = 0.5 + (i / N) * 0.5
            x = radius * cos(angle)
            y = radius * sin(angle)
            z = 1. / (i+1)
            r = (cos(angle * 3.0) + 1.0) / 2.0
            g = (cos(angle * 5.0) + 1.0) / 2.0
            b = (cos(angle * 7.0) + 1.0) / 2.0

            yield i
            
            yield x
            yield y
            yield z

            yield r 
            yield g
            yield b