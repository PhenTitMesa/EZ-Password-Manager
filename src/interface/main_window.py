"""
Main Window - The primary application window.

This module provides:
- Main application window that hosts the dashboard
- Navigation bar with title, version, and UI size selector
- Integration with login system
- Proper window lifecycle management

This is the entry point for the application's UI after successful login.
"""

import customtkinter as ctk
from src.storage.manager import PasswordManager
from src.interface.dashboard import DashboardWindow
from src.interface.add_password import AddPasswordWindow
from src import VERSION, APP_NAME

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# UI Size presets: (scaling_factor, window_width, window_height)
UI_SIZE_PRESETS = {
    "Default": (1.0, 900, 700),
    "Larger": (1.2, 1080, 840),
    "Largest": (1.4, 1260, 980),
}


class MainWindow(ctk.CTk):
    """
    Main application window that contains the dashboard.

    This window is shown after successful login and provides
    the main interface for managing passwords.
    """

    def __init__(self, manager: PasswordManager):
        """
        Initialize the main window.

        Args:
            manager: PasswordManager instance (already authenticated)
        """
        super().__init__()

        # Store the manager instance
        self.manager = manager

        # Configure window
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("900x700")
        self.resizable(True, True)  # Allow maximize and resize
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Try to set window icon (optional)
        try:
            self.iconbitmap("src/interface/assets/icon.png")
        except Exception:
            pass  # Icon not found - continue without it

        # Create the navigation bar (top section)
        self._create_navbar()

        # Create the dashboard (main content area)
        self._create_dashboard()

    def _create_navbar(self):
        """Create the top navigation bar with title, version, and UI size selector."""

        # Navbar frame
        navbar = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0, height=60)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)  # Maintain fixed height

        # App title
        title_label = ctk.CTkLabel(
            navbar, text=APP_NAME, font=("Arial", 22, "bold"), text_color="#FFFFFF"
        )
        title_label.pack(side="left", padx=20, pady=12)

        # Version badge
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

        # Logout button
        logout_btn = ctk.CTkButton(
            navbar,
            text="Logout",
            command=self._logout,
            width=90,
            height=32,
            font=("Arial", 11),
            fg_color="#555555",
            hover_color="#444444",
        )
        logout_btn.pack(side="right", padx=(0, 10), pady=12)

        # UI Size dropdown (left of logout button)
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
            button_hover_color="#153060",
            dropdown_fg_color="#2B2B2B",
            dropdown_hover_color="#3B3B3B",
        )
        size_dropdown.pack(side="right", padx=(0, 5), pady=12)

    def _create_dashboard(self):
        """Create the main dashboard area with password list."""

        # Create dashboard frame
        self.dashboard = DashboardWindow(self, self.manager)
        self.dashboard.pack(fill="both", expand=True)

        # Connect dashboard callbacks
        self.dashboard.on_add_password = self._open_add_password
        self.dashboard.on_edit_password = self._open_edit_password

    def _open_add_password(self):
        """Open the add password form."""
        AddPasswordWindow(
            self.manager,
            on_save_callback=self.dashboard.refresh_password_list,
            entry=None,  # No entry = add mode
        )

    def _open_edit_password(self, entry: dict):
        """
        Open the edit password form.

        Args:
            entry: The password entry to edit
        """
        AddPasswordWindow(
            self.manager,
            on_save_callback=self.dashboard.refresh_password_list,
            entry=entry,
        )

    def _logout(self):
        """Handle logout button click."""
        # Destroy this window
        self.destroy()

        # Restart the application (show login again)
        import main

        main.main()

    def _on_size_change(self, selected_size: str):
        """
        Handle UI size change from dropdown.

        Args:
            selected_size: The selected size preset (Default, Larger, Largest)
        """
        scaling, width, height = UI_SIZE_PRESETS[selected_size]

        # Apply the scaling factor
        ctk.set_widget_scaling(scaling)

        # Resize the window
        self.geometry(f"{width}x{height}")

    def _on_close(self):
        """Handle window close button - fully terminate the application."""
        self.destroy()
        self.quit()  # Stop the mainloop
        import sys

        sys.exit(0)  # Ensure all processes terminate


def main():
    """Entry point for the application."""
    # Create manager and show login
    manager = PasswordManager()

    # Check if master password is set
    if not manager.is_master_set():
        # First run - show setup window
        root = ctk.CTk()
        root.withdraw()  # Hide root window

        def on_login_success():
            root.deiconify()
            root.withdraw()
            app = MainWindow(manager)
            app.mainloop()

        from src.interface.login import LoginWindow

        login = LoginWindow(manager, on_login_success)
        root.mainloop()
    else:
        # Subsequent runs - show login
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
