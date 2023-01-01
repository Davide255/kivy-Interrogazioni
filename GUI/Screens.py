# system libraries
import sys, json, os
from typing import Union
from GUI.Widget import pakedWidget
from threading import Thread
# kivy widgets libraries
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDFillRoundFlatButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
# functional libraries
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.clock import mainthread

# This is only to improve the readability of the code
from GUI.types import _App, List_obj

# Get the running app and create a macro
App = _App()

class Info_screen(Screen):
    ''' Credit screen '''

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

    def build(self) -> Screen:
        scr = Screen(name='credit')
        sv = pakedWidget().scrollview()
        bx = pakedWidget().boxlayout()
        lbl = MDLabel(text=self.description, font_style='Body2', halign='center')
        lbl.size_hint = None, None
        #lbl.size = App.
        bx.add_widget(lbl)
        btn = MDFillRoundFlatButton(text='esci', on_release=lambda *args: App.change_screen(), pos_hint={'center_x':.5})
        bx.add_widget(btn)
        bx.bind(minimum_height=bx.setter('height'))
        sv.add_widget(bx)
        scr.add_widget(sv)
        return scr

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.name='credit'

        sv = pakedWidget().scrollview()
        bx = pakedWidget().boxlayout()
        lbl = MDLabel(text=self.description, font_style='Body2', halign='center')
        lbl.size_hint = None, None
        lbl.size_hint_x = Window.size[0]
        bx.add_widget(lbl)
        btn = MDFillRoundFlatButton(text='esci', on_release=lambda *args: App.change_screen(), pos_hint={'center_x':.5})
        bx.add_widget(btn)
        bx.bind(minimum_height=bx.setter('height'))
        sv.add_widget(bx)

        self.add_widget(sv)

class Lists(Screen):
    ''' Main screen of the app '''

    _state = 0

    def __init__(self, **kw):
        self.name = 'main'
        super().__init__(**kw)

    def return_cards(self):
        pass

    def build(self):
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
            lst_card.bind(on_release = lambda *args: ListShower().dispatch(args[0]))
            vbox.add_widget(lst_card)

        vbox.bind(minimum_height=vbox.setter('height'))
        
        sv = pakedWidget().scrollview()
        sv.add_widget(vbox)
        box.add_widget(sv)

        btn = MDFloatingActionButton(icon='plus')
        btn.icon_size='34sp'
        btn.pos_hint={'center_x':.93, 'center_y':.2}
        from GUI.Widget import Add_Dialog
        btn.bind(on_release=lambda *args: App._change_screen(Add_Dialog().wait, 'preferences', **App.new_list_dialog))
        box.add_widget(btn)
        self.add_widget(box)
        return self

    def _refresh(self):
        box = App.sm.get_screen('main').ids['list_box']
        box.clear_widgets()
        for i in self.build(True):
            box.add_widget(i)
    
    @mainthread
    def _deleate(self, widget: Widget, confirm=False):
        if confirm:
            self.dlg = MDDialog(
                title='Sei sicuro?', 
                text='Vuoi davvero eliminare la lista {}?\nTutti i dati andranno persi se procedi!'.format(widget.parent.children[1].text),
                buttons = [
                    MDFlatButton(text='ANNULLA', on_release=lambda *args: self._close_hanle()), 
                    MDFlatButton(text='CONTINUA', theme_text_color="Custom", text_color = (1,0,0,1), on_release=lambda *args: self._close())
                    ]
            )
            self.dlg.open()
            Thread(target=self._wait_dlg, args=(widget,), daemon=True).start()
            return


    def _wait_dlg(self, widget: Widget):
        while (Lists._state == 0):
            pass
        
        @mainthread
        def _remove_widget():
            widget.parent.parent.remove_widget(widget.parent)

        if Lists._state == 1:
            _remove_widget()
        
        Lists._state = 0

    def _close(self):
        Lists._state = 1
        self.dlg.dismiss()

    def _close_hanle(self):
        Lists._state = 2
        self.dlg.dismiss()

class Preferences:
    ''' ==== WORK IN PROGRESS ====
Preferences screen, this is used to insert students preferences'''

    def build(self):
        preferences = Screen(name = 'preferences')
        from GUI.Widget import pakedWidget
        box = pakedWidget().boxlayout()
        from GUI.Widget import Menu
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
        from GUI.Widget import Add_Dialog
        d_args = {
            'title':'Inserisci i dati del volontario',
            't_txt':'Name',
            'required':True,
            'helper_text_mode':'on_error',
            'helper_text':'Il campo è obbligatorio'
        }
        Add_Dialog().open(**d_args)

