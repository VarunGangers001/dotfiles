from datetime import datetime
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk

from favourites import is_favourite, save_favourite
from preferences import (
    get_selected_provider,
    set_selected_provider,
)
from providers.registry import DISPLAY_NAMES, PROVIDERS
from source_manager import load_provider


DEFAULT_PROVIDER = "nasa"

PROVIDER_LABELS = {
    "nasa": "NASA",
    "hubble": "HUBBLE",
    "webb": "WEBB",
}


class ObservationWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application):
        super().__init__(application=app)

        saved_provider = get_selected_provider()

        self.current_provider = (
            saved_provider
            if saved_provider in PROVIDERS
            else DEFAULT_PROVIDER
        )

        self.current_metadata: dict = {}
        self.current_render_path: Path | None = None
        self.current_full_image: Path | None = None
        self.current_page_url = ""

        self.provider_buttons: dict[str, Gtk.Button] = {}

        self.set_title("Daedalus Observation v2")
        self.set_default_size(690, 540)
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
        root.append(self._build_provider_controls())

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

        self.source_label = Gtk.Label(xalign=0.5)
        self.source_label.set_hexpand(True)
        self.source_label.set_justify(Gtk.Justification.CENTER)
        self.source_label.add_css_class("observation-source")

        metadata_box.append(self.title_label)
        metadata_box.append(self.date_label)
        metadata_box.append(self.source_label)

        actions = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
            halign=Gtk.Align.CENTER,
        )
        actions.add_css_class("observation-actions")

        self.favourite_button = Gtk.Button(
            label="★ Favourite"
        )
        self.favourite_button.add_css_class("action-button")
        self.favourite_button.connect(
            "clicked",
            self._save_current_favourite,
        )

        source_button = Gtk.Button(
            label="Open Source Page"
        )
        source_button.add_css_class("action-button")
        source_button.connect(
            "clicked",
            self._open_source_page,
        )

        actions.append(self.favourite_button)
        actions.append(source_button)

        root.append(self.preview_button)
        root.append(metadata_box)
        root.append(actions)

        self.set_child(root)

        self._load_provider(self.current_provider)

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

    def _build_provider_controls(self) -> Gtk.Widget:
        controls = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
            halign=Gtk.Align.CENTER,
        )
        controls.add_css_class("provider-controls")

        for provider_id in ("nasa", "hubble", "webb"):
            if provider_id not in PROVIDERS:
                continue

            button = Gtk.Button(
                label=PROVIDER_LABELS[provider_id]
            )
            button.add_css_class("provider-button")
            button.set_tooltip_text(
                DISPLAY_NAMES[provider_id]
            )

            button.connect(
                "clicked",
                self._on_provider_clicked,
                provider_id,
            )

            self.provider_buttons[provider_id] = button
            controls.append(button)

        return controls

    def _on_provider_clicked(
        self,
        _button: Gtk.Button,
        provider_id: str,
    ) -> None:
        self._load_provider(provider_id)

    def _load_provider(
        self,
        provider_id: str,
    ) -> None:
        try:
            metadata, render_path, full_image_path = (
                load_provider(provider_id)
            )

            self.render_label.set_text(
                render_path.read_text(encoding="utf-8")
            )

            self.title_label.set_text(
                metadata.get(
                    "title",
                    "Untitled Observation",
                )
            )

            self.date_label.set_text(
                self._format_date(
                    metadata.get("date", "")
                )
            )

            self.source_label.set_text(
                metadata.get(
                    "source_name",
                    DISPLAY_NAMES.get(
                        provider_id,
                        provider_id,
                    ),
                )
            )

            self.current_provider = provider_id
            self.current_metadata = metadata
            self.current_render_path = render_path
            self.current_full_image = full_image_path
            self.current_page_url = metadata.get(
                "page_url",
                "",
            )

            set_selected_provider(provider_id)

            self._update_active_provider()
            self._update_favourite_button()

        except (RuntimeError, ValueError, OSError) as error:
            self.render_label.set_text(
                f"Unable to load {provider_id}:\n{error}"
            )
            self.title_label.set_text(
                "Observation unavailable"
            )
            self.date_label.set_text("")
            self.source_label.set_text(
                DISPLAY_NAMES.get(
                    provider_id,
                    provider_id,
                )
            )

    def _update_active_provider(self) -> None:
        for provider_id, button in (
            self.provider_buttons.items()
        ):
            button.remove_css_class("active")

            if provider_id == self.current_provider:
                button.add_css_class("active")

    def _update_favourite_button(self) -> None:
        if (
            self.current_metadata
            and is_favourite(
    self.current_metadata,
    self.current_full_image,
)
        ):
            self.favourite_button.set_label("★ Saved")
            self.favourite_button.set_sensitive(False)
        else:
            self.favourite_button.set_label("★ Favourite")
            self.favourite_button.set_sensitive(True)

    @staticmethod
    def _format_date(raw_date: str) -> str:
        if not raw_date:
            return "Latest available release"

        try:
            parsed = datetime.strptime(
                raw_date[:10],
                "%Y-%m-%d",
            )
            return parsed.strftime("%-d %B %Y")
        except ValueError:
            return raw_date

    def _open_full_image(
        self,
        _button: Gtk.Button,
    ) -> None:
        if (
            self.current_full_image is None
            or not self.current_full_image.exists()
        ):
            return

        Gio.AppInfo.launch_default_for_uri(
            self.current_full_image.as_uri(),
            None,
        )

    def _open_source_page(
        self,
        _button: Gtk.Button,
    ) -> None:
        if not self.current_page_url:
            return

        Gio.AppInfo.launch_default_for_uri(
            self.current_page_url,
            None,
        )

    def _save_current_favourite(
        self,
        _button: Gtk.Button,
    ) -> None:
        if (
            not self.current_metadata
            or self.current_full_image is None
            or self.current_render_path is None
        ):
            return

        try:
            save_favourite(
                metadata=self.current_metadata,
                full_image=self.current_full_image,
                render_path=self.current_render_path,
            )
            self._update_favourite_button()

        except (RuntimeError, OSError) as error:
            self.favourite_button.set_label(
                f"Save failed: {error}"
            )
