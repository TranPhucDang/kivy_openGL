from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Renderer, Scene
from kivy3.loaders import OBJLoader
from kivy.core.window import Window

VERTEX_SHADER = """
#version 400
layout(location = 0) in vec4 vPosition;
layout(location = 1) in vec2 vTexCoord;
smooth out vec2 fTexCoord;

void main()
{
    gl_Position = vPosition;
    fTexCoord = vTexCoord;
}
"""

FRAGMENT_SHADER = """
#version 400
smooth in vec2 fTexCoord;
out vec4 FragColor;
uniform sampler2D reflectionMap;

void main()
{
    FragColor = texture(reflectionMap, fTexCoord);
}
"""

class SphericalReflectionApp(App):
    def build(self):
        layout = FloatLayout(size=Window.size)

        # Load the 3D model
        obj_loader = OBJLoader()
        model = obj_loader.load('shading/card2_4.obj')

        # Set up the renderer and scene
        renderer = Renderer(shader_file=(VERTEX_SHADER, FRAGMENT_SHADER))
        scene = Scene()

        # Load the spherical reflection map
        reflection_map = renderer.load_texture('./reflection_map.jpg')

        # Assign the reflection map to the shader
        renderer.uniforms['reflectionMap'] = 0  # 0 corresponds to GL_TEXTURE0
        reflection_map.bind(0)

        # Add the model to the scene
        scene.add_child(model)

        # Set the scene for the renderer
        renderer.set_clear_color(color=(0, 0, 0, 0))
        renderer.render(scene)

        layout.add_widget(renderer)
        return layout

if __name__ == '__main__':
    SphericalReflectionApp().run()
