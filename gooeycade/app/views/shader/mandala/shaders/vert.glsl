#version 430

uniform float time;

in vec2 in_pos;
in vec3 in_col;

out vec4 col;

void main()
{
    // set z plane to 0

    vec2 new_pos = vec2(in_pos.x * cos(time*in_pos.x), in_pos.y * sin(time*in_pos.y));
    gl_Position = vec4(new_pos, 0.0, 1.0);

    // set output color directly from input
    col = vec4(in_col.xyz, 1.);
}
