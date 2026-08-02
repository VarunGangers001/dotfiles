from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk


def load_css():
    css = Gtk.CssProvider()

    css_path = (
        Path(__file__).resolve().parent.parent
        / "styles"
        / "daedalus.css"
    )

    css.load_from_path(str(css_path))

    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )
