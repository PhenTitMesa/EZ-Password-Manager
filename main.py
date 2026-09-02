"""
Simple Password Manager - Main Entry Point

This is the main script to run the password manager application.
It handles:
- Application initialization
- Login screen display
- Main window creation after authentication

Usage:
    python main.py

Requirements:
    - Python 3.8+
    - CustomTkinter
    - cryptography
    - pyperclip

Author: Student Project
Version: 1.0
"""

import sys
import os

# Add the project root to Python path
# This allows us to import from src/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set CustomTkinter appearance
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def main():
    """
    Main entry point for the application.

    This function:
    1. Creates the PasswordManager instance
    2. Shows login screen (or setup screen on first run)
    3. Opens main window after successful authentication
    """
    # Import here to avoid circular imports
    from src.storage.manager import PasswordManager
    from src.interface.login import LoginWindow
    from src.interface.main_window import MainWindow

    # Create the password manager
    manager = PasswordManager()

    # Create a hidden root window (needed for tkinter)
    root = ctk.CTk()
    root.withdraw()  # Hide the root window

    def open_main_window():
        """Open the main application window after successful login."""
        # Create and show the main window
        app = MainWindow(manager)
        app.mainloop()

    # Show the login window
    # This will handle first-run setup or password verification
    login = LoginWindow(manager, on_success_callback=open_main_window)

    # Start the tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # Print a welcome message
    print("=" * 50)
    print("  Simple Password Manager v1.0")
    print("  Secure • Simple • Modern")
    print("=" * 50)
    print()
    print("Starting application...")
    print()

    # Run the application
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please report this issue.")
        sys.exit(1)
