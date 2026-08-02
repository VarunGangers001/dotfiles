import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ui import ObservationWindow
from style import load_css


class ObservationApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.daedalus.observation")

    def do_activate(self):
        load_css()
        ObservationWindow(self).present()


app = ObservationApp()
app.run()
