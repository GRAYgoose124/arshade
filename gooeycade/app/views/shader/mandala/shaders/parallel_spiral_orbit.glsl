#version 450 core

uniform float time;
uniform mat4 model;

// The id of the point
in float in_id;
// The position of the point
in vec3 in_pos;
// The default color of the point
in vec3 in_col;

out vec4 col;

void main()
{
    vec3 new_pos = in_pos;
    float t = (time) * (1.0 - in_id);
    new_pos.xy = mat2(cos(t), -sin(t), sin(t), cos(t)) * in_pos.xy;

    gl_Position = vec4(new_pos.xyz, 1.0);
    gl_PointSize = 4.0;
    col = vec4(in_col.xyz, 1.);
}
