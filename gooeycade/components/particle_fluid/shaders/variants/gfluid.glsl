#version 430

// Set up our compute groups
layout(local_size_x=COMPUTE_SIZE_X, local_size_y=COMPUTE_SIZE_Y) in;

// Input uniforms
uniform vec2 screen_size;

struct Ball {
    vec4 pos;
    vec4 vel;
    vec4 color;
};

// Input buffer
layout(std430, binding=0) buffer balls_in {
    Ball balls[];
} In;

// Output buffer
layout(std430, binding=1) buffer balls_out {
    Ball balls[];
} Out;

void main() {
    int curBallIndex = int(gl_GlobalInvocationID.x);

    Ball in_ball = In.balls[curBallIndex];

    vec3 pos = in_ball.pos.xyz;
    vec3 vel = in_ball.vel.xyz;

    vec3 force = vec3(0.0);

    float mass = 1.0;
    float restDensity = 2000.0;
    float gasConstant = 1000.0;
    float viscosity = 0.1;
    float h = 100.0; // Smoothing length
    float h2 = h * h;

    float density = 0.0;
    vec3 pressureForce = vec3(0.0);
    vec3 viscosityForce = vec3(0.0);

    // Compute density and forces
    for (int i = 0; i < In.balls.length(); i++) {
        if (i == curBallIndex) continue;

        vec3 otherPos = In.balls[i].pos.xyz;
        vec3 diff = pos - otherPos;
        float dist2 = dot(diff, diff);

        if (dist2 < h2) {
            float dist = sqrt(dist2);

            // Compute density
            float q = (1.0 - dist / h);
            density += mass * (q * q * q);

            // Compute pressure force
            float pressure = gasConstant * (density - restDensity);
            pressureForce += -normalize(diff) * pressure * (q * q);

            // Compute viscosity force
            vec3 otherVel = In.balls[i].vel.xyz;
            viscosityForce += viscosity * (otherVel - vel) * q;
        }
    }

    // Apply forces to velocity
    force += pressureForce + viscosityForce;

    // Add gravitational force
    vec3 gravity = vec3(0.0, -1000000.0, 0.0);
    force += gravity * mass;

    // Scale force
    float scale = 0.001 / In.balls.length();

    // Integrate velocity
    vel += force * scale;
    // vel *= 0.99; // Optional: Apply damping to velocity to reduce energy over time

    // Integrate position
    pos += vel;

    // Boundaries
    float screenWidth = screen_size.x;
    float screenHeight = screen_size.y;

    if (pos.x < 0.0) { pos.x = 0.0; vel.x *= -0.5; }
    if (pos.x > screenWidth) { pos.x = screenWidth; vel.x *= -0.5; }
    if (pos.y < 0.0) { pos.y = 0.0; vel.y *= -0.5; }
    if (pos.y > screenHeight) { pos.y = screenHeight; vel.y *= -0.5; }
    if (pos.z < 0.0) { pos.z = 0.0; vel.z *= -0.5; }
    if (pos.z > screenWidth) { pos.z = screenWidth; vel.z *= -0.5; }

    // Store output
    Ball out_ball;
    out_ball.pos = vec4(pos, in_ball.pos.w);
    out_ball.vel = vec4(vel, in_ball.vel.w);
    out_ball.color = in_ball.color;

    Out.balls[curBallIndex] = out_ball;
}
