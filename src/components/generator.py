# PasswordGenerator - Secure random password generation

import secrets
import string
import customtkinter as ctk


class PasswordGenerator:
    # Core password generation logic

    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    @staticmethod
    def generate_password(
        length=16,
        use_uppercase=True,
        use_lowercase=True,
        use_digits=True,
        use_symbols=True,
    ) -> str:
        # Generate secure random password
        char_pool = ""
        if use_lowercase:
            char_pool += PasswordGenerator.LOWERCASE
        if use_uppercase:
            char_pool += PasswordGenerator.UPPERCASE
        if use_digits:
            char_pool += PasswordGenerator.DIGITS
        if use_symbols:
            char_pool += PasswordGenerator.SYMBOLS

        if not char_pool:
            raise ValueError("At least one character type must be selected")

        length = max(4, min(128, length))
        return "".join(secrets.choice(char_pool) for _ in range(length))

    @staticmethod
    def calculate_strength(password: str) -> tuple:
        # Calculate password strength (0-4)
        score = 0
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        if variety_count >= 3:
            score += 1
        if variety_count == 4:
            score += 1

        labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
        return score, labels[min(score, 4)]


class PasswordGeneratorDialog(ctk.CTkToplevel):
    # Password generator popup dialog

    def __init__(self, parent):
        super().__init__(parent)

        self.generated_password = None

        # Window setup
        self.title("Password Generator")
        self.geometry("400x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"400x500+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=25, pady=20)

        # Title
        ctk.CTkLabel(
            frame,
            text="Password Generator",
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF",
        ).pack(pady=(0, 15))

        # Length slider
        self.length_label = ctk.CTkLabel(
            frame, text="Password Length: 16", font=("Arial", 13), text_color="#AAAAAA"
        )
        self.length_label.pack(anchor="w", pady=(0, 5))

        self.length_slider = ctk.CTkSlider(
            frame,
            from_=4,
            to=64,
            number_of_steps=60,
            command=self._on_length_change,
            width=350,
            height=20,
        )
        self.length_slider.set(16)
        self.length_slider.pack(pady=(0, 15))

        # Character type checkboxes
        ctk.CTkLabel(
            frame, text="Character Types", font=("Arial", 13), text_color="#AAAAAA"
        ).pack(anchor="w", pady=(0, 10))

        checkbox_frame = ctk.CTkFrame(frame, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=(0, 15))

        self.uppercase_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        ).pack(anchor="w", pady=3)

        self.lowercase_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        ).pack(anchor="w", pady=3)

        self.digits_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Numbers (0-9)",
            variable=self.digits_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        ).pack(anchor="w", pady=3)

        self.symbols_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Symbols (!@#$%^&*)",
            variable=self.symbols_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        ).pack(anchor="w", pady=3)

        # Generated password display
        password_frame = ctk.CTkFrame(frame, fg_color="#1E1E1E", corner_radius=8)
        password_frame.pack(fill="x", pady=(10, 10))

        self.password_display = ctk.CTkLabel(
            password_frame,
            text="Click 'Generate' to create a password",
            font=("Courier", 14),
            text_color="#00FF00",
            wraplength=330,
        )
        self.password_display.pack(padx=15, pady=15)

        # Strength indicator
        self.strength_label = ctk.CTkLabel(
            frame, text="", font=("Arial", 11), text_color="#888888"
        )
        self.strength_label.pack(pady=(0, 10))

        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x")

        ctk.CTkButton(
            button_frame,
            text="⚡ Generate",
            command=self._generate_password,
            width=120,
            height=38,
            font=("Arial", 13, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="📋 Copy",
            command=self._copy_password,
            width=100,
            height=38,
            font=("Arial", 13),
            fg_color="#3B82F6",
            hover_color="#2563EB",
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="Use Password",
            command=self._use_password,
            width=120,
            height=38,
            font=("Arial", 13, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        ).pack(side="right")

    def _on_length_change(self, value):
        # Update length label
        self.length_label.configure(text=f"Password Length: {int(value)}")

    def _generate_password(self):
        # Generate password with current settings
        try:
            password = PasswordGenerator.generate_password(
                length=int(self.length_slider.get()),
                use_uppercase=self.uppercase_var.get(),
                use_lowercase=self.lowercase_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
            )
            self.password_display.configure(text=password)

            score, label = PasswordGenerator.calculate_strength(password)
            colors = ["#FF4444", "#FF8800", "#FFCC00", "#88FF00", "#00FF00"]
            self.strength_label.configure(
                text=f"Strength: {label}", text_color=colors[score]
            )
        except ValueError as e:
            self.password_display.configure(text=str(e))

    def _copy_password(self):
        # Copy to clipboard
        password = self.password_display.cget("text")
        if password and password != "Click 'Generate' to create a password":
            try:
                import pyperclip

                pyperclip.copy(password)
                self.password_display.configure(text="✓ Copied to clipboard!")
                self.after(1500, lambda: self.password_display.configure(text=password))
            except ImportError:
                pass

    def _use_password(self):
        # Confirm and use generated password
        password = self.password_display.cget("text")
        if password and password not in [
            "Click 'Generate' to create a password",
            "✓ Copied to clipboard!",
        ]:
            self.generated_password = password
            self.grab_release()
            self.destroy()
