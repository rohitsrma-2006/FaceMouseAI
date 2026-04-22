import os
import customtkinter as ctk

from config import *
from tracker import FaceTracker


class FaceMouseUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.tracking = False
        self.tracker = FaceTracker()

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        ctk.set_appearance_mode(THEME_MODE)
        ctk.set_default_color_theme(COLOR_THEME)

        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)

        icon_path = "assets/app.ico"

        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="FaceMouse AI",
            font=("Segoe UI", 28, "bold")
        )
        self.title_label.pack(pady=(25, 15))

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Stopped",
            font=("Segoe UI", 16)
        )
        self.status_label.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self,
            text="Start Tracking",
            width=220,
            height=45,
            command=self.start_tracking
        )
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(
            self,
            text="Stop Tracking",
            width=220,
            height=45,
            fg_color="#8B0000",
            hover_color="#A00000",
            command=self.stop_tracking
        )
        self.stop_button.pack(pady=10)

        self.slider_label = ctk.CTkLabel(
            self,
            text="Sensitivity",
            font=("Segoe UI", 16)
        )
        self.slider_label.pack(pady=(25, 5))

        self.slider = ctk.CTkSlider(
            self,
            from_=0.5,
            to=4.0,
            number_of_steps=35,
            command=self.update_slider
        )
        self.slider.set(SENSITIVITY)
        self.slider.pack(fill="x", padx=40)

        self.slider_value = ctk.CTkLabel(
            self,
            text=f"{SENSITIVITY:.1f}",
            font=("Segoe UI", 14)
        )
        self.slider_value.pack(pady=8)

        self.footer_label = ctk.CTkLabel(
            self,
            text="AI Webcam Mouse Controller",
            font=("Segoe UI", 12)
        )
        self.footer_label.pack(side="bottom", pady=15)

    def update_slider(self, value):
        self.slider_value.configure(text=f"{value:.1f}")

    def start_tracking(self):
        if not self.tracking:
            self.tracking = True
            self.status_label.configure(text="Status: Running")
            self.tracker.start()

    def stop_tracking(self):
        if self.tracking:
            self.tracking = False
            self.status_label.configure(text="Status: Stopped")
            self.tracker.stop()