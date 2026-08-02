import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from style import load_css
from ui import ObservationWindow


class ObservationApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.daedalus.observation"
        )

        self.window: ObservationWindow | None = None

    def do_activate(self) -> None:
        if self.window is None:
            load_css()
            self.window = ObservationWindow(self)
            self.window.present()
            return

        if self.window.get_visible():
            self.window.hide()
        else:
            self.window.present()


app = ObservationApp()
app.run()
