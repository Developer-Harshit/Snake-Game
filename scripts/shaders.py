import pygame
import moderngl
import sys
from array import array

# Creating context
ctx = moderngl.create_context()

# Creating Buffer thingy
quad_buffer = ctx.buffer(
    data=array(
        "f",
        [
            -1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            0.0,
            -1.0,
            -1.0,
            0.0,
            1.0,
            1.0,
            -1.0,
            1.0,
            1.0,
        ],
    )
)

# Vertex Shader
vert_shader = """
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}

"""
# Fragment Shader
frag_shader = """
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    
    f_color = vec4(texture(tex, uvs).r * 1.1,texture(tex, uvs).g * 1.2,texture(tex, uvs).b * 2.0, 1.0);
}
"""

# Creating Program
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view("1"))
    return tex
