import json, os
import sys
from threading import Thread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDFillRoundFlatButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from Widgets import pakedWidget


class App(MDApp):
    def build(self):
        self.title = 'Interrogazioni'
        self.theme_cls = ThemeManager()
        Window.bind(on_request_close=self.save)
        Window.bind(on_resize=lambda *args: Lists()._refresh())

        #initiallizing root variables
        App._root = MDNavigationLayout()
        App.sm = ScreenManager(transition=SlideTransition())
        App.nav = MDNavigationDrawer()

        App._root.add_widget(App.sm)
        App._root.add_widget(App.nav)

        App.new_list_dialog = {
            'title':'Nomina la nuova lista.',
            'l_text':'Inserisci il nome della nuova lista per modificarla in futuro.',
            't_text':'Nome:',
            'required':True,
            'helper_text_mode':'on_error',
            'helper_text':'Il campo è obbligatorio'
        }
        App.nav.add_widget(self._create_nav_drower())
        #Main screen
        App.sm.add_widget(Lists().build())

        App.sm.add_widget(Preferences().build())

        App.sm.add_widget(Loading_screen().build())

        App.sm.add_widget(Info_screen().build())

        return App._root

    def _create_nav_drower(self):
        sv = ScrollView()
        lst = MDList()

        from Widgets import Add_Dialog
        items = [
            OneLineListItem(text='Crea una nuova lista', 
                on_release= lambda *args: [
                    App.nav.set_state('close'), 
                    Lists()._change_screen(Add_Dialog().wait, 'preferences',**App.new_list_dialog)]),
            OneLineListItem(text='Credit',
                on_release=lambda *args: [
                    App.nav.set_state('close'),
                    Lists().change_screen(None, 'credit')
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

class Show_List(App):
    def dispatch(self, card: MDCard):
        App.sm.transition = NoTransition()
        App.sm.current = 'loading'
        App.sm.transition = SlideTransition()
        self.title = card.ids[list(card.ids.keys())[0]].text
        exec('if not hasattr(self, \'%s\'):\n\tself.%s = List_obj()\ntry:\n\tif self.working != self.%s:\n\t\tself.working=self.%s\nexcept AttributeError:\n\tself.working=self.%s'.replace('%s', self.title))
        self.working.data = App.data['lists'][self.title]
        self._update()
        if self._load_data():
            App.sm.current = self.title

    def _load_data(self):
        try:
            self.days = self.working.data['list'].keys()
        except KeyError as e:
            dlg = MDDialog(title='I dati della lista sembrano essere corrotti', 
            text='I dati della lista selezionata potrebbereo essere corrotti in quanto non è stata torvata la chiave {} (KeyError: {})'.format(e,e))
            dlg.open()
            dlg.bind(on_dismiss=lambda *args: Lists().change_screen())
            return False
        for i in self.days:
            if len(i.split('/')) < 3:
                self.year = self.working.calendar.active_date[2]
            else:
                self.year = int(i.split('/')[2])

            if len(i.split('/')) < 2:
                self.month = self.working.calendar.active_date[1]
            else:
                self.month = int(i.split('/')[1])
                
            if len(i.split('/')) == 0:
                raise SyntaxError()
            else:
                self.day = int(i.split('/')[0])
            self._create_costum_button_layout('/'.join([str(self.day), str(self.month), str(self.year)]), i)

        if hasattr(self, '_costum_buttons'):
            self.working.calendar.costum_buttons = self._costum_buttons
            self.working.calendar.reset_widget()
        return True

    def _create_costum_button_layout(self, day_formatted: str, data_index: str):
        if not hasattr(self, '_costum_buttons'):
            self._costum_buttons = {}
        box = MDBoxLayout(orientation='vertical')
        #box.md_bg_color = (0, 1, 0, 1)
        lbl = MDLabel(text=day_formatted.split('/')[0] + '\n{} +\n{} altri'.format(self.working.data['list'][data_index][0], len(self.working.data['list'][data_index])-1), 
                halign='center', font_style='Body1')
        lbl.pos_hint = {'center_x': .5, 'center_y': .5}
        box.add_widget(lbl)
        self._costum_buttons[day_formatted] = box

    def _load_screen(self):
        if not hasattr(self.working, 'screen'):
            self.working.screen = Screen(name = self.title)

    def _update(self):
        from Widgets import Calendar
        self._load_screen()
        self.working.calendar = Calendar(event_handler=self._update_screen)
        self.working.box = BoxLayout(orientation = 'vertical')
        self.working.toolbar = pakedWidget().toolbar('%s'%self.title, lambda *args: Lists().change_screen())
        self.working.toolbar.right_action_items = [['calendar', lambda *args: self._show_calendar()]]
        self.working.box.add_widget(self.working.toolbar)
        fl = FloatLayout()
        self.working.day_num = MDLabel(text = str(self.working.calendar.active_date[0]), font_style = 'H2')
        self.working.day_num.pos_hint = {'center_x':.52, 'center_y':.93}
        fl.add_widget(self.working.day_num)
        self.working.box.add_widget(fl)
        self.working.screen.add_widget(self.working.box)
        self.working.update()

    def _show_calendar(self):
        try:
            Show_List.dlg.open()
        except AttributeError:
            Show_List.dlg = Popup(
                title='Seleziona un giorno',
                content=self.working.calendar
                )
            Show_List.dlg.open()

    def _update_screen(self, *args):
        Show_List.dlg.dismiss()
        self.working.day_num.text = str(args[1][0])
        self.working.update()

class Lists(App):
    def build(self, only_cards=False):
        from Widgets import pakedWidget
        if not only_cards:
            main = Screen(name='main')
            box = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar('Interrogazioni', lambda *args: App.nav.set_state('open'))
            box.add_widget(tb)
        App.data = json.load(open(os.path.join(os.getcwd(),"Data.json")))
        vbox = pakedWidget().gridlayout(cols=1, size_hint_y=None)
        for lst in App.data["lists"]:
            lst_card = pakedWidget().card(orientation='horizontal', size=(Window.size[0]-40, 100))
            lbl = MDLabel(text=lst)
            lst_card.ids[lst] = lbl
            lst_card.add_widget(lbl)
            trash = MDFloatingActionButton(icon='trash-can')
            trash.icon_size='34sp'
            trash.md_bg_color = (1, 0, 0, 1)
            trash.pos_hint = {'center_x':.82, 'center_y':.5}
            trash.bind(on_release=lambda *args: self._deleate(args[0], confirm=True))
            lst_card.add_widget(trash)
            lst_card.bind(on_release = lambda *args: Show_List().dispatch(args[0]))
            vbox.add_widget(lst_card)

        vbox.bind(minimum_height=vbox.setter('height'))
        if only_cards:
            cards = vbox.children.copy()
            vbox.clear_widgets()
            return cards
        sv = pakedWidget().scrollview()
        sv.add_widget(vbox)
        box.add_widget(sv)

        btn = MDFloatingActionButton(icon='plus')
        btn.icon_size='34sp'
        btn.pos_hint={'center_x':.93, 'center_y':.2}
        from Widgets import Add_Dialog
        btn.bind(on_release=lambda *args: Lists()._change_screen(Add_Dialog().wait, 'preferences',**App.new_list_dialog))
        box.add_widget(btn)
        main.add_widget(box)
        main.ids['main_box'] = box
        main.ids['toolbar'] = tb
        main.ids['list_box'] = vbox
        return main

    def _refresh(self):
        box = App.sm.get_screen('main').ids['list_box']
        box.clear_widgets()
        for i in self.build(True):
            box.add_widget(i)
    
    def _deleate(self, *args, confirm=False):
        if confirm and (len(args) > 1):
            Lists.proceed = 0
            Lists.dlg = MDDialog(
                title='Sei sicuro?', 
                text='Vuoi davvero eliminare la lista {}?\nTutti i dati andranno persi se procedi!'.format(args[0].parent.ids[list(args[0].parent.ids.keys())[0]].text),
                buttons = [
                    MDFlatButton(text='ANNULLA', on_release=lambda *args: self._close_hanle()), 
                    MDFlatButton(text='CONTINUA', theme_text_color="Custom", text_color = (1,0,0,1), on_release=lambda *args: self._close())
                    ]
            )
            Lists.dlg.open()
            if not self._wait():
                return
        elif confirm:
            Thread(target=self._deleate, args=(args[0], True), kwargs={'confirm':True}, daemon=True).start()
            return
        
        App.sm.get_screen('main').ids['list_box'].remove_widget(args[0].parent)

    def _wait(self, *args, **kwargs):
        import time
        while Lists.proceed == 0:
            time.sleep(0.2)
        if Lists.proceed == 1:
            return True
        elif Lists.proceed == 2:
            return False

    def _close(self):
        Lists.proceed = 1
        Lists.dlg.dismiss()

    def _close_hanle(self):
        Lists.proceed = 2
        Lists.dlg.dismiss()

class Loading_screen:
    def build(self):
        ls = Screen(name='loading')
        from kivymd.uix.spinner import MDSpinner
        from kivy.metrics import dp
        box = FloatLayout()
        lbl = MDLabel(text='Caricamento...', halign='center')
        lbl.pos_hint = {'center_x':.5, 'center_y':.55}
        box.add_widget(lbl)
        box.add_widget(MDSpinner(
                            size_hint=(None, None),
                            size=(dp(46), dp(46)),
                            pos_hint={'center_x': .5, 'center_y': .45},
                            active=True,
                            palette=[
                                [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                                [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                                [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                                [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                            ]
                        ))
        ls.add_widget(box)
        return ls

class Preferences(App):
    def build(self):
        preferences = Screen(name = 'preferences')
        from Widgets import pakedWidget
        box = pakedWidget().boxlayout()
        from Widgets import Menu
        m_args = {}
        tb = pakedWidget().toolbar('Preferenze', lambda *args: Menu().open(**m_args))
        box.add_widget(tb)
        layout = FloatLayout()
        btn = MDFlatButton(text = 'Aggiungi un volontario', on_release = lambda *args: self.vol_dialog())
        layout.add_widget(btn)
        box.add_widget(layout)
        preferences.add_widget(box)
        return preferences

    def vol_dialog(self, *args):
        from Widgets import Add_Dialog
        d_args = {
            'title':'Inserisci i dati del volontario',
            't_txt':'Name',
            'required':True,
            'helper_text_mode':'on_error',
            'helper_text':'Il campo è obbligatorio'
        }
        Add_Dialog().open(**d_args)

class List_obj(object):
    
    def _globalize(self):
        for i in self.screen.children:
            tp = str(type(i)).split('\'')[1].split('.')[-1]
            exec('if not hasattr(self, \'self.%s.widget\'):\n\tself.%s = List_obj()\n\tself.%s.widget = List_obj()'.replace('%s', self.screen.name))
            exec('self.{}.widget.{} = i'.format(self.screen.name, tp))

    def update(self, change=False):
        self._globalize()
        try:
            if not App.sm.has_screen(self.screen.name):
                App.sm.add_widget(self.screen)
            scr = App.sm.get_screen(self.screen.name)
            if scr != self.screen:
                self.screen.clear_widgets()
            scr.clear_widgets()
            exec('for i in self.%s.widget:\n\texec(\'scr.add_widget(self.%s.widget.wdg)\'.replace(\'wdg\',i))'.replace('%s', self.screen.name))
            self.screen = scr
            if change:
                App.sm.current = self.screen.name
        except AttributeError:
            return

    def __iter__(self):
        self.methods = dir(self)
        for i in self.methods:
            if (i.startswith('_') or i.startswith('__')):
                self.methods.remove(i)
        return self
    
    def __next__(self):
        if not len(self.methods) == 0:
            while True:
                try:
                    if not ('_' in self.methods[0] or 'update' in self.methods[0]):
                        return self.methods.pop(0)
                    else:
                        self.methods.pop(0)
                except Exception as e:
                    raise StopIteration
        raise StopIteration

class Info_screen:
    from kivy.utils import platform
    import kivy
    description = '''
Authors: Davide Berardi & Filippo Bollito
Powered by python and kivy
Platform: {}
Python version: {}
Kivy version: {}

Licence: MIT License

Copyright (c) 2021 Davide255

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''.format(platform, sys.version, kivy.version)

    def build(self):
        scr = Screen(name='credit')
        sv = pakedWidget().scrollview()
        bx = pakedWidget().boxlayout()
        lbl = MDLabel(text=self.description, font_style='Body2', halign='center')
        lbl.size_hint = None, None
        #lbl.size = App.
        bx.add_widget(lbl)
        btn = MDFillRoundFlatButton(text='esci', on_release=lambda *args: Lists().change_screen(), pos_hint={'center_x':.5})
        bx.add_widget(btn)
        bx.bind(minimum_height=bx.setter('height'))
        sv.add_widget(bx)
        scr.add_widget(sv)
        return scr

try:
    from kivy.base import runTouchApp
    App()._run_prepare()
    runTouchApp()
    App().stop()
except KeyboardInterrupt as e:
    exit(0)
