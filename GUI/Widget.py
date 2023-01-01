from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel as Label
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar as MDToolbar
import time

class Day_Input:
    def open(self):
        box = BoxLayout(size_hint_y = None)
        Day_Input.txt_f = MDTextField(
            hint_text='Day', 
            required=True, 
            mode='fill', 
            helper_text_mode='on_error', 
            helper_text= "Il campo è obbligatorio",
            max_text_length=2
        )
        Day_Input.txt_f.pos_hint = {'center_x':.5, 'center_y':.7}
        box.add_widget(Day_Input.txt_f)

        Day_Input.dlg = MDDialog(
            title='Input a day',
            type='custom',
            content_cls=box,
            buttons = [MDFlatButton(text='salva', on_release=lambda *args: Day_Input()._close())],
            size_hint= [0.5, None],
            size_hint_y = .8,
        )

        Day_Input.dlg.bind(on_dismiss=lambda *args:Day_Input()._get_text())
        Day_Input.dlg.open()

    def _close(self, *args):
        Day_Input.dlg.dismiss()

    def _get_text(self, *args):
        print(Day_Input.txt_f.text)

class Add_Dialog:
    proc_end = int()

    def __init__(self) -> None:
        if Add_Dialog.proc_end != 0:
            Add_Dialog.proc_end = 0
   
    def open(self, *args, **kwargs):
        title = kwargs.get('title')
        l_text = kwargs.get('l_text')
        t_text = kwargs.get('t_text')
        required = kwargs.get('required')
        helper_text = kwargs.get('helper_text')
        helper_text_mode = kwargs.get('helper_text_mode')
        on_text_validate = kwargs.get('on_text_validate')
        content_cls = kwargs.get('content_cls')
        try:
            bx = BoxLayout(size_hint_y = None)
            l = FloatLayout()
            if l_text:
                lbl = Label(text='Inserisci il nome della lista che vuoi creare.', pos_hint={'center_x': .7, 'center_y':1})
                l.add_widget(lbl)
            if not t_text:
                t_text = ''
            if not helper_text:
                helper_text = ''
            if not helper_text_mode in ['on_focus','on_error', 'persistent']:
                helper_text_mode = 'none'
            else:
                helper_text_mode = 'none'
            Add_Dialog.txt_f = MDTextField(
                hint_text=t_text, 
                required=required, 
                mode='fill', 
                helper_text_mode=helper_text_mode, 
                helper_text=helper_text,
                pos_hint={'center_x':.5,'center_y':.4}
            )
            if not on_text_validate:
                on_text_validate = self._end_dialog
            else:
                on_text_validate = on_text_validate
            Add_Dialog.txt_f.bind(on_text_validate=lambda *args: on_text_validate())
            l.add_widget(Add_Dialog.txt_f)
            bx.add_widget(l)
            if content_cls:
                bx.add_widget(content_cls)

            Add_Dialog.dlg = MDDialog(
                title = title,
                type='custom',
                content_cls= bx,
                buttons = [MDFlatButton(text='Avanti', on_release=lambda *args: self._end_dialog())]
            )
            Add_Dialog.dlg.bind(on_pre_dismiss=self._close_handle)
            Add_Dialog.dlg.open()
        except IndexError as e:
            Add_Dialog.dlg = MDDialog(
                title='Error:',
                text=e,
                buttons = [MDFlatButton(text='OK', on_release=lambda *args: self._close())]
            )

    def wait(self, *args, **kwargs):
        try:
            Add_Dialog().open(**kwargs)
        except AttributeError:
            self.open()
        while Add_Dialog.proc_end == 0:
            time.sleep(0.2)
        if Add_Dialog.proc_end == 1:
            return True
        elif Add_Dialog.proc_end == 2:
            return False
    
    def _close_handle(self, *args):
        Add_Dialog.proc_end = 2

    def _end_dialog(self, *args):
        if Add_Dialog.txt_f.text != '':
            self._close()
        else:
            Add_Dialog.txt_f.error = True

    def _close(self, *args):
        Add_Dialog.dlg.dismiss()
        Add_Dialog.proc_end = 1

class Menu:
    def open(self, **kwargs):
        pass

#Classe di widget già formattati
class pakedWidget():
    def switch(self, **kwargs):
        sw = MDSwitch(**kwargs)
        if kwargs.get('pos_hint') == None:
            sw.pos_hint = {'center_x': .80, 'center_y': .3}
        return sw

    def card(self, **kwargs):
        mc = MDCard(**kwargs)
        if not kwargs.get('orientation'):
            mc.orientation = 'vertical'
        mc.padding = '8dp'
        mc.size_hint = None, None
        if kwargs.get('size') == None:
            mc.size = "240dp", "280dp"
        mc.elevation = 3
        mc.border_radius = 20
        mc.radius = [15]
        return mc

    def scrollview(self, **kwargs):
        sv = ScrollView(**kwargs)
        sv.do_scroll_x = False
        sv.do_scroll_y = True
        return sv

    def gridlayout(self, **kwargs):
        gl = GridLayout(**kwargs)
        gl.size_hint_max_y = None
        if kwargs.get('cols') == None:
            gl.cols = 3
        if kwargs.get('padding') == None:
            gl.padding = "20dp"
        if kwargs.get('spacing') == None:
            gl.spacing = "20dp"
        return gl

    def boxlayout(self, **kwargs):
        bl = BoxLayout(**kwargs)
        if not kwargs.get('orientation'):
            bl.orientation = 'vertical'
        return bl

    def toolbar(self, title, callback=None, **kwargs):
        tb = MDToolbar(**kwargs)
        tb.title = title
        if callback:
            tb.left_action_items = [['menu', lambda x: callback(x)]]
        return tb
