import json
from datetime import datetime

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk

from cache import FULL_IMAGE_PATH, METADATA_PATH
from renderer import render_observation


class ObservationWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application):
        super().__init__(application=app)

        self.set_title("Daedalus Observation")
        self.set_default_size(690, 455)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_hide_on_close(True)

        self.add_css_class("observation-window")

        root = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=7,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10,
        )
        root.add_css_class("observation-root")

        root.append(self._build_header())

        self.render_label = Gtk.Label()
        self.render_label.set_xalign(0.5)
        self.render_label.set_yalign(0.5)
        self.render_label.set_selectable(False)
        self.render_label.add_css_class("observation-art")

        self.preview_button = Gtk.Button()
        self.preview_button.set_hexpand(True)
        self.preview_button.set_child(self.render_label)
        self.preview_button.add_css_class("preview-card")
        self.preview_button.set_tooltip_text(
            "Open the full-resolution observation"
        )
        self.preview_button.connect(
            "clicked",
            self._open_full_image,
        )

        metadata_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=1,
            margin_top=1,
        )
        metadata_box.add_css_class("metadata-box")

        self.title_label = Gtk.Label(xalign=0.5)
        self.title_label.set_hexpand(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)
        self.title_label.set_wrap(True)
        self.title_label.add_css_class("observation-title")

        self.date_label = Gtk.Label(xalign=0.5)
        self.date_label.set_hexpand(True)
        self.date_label.set_justify(Gtk.Justification.CENTER)
        self.date_label.add_css_class("observation-date")

        self.source_label = Gtk.Label(
            label="NASA Astronomy Picture of the Day",
            xalign=0.5,
        )
        self.source_label.set_hexpand(True)
        self.source_label.set_justify(Gtk.Justification.CENTER)
        self.source_label.add_css_class("observation-source")

        metadata_box.append(self.title_label)
        metadata_box.append(self.date_label)
        metadata_box.append(self.source_label)

        root.append(self.preview_button)
        root.append(metadata_box)

        self.set_child(root)

        self._load_metadata()
        self._load_render()

    def _build_header(self) -> Gtk.Widget:
        header = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        header.add_css_class("observation-header")

        title = Gtk.Label(
            label="✦  Observation",
            xalign=0,
        )
        title.set_hexpand(True)
        title.add_css_class("header-title")

        mode = Gtk.Label(label="Engraved")
        mode.add_css_class("renderer-name")

        close_button = Gtk.Button(label="×")
        close_button.add_css_class("close-button")
        close_button.set_tooltip_text("Hide Observation")
        close_button.connect(
            "clicked",
            lambda _button: self.hide(),
        )

        header.append(title)
        header.append(mode)
        header.append(close_button)

        return header

    def _load_render(self) -> None:
        try:
            render_path = render_observation("engraved")
            render_text = render_path.read_text(
                encoding="utf-8"
            )
            self.render_label.set_text(render_text)

        except (RuntimeError, ValueError, OSError) as error:
            self.render_label.set_text(
                f"Unable to render observation:\n{error}"
            )

    def _load_metadata(self) -> None:
        if not METADATA_PATH.exists():
            self.title_label.set_text(
                "Observation metadata unavailable"
            )
            self.date_label.set_text("")
            return

        try:
            metadata = json.loads(
                METADATA_PATH.read_text(
                    encoding="utf-8"
                )
            )
        except (OSError, json.JSONDecodeError):
            self.title_label.set_text(
                "Observation metadata could not be read"
            )
            self.date_label.set_text("")
            return

        title = metadata.get(
            "title",
            "Untitled Observation",
        )
        raw_date = metadata.get("date", "")

        self.title_label.set_text(title)
        self.date_label.set_text(
            self._format_date(raw_date)
        )

    @staticmethod
    def _format_date(raw_date: str) -> str:
        if not raw_date:
            return ""

        try:
            parsed = datetime.strptime(
                raw_date,
                "%Y-%m-%d",
            )
            return parsed.strftime("%-d %B %Y")
        except ValueError:
            return raw_date

    def _open_full_image(
        self,
        _button: Gtk.Button,
    ) -> None:
        if not FULL_IMAGE_PATH.exists():
            self.render_label.set_text(
                "The full-resolution image is unavailable."
            )
            return

        try:
            Gio.AppInfo.launch_default_for_uri(
                FULL_IMAGE_PATH.as_uri(),
                None,
            )
        except Exception as error:
            self.render_label.set_text(
                f"Unable to open the full image:\n{error}"
            )
