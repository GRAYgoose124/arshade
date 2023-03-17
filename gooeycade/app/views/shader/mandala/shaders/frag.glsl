#version 450


uniform float time;

// Color passed in from the vertex shader
in vec4 col;

// The pixel we are writing to in the framebuffer
out vec4 fragColor;

// void main() {
//     fragColor = col;
// }

void main () {
    // This should work, but doesn't. gl_PointCoord is always (0, 0)...
    // I'm enabling gl.PROGRAM_POINT_SIZE and GL_POINT_SPRITE isn't necessary anymore...
    // discard the fragment if it's outside the unit circle
    // if (length(2.0 * gl_PointCoord - 1.0) > 1.0) {
    //     discard;
    // }

    fragColor = col;
}