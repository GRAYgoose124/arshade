#version 430

// Color passed in from the vertex shader
in vec4 col;

// The pixel we are writing to in the framebuffer
out vec4 fragColor;

void main() {
    fragColor = col;
}