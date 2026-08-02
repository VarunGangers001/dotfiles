import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

CARD_PADDING = 24
CARD_SPACING = 16


class ObservationWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("Daedalus Observation")
        self.set_default_size(400, 360)

        root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=CARD_SPACING,
            margin_top=CARD_PADDING,
            margin_bottom=CARD_PADDING,
            margin_start=CARD_PADDING,
            margin_end=CARD_PADDING,
        )

        title = Gtk.Label(
            xalign=0
        )
        title.set_markup(
            "<span size='18000' weight='bold'>Today's Observation</span>"
        )

        preview = Gtk.Frame()
        preview.set_size_request(-1, 180)

        placeholder = Gtk.Label(label="ASCII Preview")
        preview.set_child(placeholder)

        object_name = Gtk.Label(xalign=0)
        object_name.set_markup("<b>Pillars of Creation</b>")

        source = Gtk.Label(
            label="NASA APOD",
            xalign=0
        )

        root.append(title)
        root.append(preview)
        root.append(object_name)
        root.append(source)

        self.set_child(root)
