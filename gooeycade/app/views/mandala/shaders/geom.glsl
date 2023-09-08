#version 330 core

layout (points) in;
layout (line_strip, max_vertices = 100) out;

uniform float time; // time since program start

void main() {
  for (int i = 0; i < 100; i++) { // generate 100 output points per input point
    float angle = (i / 100.0) * 2.0 * 3.14159; // calculate angle of current output point
    float radius = 0.5 + (i / 100.0) * 0.5; // calculate radius of current output point
    vec3 pos = vec3(radius * cos(angle + time), radius * sin(angle + time), 0.0); // calculate position of current output point
    gl_Position = gl_in[0].gl_Position + vec4(pos, 0.0); // set position of current output point
    EmitVertex(); // emit current output point
  }
  EndPrimitive(); // end current primitive (the input point)
}
