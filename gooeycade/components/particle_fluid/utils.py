from pathlib import Path


def get_shader_root():
    return Path(__file__).parent / "shaders"


def get_shader_variants():
    for shader in (get_shader_root() / "variants").glob("*.glsl"):
        yield shader.name
