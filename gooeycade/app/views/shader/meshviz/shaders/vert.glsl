#version 430

uniform mat4 projection;
uniform mat4 model;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

out vec2 uv;

void main()
{
    gl_Position = projection * model * vec4(in_position, 1.0);
    uv = in_uv;
}