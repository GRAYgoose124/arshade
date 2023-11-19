#version 450

layout (local_size_x = COMPUTE_SIZE_X, local_size_y = COMPUTE_SIZE_Y, local_size_z = COMPUTE_SIZE_Z) in;

// Buffer for mesh vertices
layout(std430, binding = 0) buffer VertexBuffer {
    vec3 vertices[];
};

// Buffer for octree vertices
layout(std430, binding = 1) buffer OctreeBuffer {
    vec3 octreeVertices[];
};

void main() {
    uint globalID = gl_GlobalInvocationID.x + gl_GlobalInvocationID.y * gl_NumWorkGroups.x * gl_WorkGroupSize.x;

    // Check if the globalID is within bounds
    if (globalID < vertices.length()) {
        // Example operation: scale each vertex
        vec3 scaledVertex = vertices[globalID] * 2.0;
        octreeVertices[globalID] = scaledVertex;
    }
}
