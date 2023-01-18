import json, os

from kivymd.app import MDApp

# Widgets
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem

# Theme
from kivymd.theming import ThemeManager

# Modules
from .GUI.Pages import (Main, Loading)

# Type helpers
from typing import Union, List

class CoreApplication(MDApp):

    data: dict = json.load(open(os.path.join(os.path.dirname(__file__), "Data", "Data.json"), 'r'))
    pages: Union[None, List[Screen]] = None

    def build(self) -> ScreenManager:
        
        self.title = 'InterrogationPlanner V2'
        self.theme_cls = ThemeManager()
        self.theme_cls.theme_style = 'Dark'

        self.navigationlayout = MDNavigationLayout()

        self.sm = ScreenManager(transition=SlideTransition())

        self.sm.add_widget(Main())
        self.sm.add_widget(Loading())

        self.navigationlayout.add_widget(self.sm)

        self.nav = self.create_navigation_drower()
        self.navigationlayout.add_widget(self.nav)

        return self.navigationlayout

    def create_navigation_drower(self) -> MDNavigationDrawer:
        sv = ScrollView()
        lst = MDList()

        #from GUI.Widget import Add_Dialog
        items = [
            OneLineListItem(text='Crea una nuova lista', 
                on_release= lambda *args: [
                    MDApp.get_running_app().nav.set_state('close'),
                    #self._change_screen(Add_Dialog().wait, 'preferences',**MainApp.new_list_dialog)
                ]),
            OneLineListItem(text='Credit',
                on_release=lambda *args: [
                    MDApp.get_running_app().nav.set_state('close'),
                    #self.change_screen(None, 'credit')
                ])
            ]

        for i in items:
            lst.add_widget(i)
        
        sv.add_widget(lst)
        
        navigationdrawer = MDNavigationDrawer()
        navigationdrawer.add_widget(sv)

        return navigationdrawer
