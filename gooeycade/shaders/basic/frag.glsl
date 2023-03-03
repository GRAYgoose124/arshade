#version 330

uniform float time;


in vec4 color;
out vec4 fragColor;

void main() {
    vec2 p = gl_FragCoord.xy;

    // vary color over time and space
    float alpha = 2.*(cos(time*2.)+sin(time*1.5)) - 2.;
    alpha = step(.1, alpha) * alpha;
    vec4 dV = vec4(0.5 + 0.5 * sin(time * vec3(1.5, 2, 4)), alpha);

    fragColor = vec4(color * dV);
}