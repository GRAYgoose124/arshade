#version 450 core

uniform float time;
uniform mat4 model;

#define INV_ID_MAX 0.008
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
    new_pos.xy = mat2(cos(time * (1.0 - in_id)), -sin(time * (1.0 - in_id)), sin(time * (1.0 - in_id)), cos(time * (1.0 - in_id))) * in_pos.xy;

    gl_Position = vec4(new_pos.xyz, 1.0);
    gl_PointSize = 2.0;
    col = vec4(in_col.xyz, 1.);
}
