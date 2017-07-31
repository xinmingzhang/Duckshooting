from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from scene import TitleScreen,GameScreen,MenuScreen,ThxScreen,ShopScreen




sm = ScreenManager()
sm.add_widget(TitleScreen(name = 'TITLE'))
sm.add_widget(GameScreen(name = 'GAME'))
sm.add_widget(MenuScreen(name = 'MENU'))
sm.add_widget(ThxScreen(name = 'THX'))
sm.add_widget(ShopScreen(name = 'SHOP'))
sm.current = 'TITLE'

class DuckShooting(App):
    def build(self):
        return sm

if __name__ == '__main__':
    DuckShooting().run()