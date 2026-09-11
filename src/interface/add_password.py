# AddPasswordWindow - Form for adding and editing passwords

import customtkinter as ctk
from src.storage.manager import PasswordManager


class AddPasswordWindow(ctk.CTkToplevel):
    # Add/Edit password form modal

    CATEGORIES = ["Social", "Email", "Banking", "Other"]

    def __init__(self, manager: PasswordManager, on_save_callback, entry=None):
        super().__init__()

        self.manager = manager
        self.on_save = on_save_callback
        self.entry = entry  # None = add mode, dict = edit mode
        self.is_edit_mode = entry is not None

        # Window setup
        title = "Edit Password" if self.is_edit_mode else "Add New Password"
        self.title(title)
        self.geometry("500x650")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.transient(self.master)
        self.grab_set()

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (650 // 2)
        self.geometry(f"500x650+{x}+{y}")

        self._create_widgets()

        if self.is_edit_mode:
            self._populate_form(entry)

    def _create_widgets(self):
        # Scrollable form
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#555555",
            scrollbar_button_hover_color="#777777",
        )
        self.scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.frame.pack(fill="x", padx=20)

        # Form title
        title_text = "Edit Password" if self.is_edit_mode else "Add New Password"
        ctk.CTkLabel(
            self.frame,
            text=title_text,
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF",
        ).pack(pady=(0, 20))

        # Title field
        ctk.CTkLabel(
            self.frame, text="Title *", font=("Arial", 12), text_color="#AAAAAA"
        ).pack(anchor="w", pady=(0, 5))
        self.title_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g., Gmail, Netflix, Bank",
            width=390,
            height=38,
            font=("Arial", 13),
        )
        self.title_entry.pack(pady=(0, 10))

        # Username field
        ctk.CTkLabel(
            self.frame,
            text="Username / Email *",
            font=("Arial", 12),
            text_color="#AAAAAA",
        ).pack(anchor="w", pady=(0, 5))
        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="e.g., user@email.com",
            width=390,
            height=38,
            font=("Arial", 13),
        )
        self.username_entry.pack(pady=(0, 10))

        # Password field with show/hide + generate
        ctk.CTkLabel(
            self.frame, text="Password *", font=("Arial", 12), text_color="#AAAAAA"
        ).pack(anchor="w", pady=(0, 5))
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

        # Show/hide toggle
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

        # Generate button
        ctk.CTkButton(
            password_frame,
            text="⚡ Generate",
            width=80,
            height=38,
            font=("Arial", 11),
            fg_color="#10B981",
            hover_color="#059669",
            command=self._open_generator,
        ).pack(side="left", padx=(10, 0))

        # Category dropdown
        ctk.CTkLabel(
            self.frame, text="Category", font=("Arial", 12), text_color="#AAAAAA"
        ).pack(anchor="w", pady=(0, 5))
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

        # Notes field
        ctk.CTkLabel(
            self.frame,
            text="Notes (optional)",
            font=("Arial", 12),
            text_color="#AAAAAA",
        ).pack(anchor="w", pady=(0, 5))
        self.notes_textbox = ctk.CTkTextbox(
            self.frame, width=390, height=80, font=("Arial", 13)
        )
        self.notes_textbox.pack(pady=(0, 10))

        # Error message
        self.error_label = ctk.CTkLabel(
            self.frame, text="", font=("Arial", 12), text_color="#FF4444"
        )
        self.error_label.pack(pady=(0, 10))

        # Buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=140,
            height=45,
            font=("Arial", 14),
            fg_color="#555555",
            hover_color="#444444",
        ).pack(side="left", padx=(0, 10))

        save_text = "Add Password" if not self.is_edit_mode else "Update Password"
        self.save_button = ctk.CTkButton(
            button_frame,
            text=save_text,
            command=self._save_password,
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        self.save_button.pack(side="right")

    def _populate_form(self, entry: dict):
        # Fill form with existing data for editing
        self.title_entry.insert(0, entry.get("title", ""))
        self.username_entry.insert(0, entry.get("username", ""))
        self.password_entry.insert(0, entry.get("password", ""))
        self.category_var.set(entry.get("category", "Other"))
        notes = entry.get("notes", "")
        if notes:
            self.notes_textbox.insert("1.0", notes)

    def _toggle_password_visibility(self):
        # Show/hide password
        if self.show_password_var.get():
            self.password_entry.configure(show="●")
            self.show_password_var.set(False)
        else:
            self.password_entry.configure(show="")
            self.show_password_var.set(True)

    def _open_generator(self):
        # Open password generator and use result
        from src.components.generator import PasswordGeneratorDialog

        dialog = PasswordGeneratorDialog(self)
        self.wait_window(dialog)
        if hasattr(dialog, "generated_password") and dialog.generated_password:
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, dialog.generated_password)
            self.password_entry.configure(show="")
            self.show_password_var.set(True)

    def _save_password(self):
        # Validate and save
        title = self.title_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        category = self.category_var.get()
        notes = self.notes_textbox.get("1.0", "end-1c").strip()

        if not title:
            self._show_error("Title is required")
            return
        if not username:
            self._show_error("Username is required")
            return
        if not password:
            self._show_error("Password is required")
            return

        entry = {
            "title": title,
            "username": username,
            "password": password,
            "category": category,
            "notes": notes,
        }

        if self.is_edit_mode:
            if self.manager.update_password(self.entry["id"], entry):
                self._on_save_success()
            else:
                self._show_error("Failed to update password")
        else:
            self.manager.add_password(entry)
            self._on_save_success()

    def _on_save_success(self):
        # Close modal and refresh dashboard
        self.grab_release()
        self.destroy()
        if self.on_save:
            self.on_save()

    def _show_error(self, message: str):
        # Show error message
        self.error_label.configure(text=message)

    def _on_close(self):
        # Close this modal only
        self.grab_release()
        self.destroy()
