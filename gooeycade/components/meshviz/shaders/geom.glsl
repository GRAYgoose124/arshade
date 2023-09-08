#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

// Use arcade's global projection UBO
uniform Projection {
    uniform mat4 matrix;
} proj;

in vec2 vertex_pos[];
in vec4 vertex_color[];
in float vertex_radius[];
in float v_strength[];

out vec2 g_uv;
out vec3 g_color;
out float g_strength;

void main() {
    vec2 pos = gl_in[0].gl_Position.xy;
    float radius = vertex_radius[0];
    vec4 color = vertex_color[0];
    float strength = v_strength[0];

    vec2 p1 = pos + vec2(-radius, -radius);
    vec2 p2 = pos + vec2(radius, -radius);
    vec2 p3 = pos + vec2(radius, radius);
    vec2 p4 = pos + vec2(-radius, radius);

    gl_Position = proj.matrix * vec4(p1, 0, 1);
    g_uv = vec2(0, 0);
    g_color = color.rgb;
    g_strength = strength;
    EmitVertex();

    gl_Position = proj.matrix * vec4(p2, 0, 1);
    g_uv = vec2(1, 0);
    g_color = color.rgb;
    g_strength = strength;
    EmitVertex();

    gl_Position = proj.matrix * vec4(p3, 0, 1);
    g_uv = vec2(1, 1);
    g_color = color.rgb;
    g_strength = strength;
    EmitVertex();

    gl_Position = proj.matrix * vec4(p4, 0, 1);
    g_uv = vec2(0, 1);
    g_color = color.rgb;
    g_strength = strength;
    EmitVertex();

    EndPrimitive();
}