class List_obj(object):
    ''' Usefull object to organize the lists '''

    # name of the list
    name: str = None
    # readable only variable to indicate wether the list has a name or not
    allocated: bool = property(lambda self: True if self.name else False)
    # the app screen related at the list
    screen: Screen = None
    # fast access widgets
    widget: Union[List_obj, None] = None
    # here is stored the data of the list
    data: dict = None

    def __init__(self, name: str = '') -> None:
        if name: self.name = name
    
    def assing_widget(self, widget: Union[List_obj, None] = None) -> List_obj:
        ''' init the widget variable '''
        if widget: self.widget = widget
        else: self.widget = List_obj(self.name+' widgetlist')

        return self.widget

    # def _screen_setter(self, screen: Screen):
    #    self.screen = screen
    #    if not App.sm.has_screen(screen.name): 
    #        App.sm.add_widget(screen)
    
    #def _screen_getter(self) -> Screen:
    #    return self.screen

    #screen: Screen = property(fget=_screen_getter, fset=_screen_setter )

    def __repr__(self) -> str:
        if self.name: return 'List_obj: "{}"'.format(self.name)
        else: return 'Unallocated List_obj'

    def __iter__(self):
        ''' helper to iter among the fast widgets '''
        _widgets = list()
        for i in dir(self.widget):
            exec("_widgets.append(self.widget.{})".format(i))
        return _widgets

class ListShower:
    ''' This class is responsable of showing every list '''

    def dispatch(self, card: MDCard):

        ''' from a card retrive list name and develop the associated screen '''

        App: _App = MDApp.get_running_app()
        App.sm.transition = NoTransition()
        App.sm.current = 'loading'
        App.sm.transition = SlideTransition()
        self.title = card.children[1].text

        self.working: List_obj = None
    
        exec("""if not hasattr(self, '%s'):
    self.%s = List_obj('%s')
    if self.working != self.%s:
        self.working = self.%s""".replace('%s', self.title))
        
        self.working.assing_widget()
        self.working.data = App.data['lists'][self.title]

        self._update()
        if self._load_data():
            App.sm.current = self.title

    def _load_data(self):
        '''method to prepare the data and check the validity '''
        try:
            self.days = self.working.data['list'].keys()
        except KeyError as e:
            dlg = MDDialog(title='I dati della lista sembrano essere corrotti', 
            text='I dati della lista selezionata potrebbereo essere corrotti in quanto non è stata torvata la chiave {} (KeyError: {})'.format(e,e))
            dlg.open()
            dlg.bind(on_dismiss=lambda *args: App.change_screen())
            return False

        for i in self.days:

            if len(i.split('/')) < 3:
                self.year = self.working.widget.calendar.active_date[2]
            else:
                self.year = int(i.split('/')[2])

            if len(i.split('/')) < 2:
                self.month = self.working.widget.calendar.active_date[1]
            else:
                self.month = int(i.split('/')[1])
                
            if len(i.split('/')) == 0:
                raise SyntaxError('Invalid data syntax')
            else:
                self.day = int(i.split('/')[0])
            self._create_costum_button_layout('/'.join([str(self.day), str(self.month), str(self.year)]), i)

        if hasattr(self, '_costum_buttons'):
            self.working.widget.calendar.costum_buttons = self._costum_buttons
            self.working.widget.calendar.reset_widget()
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
        ''' make sure that the screen exist and it's aviable '''
        App: _App = MDApp.get_running_app()
        if not self.working.screen: 
            self.working.screen = Screen(name = self.title)
            App.sm.add_widget(self.working.screen)

    def _update(self):
        ''' build the screen it self '''
        from GUI.calendar_widget.calendar_ui import Calendar
        self._load_screen()
        self.working.widget.calendar = Calendar(event_handler=self._update_screen)
        self.working.widget.box = BoxLayout(orientation = 'vertical')
        self.working.widget.toolbar = pakedWidget().toolbar('%s'%self.title, lambda *args: App.change_screen())
        self.working.widget.toolbar.right_action_items = [['calendar', lambda *args: self._show_calendar()]]
        self.working.widget.box.add_widget(self.working.widget.toolbar)
        fl = FloatLayout()
        self.working.widget.day_num = MDLabel(text = str(self.working.widget.calendar.active_date[0]), font_style = 'H2')
        self.working.widget.day_num.pos_hint = {'center_x':.52, 'center_y':.93}
        fl.add_widget(self.working.widget.day_num)
        self.working.widget.box.add_widget(fl)
        self.working.screen.add_widget(self.working.widget.box)

    def _show_calendar(self):
        ''' show the calendar '''
        try:
            ListShower.dlg.open()
        except AttributeError:
            ListShower.dlg = Popup(
                title='Seleziona un giorno',
                content=self.working.widget.calendar
                )
            ListShower.dlg.open()

    def _update_screen(self, *args):
        ListShower.dlg.dismiss()
        self.working.widget.day_num.text = str(args[1][0])

class Loading_screen:
    ''' loading screen '''

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
