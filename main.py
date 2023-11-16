
import os
os.environ["KCFG_KIVY_LOG_LEVEL"] = "debug"
os.environ["KIVY_GL_DEBUG"] = "1"
import math
from kivy.app import App
from kivy.clock import Clock
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJLoader, STLLoader, OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Mesh, Material

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
# obj_file = os.path.join(_this_path, "demodata/MQ-27.obj")
# obj_file = os.path.join(_this_path, "NC/card3.obj")
obj_file = os.path.join(_this_path, "NC/card33_1.obj")
mtl_file = os.path.join(_this_path, "NC/card33_1.mtl")
shader_file = os.path.join(_this_path, "NC/simple.glsl")
# obj_file = os.path.join(_this_path, "./data/monkey.obj")
# stl_file = os.path.join(_this_path, "./data/untitled.stl")


class ObjectTrackball(FloatLayout):

    def __init__(self, camera, radius, *args, **kw):
        super(ObjectTrackball, self).__init__(*args, **kw)
        self.camera = camera
        self.radius = radius
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = radius
        camera.look_at((0, 0, 0))

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = -1 * (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        touch.grab(self)
        self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        self._touches.remove(touch)

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        y = self.radius * math.cos(_phi)
        self.camera.pos = x, y, z
        self.camera.look_at((0, 0, 0))


class MainApp(App):

    def build(self):
        self.renderer = Renderer(shader_file=shader_file)
        self.renderer.set_clear_color((.16, .30, .44, 1.))
        scene = Scene()
        # camera = PerspectiveCamera(30, 1, 100, 2500)
        camera = PerspectiveCamera(3, 1, 100, 2500)
        loader = OBJMTLLoader()
        obj = loader.load(obj_file, mtl_file)
        # material = Material(color=(0.3, 0., 0.3), diffuse=(0.3, 0.3, 0.3),
        #                 specular=(0., 0., 0.))

        # loader = STLLoader()
        # obj = loader.load(stl_file,material)
        self.obj3d = obj
        self.camera = camera
        # root = ObjectTrackball(camera, 1500)
        root = ObjectTrackball(camera, 150)

        scene.add(obj)

        self.renderer.render(scene, camera)
        self.renderer.main_light.intensity = 500

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    MainApp().run()
