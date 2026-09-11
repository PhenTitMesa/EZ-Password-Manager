# MainWindow - Main app window with navbar and dashboard

import customtkinter as ctk
from src.storage.manager import PasswordManager
from src.interface.dashboard import DashboardWindow
from src.interface.add_password import AddPasswordWindow
from src import VERSION, APP_NAME

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# UI Size presets: (scaling, width, height)
UI_SIZE_PRESETS = {
    "Default": (1.0, 900, 700),
    "Larger": (1.2, 1080, 840),
    "Largest": (1.4, 1260, 980),
}


class MainWindow(ctk.CTk):
    # Main app window shown after login

    def __init__(self, manager: PasswordManager):
        super().__init__()

        self.manager = manager

        # Window setup
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("900x700")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Try to set icon (optional)
        try:
            self.iconbitmap("src/interface/assets/icon.png")
        except Exception:
            pass

        self._create_navbar()
        self._create_dashboard()

    def _create_navbar(self):
        # Top navbar with title and UI size selector

        navbar = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0, height=60)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        # App title (left)
        title_label = ctk.CTkLabel(
            navbar, text=APP_NAME, font=("Arial", 22, "bold"), text_color="#FFFFFF"
        )
        title_label.pack(side="left", padx=20, pady=12)

        # UI Size dropdown (right side)
        size_label = ctk.CTkLabel(
            navbar, text="UI Size:", font=("Arial", 11), text_color="#AAAAAA"
        )
        size_label.pack(side="right", padx=(0, 5), pady=12)

        self.size_var = ctk.StringVar(value="Default")
        size_dropdown = ctk.CTkOptionMenu(
            navbar,
            variable=self.size_var,
            values=list(UI_SIZE_PRESETS.keys()),
            command=self._on_size_change,
            width=100,
            height=32,
            font=("Arial", 11),
            fg_color="#2B5EA7",
            button_color="#1E4080",
            dropdown_fg_color="#2B2B2B",
            dropdown_hover_color="#3B3B3B",
        )
        size_dropdown.pack(side="right", padx=(0, 5), pady=12)

        # Version badge (right)
        version_label = ctk.CTkLabel(
            navbar,
            text=f"v{VERSION}",
            font=("Arial", 10),
            text_color="#888888",
            fg_color="#2B2B2B",
            corner_radius=4,
            padx=8,
            pady=2,
        )
        version_label.pack(side="right", padx=20, pady=12)

    def _create_dashboard(self):
        # Main password list area
        self.dashboard = DashboardWindow(self, self.manager)
        self.dashboard.pack(fill="both", expand=True)

        # Connect callbacks for add/edit buttons
        self.dashboard.on_add_password = self._open_add_password
        self.dashboard.on_edit_password = self._open_edit_password

    def _open_add_password(self):
        # Open add password form
        AddPasswordWindow(
            self.manager,
            on_save_callback=self.dashboard.refresh_password_list,
            entry=None,
        )

    def _open_edit_password(self, entry: dict):
        # Open edit password form
        AddPasswordWindow(
            self.manager,
            on_save_callback=self.dashboard.refresh_password_list,
            entry=entry,
        )

    def _on_size_change(self, selected_size: str):
        # Change UI scaling
        scaling, width, height = UI_SIZE_PRESETS[selected_size]
        ctk.set_widget_scaling(scaling)
        self.geometry(f"{width}x{height}")

    def _on_close(self):
        # Terminate app completely
        self.destroy()
        self.quit()
        import sys

        sys.exit(0)


def main():
    # Alternate entry point (login -> main window)
    manager = PasswordManager()
    root = ctk.CTk()
    root.withdraw()

    def on_login_success():
        root.destroy()
        app = MainWindow(manager)
        app.mainloop()

    from src.interface.login import LoginWindow

    login = LoginWindow(manager, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    main()
