#version 450


uniform float time;

// Color passed in from the vertex shader
in vec4 col;

// The pixel we are writing to in the framebuffer
out vec4 fragColor;

// void main() {
//     fragColor = col;
// }


vec4 hueShift (vec4 c){
    float hue = time * 0.1;
    float sat = 1.0;
    float val = 1.0;

    float r = c.r;
    float g = c.g;
    float b = c.b;

    float h, s, v;
    float f, p, q, t;

    float i = floor(hue * 6.0);
    f = hue * 6.0 - i;
    p = val * (1.0 - sat);
    q = val * (1.0 - f * sat);
    t = val * (1.0 - (1.0 - f) * sat);

    if (i == 0.0) {
        r = val;
        g = t;
        b = p;
    } else if (i == 1.0) {
        r = q;
        g = val;
        b = p;
    } else if (i == 2.0) {
        r = p;
        g = val;
        b = t;
    } else if (i == 3.0) {
        r = p;
        g = q;
        b = val;
    } else if (i == 4.0) {
        r = t;
        g = p;
        b = val;
    } else if (i == 5.0) {
        r = val;
        g = p;
        b = q;
    }

    return vec4(r, g, b, c.a);
}


void main () {
    // This should work, but doesn't. gl_PointCoord is always (0, 0)...
    // I'm enabling gl.PROGRAM_POINT_SIZE and GL_POINT_SPRITE isn't necessary anymore...
    // discard the fragment if it's outside the unit circle
    // if (length(2.0 * gl_PointCoord - 1.0) > 1.0) {
    //     discard;
    // }


    fragColor = hueShift(col);
}