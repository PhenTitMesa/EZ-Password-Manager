"""
Dashboard Window - Main interface for managing passwords.

This module provides:
- Scrollable list of all password entries
- Search bar for filtering passwords
- Add new password button
- Edit and delete buttons for each entry
- Copy to clipboard functionality
- Empty state when no passwords exist

The dashboard is the main screen users interact with after login.
"""

import customtkinter as ctk
from src.storage.manager import PasswordManager
from src import VERSION


class DashboardWindow(ctk.CTkFrame):
    """
    Dashboard frame showing all passwords with management options.

    This frame displays inside the main window and provides
    the core functionality for viewing and managing passwords.
    """

    def __init__(self, master, manager: PasswordManager):
        """
        Initialize the dashboard.

        Args:
            master: Parent window (MainWindow)
            manager: PasswordManager instance for data operations
        """
        super().__init__(master, fg_color="transparent")

        # Store reference to manager
        self.manager = manager

        # Callbacks for opening other windows
        self.on_add_password = None
        self.on_edit_password = None

        # Create the UI
        self._create_header()
        self._create_search_bar()
        self._create_password_list()

        # Load and display passwords
        self.refresh_password_list()

    def _create_header(self):
        """Create the header with title and add button."""

        # Header frame
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        title = ctk.CTkLabel(
            header,
            text="My Passwords",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF",
        )
        title.pack(side="left")

        # Add new password button
        self.add_button = ctk.CTkButton(
            header,
            text="+ Add Password",
            command=self._on_add_click,
            width=140,
            height=35,
            font=("Arial", 13, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        self.add_button.pack(side="right")

    def _create_search_bar(self):
        """Create the search bar for filtering passwords."""

        # Search frame
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Search icon/label
        search_label = ctk.CTkLabel(
            search_frame, text="🔍", font=("Arial", 16), text_color="#888888"
        )
        search_label.pack(side="left", padx=(0, 10))

        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by title or username...",
            width=400,
            height=35,
            font=("Arial", 13),
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # Clear search button
        self.clear_search_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self._clear_search,
            width=60,
            height=35,
            font=("Arial", 12),
            fg_color="#555555",
            hover_color="#444444",
        )
        self.clear_search_button.pack(side="left")

    def _create_password_list(self):
        """Create the scrollable list for password entries."""

        # Scrollable frame for password entries
        self.password_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#555555",
            scrollbar_button_hover_color="#777777",
        )
        self.password_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Empty state label (shown when no passwords)
        self.empty_label = ctk.CTkLabel(
            self.password_frame,
            text="No passwords yet.\nClick '+ Add Password' to get started!",
            font=("Arial", 14),
            text_color="#888888",
        )

        # Status label for search results
        self.status_label = ctk.CTkLabel(
            self.password_frame, text="", font=("Arial", 12), text_color="#666666"
        )

    def refresh_password_list(self, passwords=None):
        """
        Refresh the password list display.

        Args:
            passwords: List of passwords to display (None = load all)
        """
        # Clear existing entries
        for widget in self.password_frame.winfo_children():
            widget.destroy()

        # Get passwords from manager if not provided
        if passwords is None:
            passwords = self.manager.get_all_passwords()

        # Show empty state if no passwords
        if not passwords:
            self.empty_label = ctk.CTkLabel(
                self.password_frame,
                text="No passwords found.\nClick '+ Add Password' to get started!",
                font=("Arial", 14),
                text_color="#888888",
            )
            self.empty_label.pack(pady=50)
            return

        # Create a card for each password
        for entry in passwords:
            self._create_password_card(entry)

    def _create_password_card(self, entry: dict):
        """
        Create a card widget for a single password entry.

        Args:
            entry: Password entry dictionary
        """
        # Card frame with background
        card = ctk.CTkFrame(
            self.password_frame,
            fg_color="#2B2B2B",
            corner_radius=10,
            border_width=1,
            border_color="#3B3B3B",
        )
        card.pack(fill="x", pady=5, padx=5)

        # Content frame (inside card)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)

        # Title and category row
        title_frame = ctk.CTkFrame(content, fg_color="transparent")
        title_frame.pack(fill="x")

        # Title
        title_label = ctk.CTkLabel(
            title_frame,
            text=entry.get("title", "Untitled"),
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF",
        )
        title_label.pack(side="left")

        # Category badge
        category = entry.get("category", "Other")
        category_colors = {
            "Social": "#3B82F6",
            "Email": "#10B981",
            "Banking": "#F59E0B",
            "Other": "#6B7280",
        }
        category_color = category_colors.get(category, "#6B7280")

        category_badge = ctk.CTkLabel(
            title_frame,
            text=category,
            font=("Arial", 10),
            text_color="#FFFFFF",
            fg_color=category_color,
            corner_radius=4,
            padx=8,
            pady=2,
        )
        category_badge.pack(side="right")

        # Username row
        username = entry.get("username", "")
        if username:
            username_frame = ctk.CTkFrame(content, fg_color="transparent")
            username_frame.pack(fill="x", pady=(5, 0))

            username_label = ctk.CTkLabel(
                username_frame,
                text=f"👤 {username}",
                font=("Arial", 12),
                text_color="#AAAAAA",
            )
            username_label.pack(side="left")

            # Copy username button
            copy_user_btn = ctk.CTkButton(
                username_frame,
                text="📋",
                width=30,
                height=25,
                font=("Arial", 12),
                fg_color="transparent",
                hover_color="#3B3B3B",
                command=lambda u=username: self._copy_to_clipboard(u, "Username"),
            )
            copy_user_btn.pack(side="right")

        # Password row (masked)
        password_frame = ctk.CTkFrame(content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(5, 0))

        password_masked = "●" * min(len(entry.get("password", "")), 12)
        password_label = ctk.CTkLabel(
            password_frame,
            text=f"🔒 {password_masked}",
            font=("Arial", 12),
            text_color="#AAAAAA",
        )
        password_label.pack(side="left")

        # Copy password button
        copy_pass_btn = ctk.CTkButton(
            password_frame,
            text="📋",
            width=30,
            height=25,
            font=("Arial", 12),
            fg_color="transparent",
            hover_color="#3B3B3B",
            command=lambda p=entry.get("password", ""): self._copy_to_clipboard(
                p, "Password"
            ),
        )
        copy_pass_btn.pack(side="right")

        # Action buttons row
        action_frame = ctk.CTkFrame(content, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 0))

        # Edit button
        edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️ Edit",
            width=80,
            height=30,
            font=("Arial", 11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=lambda e=entry: self._on_edit_click(e),
        )
        edit_btn.pack(side="left", padx=(0, 5))

        # Delete button
        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Delete",
            width=80,
            height=30,
            font=("Arial", 11),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=lambda e=entry: self._on_delete_click(e),
        )
        delete_btn.pack(side="left")

        # Notes (if any)
        notes = entry.get("notes", "")
        if notes:
            notes_label = ctk.CTkLabel(
                action_frame,
                text=f"📝 {notes[:30]}{'...' if len(notes) > 30 else ''}",
                font=("Arial", 10),
                text_color="#666666",
            )
            notes_label.pack(side="right")

    def _copy_to_clipboard(self, text: str, label: str):
        """
        Copy text to clipboard and show feedback.

        Args:
            text: Text to copy
            label: Label for the feedback message (e.g., "Password")
        """
        try:
            import pyperclip

            pyperclip.copy(text)
            self._show_toast(f"{label} copied!")
        except ImportError:
            # Fallback if pyperclip isn't installed
            self._show_toast("Copy not available - install pyperclip")

    def _show_toast(self, message: str):
        """
        Show a temporary toast notification.

        Args:
            message: The message to display
        """
        # Create a temporary label for the toast
        toast = ctk.CTkLabel(
            self.master,
            text=message,
            font=("Arial", 12),
            text_color="#FFFFFF",
            fg_color="#2B5EA7",
            corner_radius=5,
            padx=15,
            pady=8,
        )

        # Position at bottom center of main window
        toast.place(relx=0.5, rely=0.95, anchor="center")

        # Auto-remove after 2 seconds
        self.after(2000, toast.destroy)

    def _on_add_click(self):
        """Handle add password button click."""
        if self.on_add_password:
            self.on_add_password()

    def _on_edit_click(self, entry: dict):
        """Handle edit button click for a password entry."""
        if self.on_edit_password:
            self.on_edit_password(entry)

    def _on_delete_click(self, entry: dict):
        """
        Handle delete button click with confirmation.

        Args:
            entry: The password entry to delete
        """
        # Create confirmation dialog
        dialog = ctk.CTkInputDialog(
            text=f"Delete '{entry.get('title', 'Untitled')}'?\n\nType 'DELETE' to confirm:",
            title="Confirm Delete",
        )

        # Get user input
        response = dialog.get_input()

        # Check if user typed DELETE
        if response and response.strip().upper() == "DELETE":
            # Delete the entry
            if self.manager.delete_password(entry["id"]):
                self.refresh_password_list()
                self._show_toast("Password deleted!")
            else:
                self._show_toast("Failed to delete password")

    def _on_search(self, event=None):
        """
        Handle search input changes.

        Filters the password list based on the search query.
        """
        query = self.search_entry.get().strip()

        if not query:
            # If search is empty, show all passwords
            self.refresh_password_list()
            return

        # Search for matching passwords
        results = self.manager.search_passwords(query)
        self.refresh_password_list(results)

    def _clear_search(self):
        """Clear the search field and show all passwords."""
        self.search_entry.delete(0, "end")
        self.refresh_password_list()
