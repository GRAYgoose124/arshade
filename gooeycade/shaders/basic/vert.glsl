#version 330

// Time since burst start
uniform float time;

in vec2 in_pos;
in vec2 in_vel;
in vec3 in_color;
in float in_fade_rate;


out vec4 color;

void main() {
    // Calculate alpha based on time and fade rate
    float alpha = 1.0 - (in_fade_rate * time);

    if(alpha < 0.0) alpha = 0;

    // Set the RGBA color
    color = vec4(in_color[0], in_color[1], in_color[2], alpha);

    // Adjust velocity based on gravity
    vec2 new_vel = in_vel;
    new_vel[1] -= time * 1.1;

    // Calculate a new position
    vec2 new_pos = in_pos + (time * new_vel);

    // Set the position. (x, y, z, w)
    gl_Position = vec4(new_pos, 0.0, 1);
}