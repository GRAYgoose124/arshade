#version 430

uniform float time;
uniform mat4 model;
uniform float point_size;

// The id of the point
in float in_id;
in vec3 in_pos;
in vec3 in_col;

out vec4 col;

void main()
{
    // calculate z_plane for better clipping
    float z_plane = in_pos.z * 0.1;


    mat3 rot = mat3(in_pos.x*cos(time*in_pos.x), in_pos.y*sin(time*in_pos.y), 0., in_pos.x*sin(time*in_pos.y), in_pos.y*cos(time*in_pos.x), 0., 0., 0., 1.);
    vec3 new_pos = rot * in_pos;

    mat3 rot2_in_pos_norm = mat3(in_pos.x*cos(time*in_pos.x), in_pos.y*sin(time*in_pos.y), 0., in_pos.x*sin(time*in_pos.y), in_pos.y*cos(time*in_pos.x), 0., 0., 0., 1.);
    new_pos += rot2_in_pos_norm * in_pos;
    new_pos -= in_pos;


    gl_Position = model * vec4(new_pos, 1.);

    // if in_id mod 3 == 0, then rotate the point/offset it
    if (mod(in_id, 3.) == 0.) {
        gl_Position.x += sin(time*in_pos.x) * 0.1;
        gl_Position.y += cos(time*in_pos.y) * 0.1;
    }
    gl_PointSize = point_size;

    // set output color directly from input
    col = vec4(in_col.xyz, 1.);
}