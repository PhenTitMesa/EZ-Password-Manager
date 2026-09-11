# DashboardWindow - Password list, search, and management UI

import customtkinter as ctk
from src.storage.manager import PasswordManager


class DashboardWindow(ctk.CTkFrame):
    # Main dashboard showing all passwords with search and actions

    def __init__(self, master, manager: PasswordManager):
        super().__init__(master, fg_color="transparent")

        self.manager = manager

        # Callbacks (set by MainWindow)
        self.on_add_password = None
        self.on_edit_password = None

        self._create_header()
        self._create_search_bar()
        self._create_password_list()
        self.refresh_password_list()

    def _create_header(self):
        # Title + Add button
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="My Passwords",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF",
        )
        title.pack(side="left")

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
        # Search input + clear button
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))

        search_label = ctk.CTkLabel(
            search_frame, text="🔍", font=("Arial", 16), text_color="#888888"
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by title/username...",
            width=400,
            height=35,
            font=("Arial", 13),
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)

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
        # Scrollable list of password cards
        self.password_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#555555",
            scrollbar_button_hover_color="#777777",
        )
        self.password_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Empty state label
        self.empty_label = ctk.CTkLabel(
            self.password_frame,
            text="No passwords yet.\nClick '+ Add Password' to get started!",
            font=("Arial", 14),
            text_color="#888888",
        )

    def refresh_password_list(self, passwords=None):
        # Refresh the password list display
        for widget in self.password_frame.winfo_children():
            widget.destroy()

        if passwords is None:
            passwords = self.manager.get_all_passwords()

        if not passwords:
            self.empty_label = ctk.CTkLabel(
                self.password_frame,
                text="No passwords found.\nClick '+ Add Password' to get started!",
                font=("Arial", 14),
                text_color="#888888",
            )
            self.empty_label.pack(pady=50)
            return

        for entry in passwords:
            self._create_password_card(entry)

    def _create_password_card(self, entry: dict):
        # Single password entry card
        card = ctk.CTkFrame(
            self.password_frame,
            fg_color="#2B2B2B",
            corner_radius=10,
            border_width=1,
            border_color="#3B3B3B",
        )
        card.pack(fill="x", pady=5, padx=5)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)

        # Title + category
        title_frame = ctk.CTkFrame(content, fg_color="transparent")
        title_frame.pack(fill="x")

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
        category_badge = ctk.CTkLabel(
            title_frame,
            text=category,
            font=("Arial", 10),
            text_color="#FFFFFF",
            fg_color=category_colors.get(category, "#6B7280"),
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
            ctk.CTkLabel(
                username_frame,
                text=f"👤 {username}",
                font=("Arial", 12),
                text_color="#AAAAAA",
            ).pack(side="left")
            ctk.CTkButton(
                username_frame,
                text="📋",
                width=30,
                height=25,
                font=("Arial", 12),
                fg_color="transparent",
                hover_color="#3B3B3B",
                command=lambda u=username: self._copy_to_clipboard(u, "Username"),
            ).pack(side="right")

        # Password row (masked)
        password_frame = ctk.CTkFrame(content, fg_color="transparent")
        password_frame.pack(fill="x", pady=(5, 0))
        password_masked = "●" * min(len(entry.get("password", "")), 12)
        ctk.CTkLabel(
            password_frame,
            text=f"🔒 {password_masked}",
            font=("Arial", 12),
            text_color="#AAAAAA",
        ).pack(side="left")
        ctk.CTkButton(
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
        ).pack(side="right")

        # Action buttons
        action_frame = ctk.CTkFrame(content, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(
            action_frame,
            text="✏️ Edit",
            width=80,
            height=30,
            font=("Arial", 11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=lambda e=entry: self._on_edit_click(e),
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            action_frame,
            text="🗑️ Delete",
            width=80,
            height=30,
            font=("Arial", 11),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=lambda e=entry: self._on_delete_click(e),
        ).pack(side="left")

        # Notes preview
        notes = entry.get("notes", "")
        if notes:
            ctk.CTkLabel(
                action_frame,
                text=f"📝 {notes[:30]}{'...' if len(notes) > 30 else ''}",
                font=("Arial", 10),
                text_color="#666666",
            ).pack(side="right")

    def _copy_to_clipboard(self, text: str, label: str):
        # Copy text to clipboard
        try:
            import pyperclip

            pyperclip.copy(text)
            self._show_toast(f"{label} copied!")
        except ImportError:
            self._show_toast("Copy not available - install pyperclip")

    def _show_toast(self, message: str):
        # Show temporary notification at bottom
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
        toast.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2000, toast.destroy)

    def _on_add_click(self):
        if self.on_add_password:
            self.on_add_password()

    def _on_edit_click(self, entry: dict):
        if self.on_edit_password:
            self.on_edit_password(entry)

    def _on_delete_click(self, entry: dict):
        # Delete with confirmation
        dialog = ctk.CTkInputDialog(
            text=f"Delete '{entry.get('title', 'Untitled')}'?\n\nType 'DELETE' to confirm:",
            title="Confirm Delete",
        )
        response = dialog.get_input()
        if response and response.strip().upper() == "DELETE":
            if self.manager.delete_password(entry["id"]):
                self.refresh_password_list()
                self._show_toast("Password deleted!")
            else:
                self._show_toast("Failed to delete password")

    def _on_search(self, event=None):
        # Filter passwords by search query
        query = self.search_entry.get().strip()
        if not query:
            self.refresh_password_list()
            return
        results = self.manager.search_passwords(query)
        self.refresh_password_list(results)

    def _clear_search(self):
        # Clear search and show all passwords
        self.search_entry.delete(0, "end")
        self.refresh_password_list()
