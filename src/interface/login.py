# LoginWindow - Master password setup and login screen

import customtkinter as ctk
from src.storage.manager import PasswordManager


class LoginWindow(ctk.CTkToplevel):
    # Login window for master password authentication

    def __init__(self, manager: PasswordManager, on_success_callback):
        super().__init__()

        self.manager = manager
        self.on_success = on_success_callback

        # Window setup
        self.title("Simple Password Manager - Login")
        self.geometry("400x350")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Make modal (blocks other windows)
        self.transient(self.master)
        self.grab_set()

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"400x350+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        # Main container
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Title (changes based on first run vs login)
        title_text = (
            "Set Master Password"
            if not self.manager.is_master_set()
            else "Enter Master Password"
        )
        self.title_label = ctk.CTkLabel(
            self.frame,
            text=title_text,
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF",
        )
        self.title_label.pack(pady=(0, 10))

        # Subtitle
        desc_text = (
            "Create a master password to secure your passwords"
            if not self.manager.is_master_set()
            else "Enter your master password to continue"
        )
        self.desc_label = ctk.CTkLabel(
            self.frame, text=desc_text, font=("Arial", 12), text_color="#888888"
        )
        self.desc_label.pack(pady=(0, 20))

        # Password field
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Master Password",
            show="●",
            width=300,
            height=40,
            font=("Arial", 14),
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", self._handle_submit)

        # Confirm field (first run only)
        self.confirm_entry = None
        if not self.manager.is_master_set():
            self.confirm_entry = ctk.CTkEntry(
                self.frame,
                placeholder_text="Confirm Master Password",
                show="●",
                width=300,
                height=40,
                font=("Arial", 14),
            )
            self.confirm_entry.pack(pady=10)
            self.confirm_entry.bind("<Return>", self._handle_submit)

        # Error message (hidden by default)
        self.error_label = ctk.CTkLabel(
            self.frame, text="", font=("Arial", 12), text_color="#FF4444"
        )
        self.error_label.pack(pady=5)

        # Submit button
        button_text = "Set Password" if not self.manager.is_master_set() else "Login"
        self.submit_button = ctk.CTkButton(
            self.frame,
            text=button_text,
            command=self._handle_submit,
            width=300,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        self.submit_button.pack(pady=10)

        self.password_entry.focus()

    def _handle_submit(self, event=None):
        # Handle login or set master password
        password = self.password_entry.get()

        if not password:
            self._show_error("Please enter a password")
            return

        if not self.manager.is_master_set():
            # First run - set master password
            confirm = self.confirm_entry.get()
            if password != confirm:
                self._show_error("Passwords do not match")
                return
            if len(password) < 4:
                self._show_error("Password must be at least 4 characters")
                return
            if self.manager.set_master_password(password):
                self._on_success()
            else:
                self._show_error("Failed to set master password")
        else:
            # Login - verify password
            if self.manager.verify_master_password(password):
                self._on_success()
            else:
                self._show_error("Incorrect password")
                self.password_entry.delete(0, "end")
                self.password_entry.focus()

    def _show_error(self, message: str):
        # Show error message
        self.error_label.configure(text=message)

    def _on_success(self):
        # Login successful - close and open main app
        self.grab_release()
        self.destroy()
        self.on_success()

    def _on_close(self):
        # Close button - terminate entire app
        self.grab_release()
        self.destroy()
        import sys

        sys.exit(0)
