#version 330

uniform float time;


in vec4 color;
out vec4 fragColor;

void main() {
    fragColor = vec4(color);
}