from typing import overload

from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.uix.screenmanager import ScreenManager

# ==== TYPE CASTING ====
class _App(MDApp):

    sm: ScreenManager = ...
    nav: MDNavigationDrawer = ...
    data: dict = ...

    @overload
    def _change_screen(self, function, screen, **kwargs): ...

    @overload
    def change_screen(self, function=None, screen='main', **kwargs): ...
    
    def __init__(self, **kwargs):
        self = MDApp.get_running_app()

    def get_app(self):
        self = MDApp.get_running_app()

@overload
class List_obj(object): ...
# ==== END TYPES ====