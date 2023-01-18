'''Definition of App pages'''

# Core
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.event import EventDispatcher

# Widget
from kivy.uix.screenmanager import Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFloatingActionButton
from .Widgets import Calendar

# Type helper
from ..Data import DataStore
from ..Data.__types__ import _App, _DataStore

class DataList(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        App = MDApp.get_running_app()

        self.data = App.data

        gl = GridLayout(**kwargs)
        gl.size_hint_max_y = None

        gl.cols = 1
        gl.size_hint_y = None
        gl.padding = '20dp'
        gl.spacing = '20dp'

        for lst in App.data["lists"]:
            card = MDCard(orientation='horizontal')
            card.padding = '8dp'
            card.size_hint = None, None
            card.size = (Window.size[0]-40, 100)
            card.elevation = 3
            card.border_radius = 20
            card.radius = [15]

            lbl = MDLabel(text=lst)
            card.add_widget(lbl)

            trash = MDFloatingActionButton(icon='trash-can')
            trash.icon_size='34sp'
            trash.md_bg_color = (1, 0, 0, 1)
            trash.pos_hint = {'center_x':.82, 'center_y':.5}
            #trash.bind(on_release=lambda *args: self._deleate(args[0], confirm=True))
            card.add_widget(trash)
            
            card.bind(on_release = lambda *args: ListPage(args[0]))

            gl.add_widget(card)

        gl.bind(minimum_height=gl.setter('height'))
        
        sv = ScrollView(do_scroll_x = False, do_scroll_y = True)
        sv.add_widget(gl)

        self.add_widget(sv)


class Main(Screen):
    ''' Main screen '''

    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = 'main'

        box = BoxLayout(orientation='vertical')

        appbar = MDTopAppBar(title='InterrogationPlanner')
        appbar.left_action_items = [['menu', lambda *args: MDApp.get_running_app().nav.set_state('open')]]
        
        box.add_widget(appbar)

        box.add_widget(DataList())

        self.add_widget(box)

class ListPage(EventDispatcher):

    name: str = None
    data: DataStore = None

    def __init__(self, listcard: MDCard):
        self.create(listcard)

        _App().sm.current = self.name

    def create(self, listcard: MDCard) -> Screen:
        App = _App()

        # Set loading screen
        App.sm.transition = NoTransition()
        App.sm.current = 'loading'
        App.sm.transition = SlideTransition()
        self.name = listcard.children[1].text

        # Load data
        self.data: _DataStore = DataStore(self.name)
        self.data.bind(on_update=self.update)

        if not App.sm.has_screen(self.name):
            working = Screen(name = self.name)
            working.add_widget(self.build_screen())
            App.sm.add_widget(working)
        else: working = App.sm.get_screen(self.name)

        return working

    def update(self, instance):
        screen: Screen = _App().sm.get_screen(self.name)
        screen.clear_widgets()
        screen.add_widget(self.build_screen())

    def build_screen(self) -> BoxLayout:
        
        box = BoxLayout(orientation = 'vertical')

        toolbar = MDTopAppBar(title = self.name)
        box.add_widget(toolbar)

        def calendar_callback(self: ListPage, *args):
            pass

        floatlayout = FloatLayout()

        calendar = Calendar(event_handler = calendar_callback)

        daynumber = MDLabel(text = str(calendar.active_date[0]), font_style = 'H2')
        daynumber.pos_hint = {'center_x':.52, 'center_y':.93}

        floatlayout.add_widget(daynumber)

        box.add_widget(floatlayout)

        return box


class Loading(Screen):
    ''' Loading screen '''

    def __init__(self, **kw):
        super().__init__(**kw)

        self.name = 'loading'

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

        self.add_widget(box)
