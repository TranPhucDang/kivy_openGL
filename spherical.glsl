// Vertex shader
---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif
#version 400
layout(location = 0) in vec4 vPosition;
layout(location = 1) in vec2 vTexCoord;
smooth out vec2 fTexCoord;

void main()
{
    gl_Position = vPosition;
    fTexCoord = vTexCoord;
}
// Fragment shader
---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif
#version 400
smooth in vec2 fTexCoord;
out vec4 FragColor;
uniform sampler2D reflectionMap;

void main()
{
    FragColor = texture(reflectionMap, fTexCoord);
}
