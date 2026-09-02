"""
Add/Edit Password Window - Form for creating and modifying passwords.

This module provides:
- Form with all required fields (title, username, password, category, notes)
- Password visibility toggle (show/hide)
- Category selection dropdown
- Form validation for required fields
- Both add and edit modes
- Integration with password generator

This window is used when adding a new password or editing an existing one.
"""

import customtkinter as ctk
from src.storage.manager import PasswordManager


class AddPasswordWindow(ctk.CTkToplevel):
    """
    Window for adding or editing password entries.

    This window provides a form for entering password details
    and handles both creation and modification of entries.
    """

    # Available categories for passwords
    CATEGORIES = ["Social", "Email", "Banking", "Other"]

    def __init__(self, manager: PasswordManager, on_save_callback, entry=None):
        """
        Initialize the add/edit password window.

        Args:
            manager: PasswordManager instance for data operations
            on_save_callback: Function to call after saving (refresh dashboard)
            entry: Existing entry to edit (None for new password)
        """
        super().__init__()

        # Store references
        self.manager = manager
        self.on_save = on_save_callback
        self.entry = entry  # None for add mode, dict for edit mode

        # Determine window title based on mode
        self.is_edit_mode = entry is not None
        title = "Edit Password" if self.is_edit_mode else "Add New Password"

        # Configure window
        self.title(title)
        self.geometry("450x550")
        self.resizable(False, False)

        # Make this window modal
        self.transient(self.master)
        self.grab_set()

        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"450x550+{x}+{y}")

        # Create the UI
        self._create_widgets()

        # If editing, populate the form with existing data
        if self.is_edit_mode:
            self._populate_form(entry)

    def _create_widgets(self):
        """Create all form widgets."""

        # Main container
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=30, pady=20)

        # Title label
        title_text = "Edit Password" if self.is_edit_mode else "Add New Password"
        title = ctk.CTkLabel(
            self.frame,
            text=title_text,
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF",
        )
        title.pack(pady=(0, 20))

        # Title field (required)
        title_label = ctk.CTkLabel(
            self.frame, text="Title *", font=("Arial", 12), text_color="#AAAAAA"
        )
        title_label.pack(anchor="w", pady=(0, 5))

        self.title_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g., Gmail, Netflix, Bank",
            width=390,
            height=38,
            font=("Arial", 13),
        )
        self.title_entry.pack(pady=(0, 10))

        # Username field (required)
        username_label = ctk.CTkLabel(
            self.frame,
            text="Username / Email *",
            font=("Arial", 12),
            text_color="#AAAAAA",
        )
        username_label.pack(anchor="w", pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g., user@email.com",
            width=390,
            height=38,
            font=("Arial", 13),
        )
        self.username_entry.pack(pady=(0, 10))

        # Password field with toggle (required)
        password_label = ctk.CTkLabel(
            self.frame, text="Password *", font=("Arial", 12), text_color="#AAAAAA"
        )
        password_label.pack(anchor="w", pady=(0, 5))

        password_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 10))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter password",
            show="●",
            width=340,
            height=38,
            font=("Arial", 13),
        )
        self.password_entry.pack(side="left")

        # Show/hide password toggle
        self.show_password_var = ctk.BooleanVar(value=False)
        self.show_hide_button = ctk.CTkButton(
            password_frame,
            text="👁️",
            width=40,
            height=38,
            font=("Arial", 14),
            fg_color="#3B3B3B",
            hover_color="#4B4B4B",
            command=self._toggle_password_visibility,
        )
        self.show_hide_button.pack(side="left", padx=(10, 0))

        # Generate password button
        generate_btn = ctk.CTkButton(
            password_frame,
            text="⚡ Generate",
            width=80,
            height=38,
            font=("Arial", 11),
            fg_color="#10B981",
            hover_color="#059669",
            command=self._open_generator,
        )
        generate_btn.pack(side="left", padx=(10, 0))

        # Category dropdown
        category_label = ctk.CTkLabel(
            self.frame, text="Category", font=("Arial", 12), text_color="#AAAAAA"
        )
        category_label.pack(anchor="w", pady=(0, 5))

        self.category_var = ctk.StringVar(value="Other")
        self.category_menu = ctk.CTkOptionMenu(
            self.frame,
            variable=self.category_var,
            values=self.CATEGORIES,
            width=390,
            height=38,
            font=("Arial", 13),
            fg_color="#3B3B3B",
            button_color="#4B4B4B",
        )
        self.category_menu.pack(pady=(0, 10))

        # Notes field (optional)
        notes_label = ctk.CTkLabel(
            self.frame,
            text="Notes (optional)",
            font=("Arial", 12),
            text_color="#AAAAAA",
        )
        notes_label.pack(anchor="w", pady=(0, 5))

        self.notes_textbox = ctk.CTkTextbox(
            self.frame, width=390, height=80, font=("Arial", 13)
        )
        self.notes_textbox.pack(pady=(0, 10))

        # Error message label
        self.error_label = ctk.CTkLabel(
            self.frame, text="", font=("Arial", 12), text_color="#FF4444"
        )
        self.error_label.pack(pady=(0, 5))

        # Button frame
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(fill="x")

        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=120,
            height=40,
            font=("Arial", 13),
            fg_color="#555555",
            hover_color="#444444",
        )
        cancel_btn.pack(side="left")

        # Save button
        save_text = "Update" if self.is_edit_mode else "Save"
        self.save_button = ctk.CTkButton(
            button_frame,
            text=save_text,
            command=self._save_password,
            width=120,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        self.save_button.pack(side="right")

    def _populate_form(self, entry: dict):
        """
        Fill the form with existing password data for editing.

        Args:
            entry: The password entry to edit
        """
        self.title_entry.insert(0, entry.get("title", ""))
        self.username_entry.insert(0, entry.get("username", ""))
        self.password_entry.insert(0, entry.get("password", ""))
        self.category_var.set(entry.get("category", "Other"))

        notes = entry.get("notes", "")
        if notes:
            self.notes_textbox.insert("1.0", notes)

    def _toggle_password_visibility(self):
        """Toggle password field between visible and hidden."""
        if self.show_password_var.get():
            self.password_entry.configure(show="●")
            self.show_password_var.set(False)
        else:
            self.password_entry.configure(show="")
            self.show_password_var.set(True)

    def _open_generator(self):
        """Open the password generator and use the result."""
        # Import here to avoid circular dependency
        from src.components.generator import PasswordGeneratorDialog

        # Open generator and get generated password
        dialog = PasswordGeneratorDialog(self)
        self.wait_window(dialog)

        # If a password was generated, insert it
        if hasattr(dialog, "generated_password") and dialog.generated_password:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, dialog.generated_password)
            # Show the password since we just generated it
            self.password_entry.configure(show="")
            self.show_password_var.set(True)

    def _save_password(self):
        """Validate and save the password entry."""

        # Get form values
        title = self.title_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        category = self.category_var.get()
        notes = self.notes_textbox.get("1.0", "end-1c").strip()

        # Validate required fields
        if not title:
            self._show_error("Title is required")
            return

        if not username:
            self._show_error("Username is required")
            return

        if not password:
            self._show_error("Password is required")
            return

        # Create the entry dictionary
        entry = {
            "title": title,
            "username": username,
            "password": password,
            "category": category,
            "notes": notes,
        }

        # Save to manager
        if self.is_edit_mode:
            # Update existing entry
            if self.manager.update_password(self.entry["id"], entry):
                self._on_save_success()
            else:
                self._show_error("Failed to update password")
        else:
            # Add new entry
            self.manager.add_password(entry)
            self._on_save_success()

    def _on_save_success(self):
        """Handle successful save operation."""
        self.grab_release()
        self.destroy()

        # Call the save callback to refresh the dashboard
        if self.on_save:
            self.on_save()

    def _show_error(self, message: str):
        """
        Display an error message.

        Args:
            message: The error message to display
        """
        self.error_label.configure(text=message)
