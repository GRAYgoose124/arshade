import pyglet

from dataclasses import dataclass, field
from math import cos, sin

#TODO: uniforms / blocks

@dataclass
class ProgramDefinition:
    vert_shader: str | None = field(default=None, kw_only=True)
    description: tuple[str, list[str]] | None = field(default=None, kw_only=True)
    modelview_enabled: bool = False
    time_offset: float = 0.0
    speed: float = 1.0
    render_modes: tuple[int, int] = field(default=(pyglet.gl.GL_LINE_STRIP, pyglet.gl.GL_POINTS), kw_only=True)

    def initial_data(self, N=0):
        raise NotImplementedError
    

    
@dataclass
class ParallelSpiralOrbit(ProgramDefinition):
    vert_shader: str | None = field(default="parallel_spiral_orbit.glsl", kw_only=True)
    description: tuple[str, list[str]] | None = field(default=("f 3f 3f", ["in_id", "in_pos", "in_col"]))
    time_offset: float = 0.0
    speed: float = 0.001
    render_modes: tuple[int, int] = field(default=(pyglet.gl.GL_LINES, pyglet.gl.GL_POINTS), kw_only=True)

    def initial_data(self, N=10000):
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
    description: tuple[str, list[str]] | None = field(default=("3f 3f", ["in_pos", "in_col"]), kw_only=True)
    modelview_enabled: bool = True

    def initial_data(self, N=1000):
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