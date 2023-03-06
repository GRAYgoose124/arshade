#version 430

uniform float time;

in vec2 g_uv;
in vec2 vertex_pos;
in vec3 g_color;
in float g_strength;

out vec4 out_color;

void main()
{
    float l = length(vec2(0.5, 0.5) - g_uv.xy);
    if ( l > 0.5)
    {
        discard;
    }
    float alpha;
    if (l == 0.0)
        alpha = g_strength;
    else {
        alpha = min(1.0, g_strength - (l * 2));
    }
    vec3 c = g_color.rgb;

    // particles at the edges of the screen are more colorful
    c = cos(time*.13)*mix(c, vec3(.0, 1.0, 0.0), g_uv.x) + sin(time*.1)*mix(c, vec3(0.0, 0.0, 1.0), g_uv.y);
    c *= c * 1.0 - l;

    out_color = vec4(c, alpha);
}
