# Simple Password Manager - Main Entry Point
# Run this file to start the application

import sys
import os

# Add project root to Python path (so we can import from src/)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set CustomTkinter to dark theme
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def main():
    # Import here to avoid circular imports
    from src.storage.manager import PasswordManager
    from src.interface.login import LoginWindow
    from src.interface.main_window import MainWindow

    # Create password manager and hidden root window
    manager = PasswordManager()
    root = ctk.CTk()
    root.withdraw()  # Hide root window (we only need it for the event loop)

    def open_main_window():
        # Open main app after successful login
        app = MainWindow(manager)
        app.mainloop()

    # Show login screen (handles first-run setup or password verification)
    login = LoginWindow(manager, on_success_callback=open_main_window)

    # Start the event loop
    root.mainloop()


if __name__ == "__main__":
    print("=" * 50)
    print("  Simple Password Manager v1.0")
    print("=" * 50)
    print()

    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
