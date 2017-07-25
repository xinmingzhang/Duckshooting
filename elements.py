import random
import math
import struct

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import StringProperty
from functools import partial


from kivy.lang import Builder

Builder.load_file('elements.kv')


def get_alpha_value(pos, img):
    size = img.texture.size
    texture_ratio = img.texture.size[0] / float(img.texture.size[1])
    widget_ratio = img.size[0] / float(img.size[1])
    if texture_ratio >= widget_ratio:
        ratio = size[0]/float(img.size[0])
        x = pos[0] - img.x
        y = pos[1] - img.y - (img.size[1] - size[1] / ratio) / 2.0
        if y <= 0 or y >= size[1] / ratio:
            return (0, 0, 0, 0)
    else:
        ratio = size[1] / float(img.size[1])
        x = pos[0] - img.x - (img.size[0] - size[0] / ratio) / 2.0
        y = pos[1] - img.y
        if x <=0 or x >=size[0]/ratio:
            return (0,0,0,0)
    x = int(round(x * ratio))
    y = size[1] - 1 - int(round(y * ratio))
    offset = (x + y * size[0]) * 4
    return struct.unpack_from('4B', img.texture.pixels, offset)

class EnermyLayer(FloatLayout):

    def on_touch_down(self,touch):
        app = App.get_running_app()
        if app.root.current_screen.ammo_num:
            for child in self.children[:]:
                if child.dispatch('on_touch_down',touch):
                    return True

class FlyingScore(BoxLayout):
    n1 = StringProperty('0')
    n2 = StringProperty('0')

    def __init__(self,score,pos,**kwargs):
        super(FlyingScore,self).__init__(pos = pos,**kwargs)
        self.score = score
        s = str(self.score)
        self.n1 = s[0]
        self.n2 = s[1]


    def on_parent(self,widget,parent):
        if parent:
            ani = Animation(center_x=0.05*Window.size[0],center_y= 0.95*Window.size[1])
            app = App.get_running_app()
            ani.bind(on_complete = lambda x,y:self.parent.remove_widget(self))
            ani.bind(on_complete = partial(app.root.current_screen.update_player_score,self.score))
            ani.start(self)

class End(Popup):
    pass


class Pause(Popup):
    pass

class Quit(Popup):
    pass

class Bullet(Image):
    pass

class EBullet(Image):
    pass

class RTarget(Image):
    def on_parent(self,widget,parent):
        if parent:
            ani = Animation(pos_hint = {'center_y':random.uniform(0.6,0.65)})
            ani += Animation(pos_hint = {'center_y':0.5})
            ani.bind(on_complete = lambda x,y:self.parent.remove_widget(self))
            ani.start(self)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if get_alpha_value(touch.pos,self) == (0,0,0,0):
                pass
            elif get_alpha_value(touch.pos,self) == (232,206,23,255):
                score = 17
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            elif get_alpha_value(touch.pos,self) == (187,128,68,255):
                score = 10
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            else:
                score = 13
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score,touch.pos))



class BTarget(Image):
    def on_parent(self,widget,parent):
        if parent:
            ani = Animation(pos_hint = {'center_y':random.uniform(0.5,0.55)})
            ani += Animation(pos_hint = {'center_y':0.4})
            ani.bind(on_complete = lambda x,y:self.parent.remove_widget(self))
            ani.start(self)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            if get_alpha_value(touch.pos,self) == (0,0,0,0):
                pass
            elif get_alpha_value(touch.pos,self) == (160,57,57,255):
                score = 16
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            elif get_alpha_value(touch.pos,self) == (166,201,203,255):
                score = 10
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            else:
                score = 12
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))




class BDuck(Image):
    def on_parent(self,widget,parent):
        if parent:
            ani = Animation(duration = 0)
            for i in range(10):
                ani += Animation(pos_hint = {'x':0.1*(i+1),'center_y':random.uniform(0.3,0.45)},duration = 0.5)
            ani.bind(on_complete = lambda x,y:self.parent.remove_widget(self))
            ani.start(self)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if get_alpha_value(touch.pos, self) == (0, 0, 0, 0):
                pass
            elif get_alpha_value(touch.pos, self) in [(232,106,23,255),(255,255,255,255)]:
                score = 20
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            else:
                score = 10
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))

class WDuck(Image):
    def on_parent(self,widget,parent):
        if parent:
            ani = Animation(duration = 0)
            for i in range(10):
                ani += Animation(pos_hint = {'x':0.1*(i+1),'center_y':random.uniform(0.2,0.3)},duration = 0.4)
            ani.bind(on_complete = lambda x,y:self.parent.remove_widget(self))
            ani.start(self)


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if get_alpha_value(touch.pos, self) == (0, 0, 0, 0):
                pass
            elif get_alpha_value(touch.pos, self) in [(232,106,23,255),(255,255,255,255)]:
                score = 25
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))
            else:
                score = 10
                app = App.get_running_app()
                app.root.current_screen.hud.add_widget(FlyingScore(score, touch.pos))








