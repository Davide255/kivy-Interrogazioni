from typing import overload, Union, List

from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.event import EventDispatcher

# ==== TYPE CASTING ====
class _App:

    sm: ScreenManager = ...
    nav: MDNavigationDrawer = ...
    data: dict = ...
    pages: Union[None, List[Screen]] = ...

    @overload
    def _change_screen(self, function, screen, **kwargs): ...

    @overload
    def change_screen(self, function=None, screen='main', **kwargs): ...
    
    def __new__(self) -> MDApp:
        return MDApp.get_running_app()

    def get_app(self) -> MDApp:
        return MDApp.get_running_app()

class _DataStore(EventDispatcher):
    days: dict = ...
    days_vol: dict = ...
    list: dict = ...
# ==== END TYPES ====