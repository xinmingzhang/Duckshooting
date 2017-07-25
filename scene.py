import random
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.properties import NumericProperty,BooleanProperty
from kivy.clock import Clock
from elements import BDuck,Pause,Quit,Bullet,EBullet,RTarget,BTarget,WDuck,End
from sound import SHOT,RELOAD,MUSIC
from kivy.animation import Animation

Builder.load_file('scene.kv')

class TitleScreen(Screen):
    bg_texture = CoreImage('bg_red.png').texture
    bg_texture.wrap = 'repeat'


class GameScreen(Screen):

    t = NumericProperty(0)
    ammo_num = NumericProperty(5)
    time = NumericProperty(60)
    player_score = NumericProperty(0)
    gameplay = BooleanProperty(False)

    bg_texture = CoreImage('bg_wood.png').texture
    bg_texture.wrap = 'repeat'
    w1_texture = CoreImage('water1.png').texture
    w1_texture.wrap = 'repeat'
    w2_texture = CoreImage('water2.png').texture
    w2_texture.wrap = 'repeat'
    g1_texture = CoreImage('grass1.png').texture
    g1_texture.wrap = 'repeat'
    g2_texture = CoreImage('grass2.png').texture
    g2_texture.wrap = 'repeat'
    c1_texture = CoreImage('curtain_top.png').texture
    c1_texture.wrap = 'repeat'
    c2_texture = CoreImage('curtain_straight.png').texture
    c2_texture.wrap = 'repeat'
    pause_icon = CoreImage('transparentLight12.png').texture

    def on_enter(self,*args):
        self.init()

    def on_leave(self, *args):
        self.stop_update()
        MUSIC.stop()

    def init(self):
        self.pause = Pause()
        self.quit = Quit()
        self.end = End()
        self.max_ammo_num = 5
        self.ammo_num = 5
        self.time = 60
        self.player_score = 0
        Clock.schedule_once(self.on_ammo_num)
        self.init_curtain()
        self.start_game()
        self.gameplay = False
        MUSIC.play()

    def start_game(self):
        img = Image(source = 'text_ready.png',size_hint=(0.01,0.01),pos_hint = {'center_x':0.5,'center_y':0.5})
        ani = Animation(size_hint=(0.5,0.5),d=2)
        ani.bind(on_complete=lambda x, y: self.remove_widget(img))
        ani.bind(on_complete=self.move_curtain)
        self.add_widget(img)
        ani.start(img)

    def init_curtain(self):
        self.ids.right_curtain.pos_hint = {'top':0.9,'right':1}
        self.ids.left_curtain.pos_hint = {'top':0.9,'x':0}

    def move_curtain(self,*args):
        img = Image(source = 'text_go.png',size_hint=(0.01,0.01),pos_hint = {'center_x':0.5,'center_y':0.5})
        ani = Animation(size_hint=(0.5, 0.5),d =0.5)
        ani.bind(on_complete=lambda x, y: self.remove_widget(img))
        self.add_widget(img)
        ani.start(img)
        ani1 = Animation(pos_hint = {'top':0.9,'right':1.5})
        ani1.start(self.ids.right_curtain)
        ani2 = Animation(pos_hint = {'top':0.9,'x':-0.5})
        ani2.start(self.ids.left_curtain)
        ani2.bind(on_complete=self.update)
        self.gameplay = True


    def update(self,*args):
        Clock.schedule_interval(self.get_time, 1/60.0)
        Clock.schedule_interval(self.countdown_time, 1)
        Clock.schedule_interval(self.spawn, 1)

    def stop_update(self,*args):
        Clock.unschedule(self.get_time)
        Clock.unschedule(self.countdown_time)
        Clock.unschedule(self.spawn)


    def get_time(self,*args):
        self.t = Clock.get_boottime()


    def update_player_score(self,delta_score,*args):
        self.player_score += delta_score


    def countdown_time(self,*args):
        if self.time == 0:
            self.end_game()
        else:
            self.time -= 1


    def spawn(self,*args):
        seed = random.randint(1,4)
        if seed == 1:
            self.e_layer_1.add_widget(RTarget())
        elif seed == 2:
            self.e_layer_2.add_widget(BTarget())
        elif seed == 3:
            self.e_layer_3.add_widget(BDuck())
        else:
            self.e_layer_4.add_widget(WDuck())


    def on_touch_down(self,touch):
        self.ids.rifle.x = touch.pos[0]
        if self.gameplay:
            for child in self.children[:]:
                if child.dispatch('on_touch_down',touch):
                    return True
            if self.ammo_num > 0:
                self.ammo_num -= 1
                SHOT.play()


    def on_ammo_num(self,*args):
        self.magazine.clear_widgets()
        for num in range(self.ammo_num):
            self.magazine.add_widget(Bullet())
        for num in range(self.max_ammo_num - self.ammo_num):
            self.magazine.add_widget(EBullet())

    def end_game(self,*args):
        self.stop_update()
        img = Image(source = 'text_timeup.png',size_hint=(0.01,0.01),pos_hint = {'center_x':0.5,'center_y':0.5})
        ani = Animation(size_hint=(0.5, 0.5),d =0.5)
        ani.bind(on_complete=lambda x, y: self.remove_widget(img))
        ani.bind(on_complete=self.end.open)
        self.add_widget(img)
        ani.start(img)


class MenuScreen(Screen):
    bg_texture1 = CoreImage('bg_red.png').texture
    bg_texture1.wrap = 'repeat'
    bg_texture2 = CoreImage('bg_blue.png').texture
    bg_texture2.wrap = 'repeat'
    bg_texture3 = CoreImage('bg_green.png').texture
    bg_texture3.wrap = 'repeat'


class ThxScreen(Screen):
    bg_texture = CoreImage('bg_green.png').texture
    bg_texture.wrap = 'repeat'

class ShopScreen(Screen):
    bg_texture = CoreImage('bg_blue.png').texture
    bg_texture.wrap = 'repeat'