#version 430

// Set up our compute groups
layout(local_size_x=COMPUTE_SIZE_X, local_size_y=COMPUTE_SIZE_Y) in;

// Input uniforms go here if you need them.
// Some examples:
//uniform vec2 screen_size;
//uniform vec2 force;
//uniform float frame_time;

struct Ball
{
    vec4 pos;
    vec4 vel;
    vec4 color;
};

// Input buffer
layout(std430, binding=0) buffer balls_in
{
    Ball balls[];
} In;

// Output buffer
layout(std430, binding=1) buffer balls_out
{
    Ball balls[];
} Out;

void main()
{
    int curBallIndex = int(gl_GlobalInvocationID);

    Ball in_ball = In.balls[curBallIndex];

    vec4 p = in_ball.pos.xyzw;
    vec4 v = in_ball.vel.xyzw;

    p.xyz += v.xyz;

    for (int i=0; i < In.balls.length(); i++) {
        //  if (i == x)
        //      continue;

        float dist = distance(In.balls[i].pos.xyzw.xyz, p.xyz);
        float distanceSquared = dist * dist;

        float minDistance = 0.01;
        float gravityStrength = 0.003;
        float simulationSpeed = 0.5;
        float force = min(minDistance, gravityStrength / distanceSquared) * -simulationSpeed;

        vec3 diff = p.xyz - In.balls[i].pos.xyzw.xyz;
        //  diff = normalize(diff);
        vec3 delta_v = diff * force;
        v.xyz += delta_v;
    }


    Ball out_ball;
    out_ball.pos.xyzw = p.xyzw;
    out_ball.vel.xyzw = v.xyzw;

    vec4 c = in_ball.color.xyzw;
    out_ball.color.xyzw = c.xyzw;

    Out.balls[curBallIndex] = out_ball;
}
