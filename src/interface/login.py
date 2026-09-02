"""
Login Window - Handles master password authentication.

This module provides:
- First-run setup for setting master password
- Login screen for subsequent runs
- Error handling for wrong passwords
- Smooth transition to main application

The login window adapts based on whether a master password exists:
- First run: Shows "Set Master Password" form with two fields
- Subsequent runs: Shows "Enter Master Password" form with one field
"""

import customtkinter as ctk
from src.storage.manager import PasswordManager


class LoginWindow(ctk.CTkToplevel):
    """
    Login window for master password authentication.

    This window appears before the main application to ensure
    only authorized users can access stored passwords.
    """

    def __init__(self, manager: PasswordManager, on_success_callback):
        """
        Initialize the login window.

        Args:
            manager: PasswordManager instance for authentication
            on_success_callback: Function to call when login succeeds
        """
        super().__init__()

        # Store reference to manager and callback
        self.manager = manager
        self.on_success = on_success_callback

        # Configure window
        self.title("Simple Password Manager - Login")
        self.geometry("400x350")
        self.resizable(False, False)

        # Handle window close button (X) - terminate the entire app
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Make this window modal (blocks interaction with other windows)
        self.transient(self.master)
        self.grab_set()

        # Center the window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"400x350+{x}+{y}")

        # Create the UI
        self._create_widgets()

    def _create_widgets(self):
        """Create all UI elements for the login window."""

        # Main container frame
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=40, pady=30)

        # Title label
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

        # Subtitle/description
        desc_text = (
            "Create a master password to secure your passwords"
            if not self.manager.is_master_set()
            else "Enter your master password to continue"
        )
        self.desc_label = ctk.CTkLabel(
            self.frame, text=desc_text, font=("Arial", 12), text_color="#888888"
        )
        self.desc_label.pack(pady=(0, 20))

        # Password entry field
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Master Password",
            show="●",  # Hide password characters
            width=300,
            height=40,
            font=("Arial", 14),
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", self._handle_submit)  # Enter key

        # Confirm password field (only for first run)
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

        # Error message label (hidden by default)
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

        # Focus on password entry
        self.password_entry.focus()

    def _handle_submit(self, event=None):
        """
        Handle the submit button click or Enter key press.

        For first run: Validates passwords match and sets master password
        For subsequent runs: Verifies password against stored hash
        """
        password = self.password_entry.get()

        # Check if password is empty
        if not password:
            self._show_error("Please enter a password")
            return

        if not self.manager.is_master_set():
            # First run - set master password
            confirm = self.confirm_entry.get()

            # Check if passwords match
            if password != confirm:
                self._show_error("Passwords do not match")
                return

            # Check minimum length
            if len(password) < 4:
                self._show_error("Password must be at least 4 characters")
                return

            # Set the master password
            if self.manager.set_master_password(password):
                # Success - open main application
                self._on_success()
            else:
                self._show_error("Failed to set master password")
        else:
            # Subsequent runs - verify password
            if self.manager.verify_master_password(password):
                # Success - open main application
                self._on_success()
            else:
                self._show_error("Incorrect password")
                # Clear the entry for retry
                self.password_entry.delete(0, "end")
                self.password_entry.focus()

    def _show_error(self, message: str):
        """
        Display an error message to the user.

        Args:
            message: The error message to display
        """
        self.error_label.configure(text=message)

    def _on_success(self):
        """Handle successful authentication."""
        # Close this window
        self.grab_release()
        self.destroy()

        # Call the success callback to open main window
        self.on_success()

    def _on_close(self):
        """Handle window close button (X) - terminate the entire application."""
        self.grab_release()
        self.destroy()
        import sys

        sys.exit(0)
