from threading import Thread
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.uix.screenmanager import *
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivy.core.window import Window
from kivymd.theming import ThemeManager

from GUI.Screens import *

class MainApp(MDApp):

    ''' Start of the application '''
    
    data: dict = json.load(open('Data.json', 'r'))

    def build(self):
        self.title = 'Interrogazioni'
        self.theme_cls = ThemeManager()
        Window.bind(on_request_close=self.save)
        Window.bind(on_resize=lambda *args: Lists()._refresh())

        #initiallizing root variables
        MainApp._root = MDNavigationLayout()
        MainApp.sm = ScreenManager(transition=SlideTransition())
        MainApp.nav = MDNavigationDrawer()

        MainApp._root.add_widget(MainApp.sm)
        MainApp._root.add_widget(MainApp.nav)

        MainApp.new_list_dialog = {
            'title':'Nomina la nuova lista.',
            'l_text':'Inserisci il nome della nuova lista per modificarla in futuro.',
            't_text':'Nome:',
            'required':True,
            'helper_text_mode':'on_error',
            'helper_text':'Il campo è obbligatorio'
        }
        MainApp.nav.add_widget(self._create_nav_drower())
        #Main screen
        MainApp.sm.add_widget(Lists().build())

        MainApp.sm.add_widget(Preferences().build())

        MainApp.sm.add_widget(Loading_screen().build())

        MainApp.sm.add_widget(Info_screen())

        return MainApp._root

    def _create_nav_drower(self):
        sv = ScrollView()
        lst = MDList()

        from GUI.Widget import Add_Dialog
        items = [
            OneLineListItem(text='Crea una nuova lista', 
                on_release= lambda *args: [
                    App.nav.set_state('close'), 
                    self._change_screen(Add_Dialog().wait, 'preferences',**MainApp.new_list_dialog)]),
            OneLineListItem(text='Credit',
                on_release=lambda *args: [
                    App.nav.set_state('close'),
                    self.change_screen(None, 'credit')
                ])
            ]

        for i in items:
            lst.add_widget(i)
        
        sv.add_widget(lst)
        return sv

    def _change_screen(self, function, screen, **kwargs):
        Thread(target=self.change_screen, args=(function,screen,),kwargs=kwargs, daemon=True).start()
        return

    def change_screen(self, function=None, screen='main', **kwargs):
        if callable(function):
            if not function(**kwargs):
                return
        self.sm.current = screen

    def save(self, *args):
        from kivy.utils import platform
        if not platform == 'ios':
            Window.close()
        #print(App.sm.get_screen('main').ids)
        if platform == 'ios':
            Window.close()

def run():
    from kivy.base import runTouchApp
    
    try:
        MainApp()._run_prepare()
        runTouchApp()
    except KeyboardInterrupt as e:
        pass

    MainApp().stop()
    exit(0)

if __name__ == '__main__':
    run()
