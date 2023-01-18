from typing import Union
from .__types__ import _App

from kivy.event import EventDispatcher
from kivy.properties import DictProperty


class _SmartDataStore(EventDispatcher):

    data = DictProperty()
    days_vol = DictProperty()
    list = DictProperty()

    def __init__(self, listname: Union[None, str] = None) -> None:
        super().__init__()

        self.register_event_type("on_data_update")
        self.register_event_type("on_update")

        if listname:
            raw = _App().data["lists"][listname]
            self.days = raw["days"]
            self.days_vol = raw["days_vol"]
            self.list = raw["list"]

    def on_data_update(self, newdata, *args, **kwargs):

        self.days = newdata["days"]
        self.days_vol = newdata["days_vol"]
        self.list = newdata["list"]

        self.dispatch("on_update", self)

    def on_update(self, *args, **kwargs):
        pass


DataStore = _SmartDataStore
