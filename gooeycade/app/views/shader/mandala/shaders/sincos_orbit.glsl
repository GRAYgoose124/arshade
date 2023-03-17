#version 430

uniform float time;
uniform mat4 model;

in vec3 in_pos;
in vec3 in_col;

out vec4 col;

void main()
{
    // calculate z_plane for better clipping
    float z_plane = in_pos.z * 0.1;
    vec3 new_pos = vec3(in_pos.x * cos(time*in_pos.x), in_pos.y * sin(time*in_pos.y), in_pos.y*cos(time)*sin(time));

    gl_Position = model * vec4(new_pos.xyz, 1.0);
    gl_PointSize = 16.0;

    // set output color directly from input
    col = vec4(in_col.xyz, 1.);
}