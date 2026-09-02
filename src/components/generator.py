"""
Password Generator - Creates secure random passwords.

This module provides:
- Secure password generation using the secrets module
- Configurable password length
- Options for character types (uppercase, lowercase, digits, symbols)
- Interactive popup dialog for generator UI
- Copy to clipboard functionality

The secrets module is used instead of random for cryptographic security,
making the generated passwords suitable for actual use.
"""

import secrets
import string
import customtkinter as ctk


class PasswordGenerator:
    """
    Core password generation logic.

    This class handles the actual generation of secure passwords
    based on the specified criteria.
    """

    # Character sets for password generation
    LOWERCASE = string.ascii_lowercase  # a-z
    UPPERCASE = string.ascii_uppercase  # A-Z
    DIGITS = string.digits  # 0-9
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    @staticmethod
    def generate_password(
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ) -> str:
        """
        Generate a secure random password.

        Args:
            length: Desired password length (4-128)
            use_uppercase: Include uppercase letters (A-Z)
            use_lowercase: Include lowercase letters (a-z)
            use_digits: Include numbers (0-9)
            use_symbols: Include special characters (!@#$%^&*)

        Returns:
            str: The generated password

        Raises:
            ValueError: If no character types are selected
        """
        # Build the character pool based on selected options
        char_pool = ""

        if use_lowercase:
            char_pool += PasswordGenerator.LOWERCASE
        if use_uppercase:
            char_pool += PasswordGenerator.UPPERCASE
        if use_digits:
            char_pool += PasswordGenerator.DIGITS
        if use_symbols:
            char_pool += PasswordGenerator.SYMBOLS

        # Ensure we have characters to choose from
        if not char_pool:
            raise ValueError("At least one character type must be selected")

        # Ensure minimum length
        length = max(4, min(128, length))

        # Generate password using secrets for cryptographic security
        password = "".join(secrets.choice(char_pool) for _ in range(length))

        return password

    @staticmethod
    def calculate_strength(password: str) -> tuple:
        """
        Calculate password strength score.

        Args:
            password: The password to evaluate

        Returns:
            tuple: (score, label) where score is 0-4 and label is description
        """
        score = 0

        # Check length
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        # Check character variety
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        if variety_count >= 3:
            score += 1
        if variety_count == 4:
            score += 1

        # Determine label
        labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
        label = labels[min(score, 4)]

        return score, label


class PasswordGeneratorDialog(ctk.CTkToplevel):
    """
    Interactive popup dialog for generating passwords.

    This dialog provides a user-friendly interface for configuring
    and generating passwords with various options.
    """

    def __init__(self, parent):
        """
        Initialize the password generator dialog.

        Args:
            parent: Parent window
        """
        super().__init__(parent)

        # Store the generated password
        self.generated_password = None

        # Configure window
        self.title("Password Generator")
        self.geometry("400x500")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"400x500+{x}+{y}")

        # Create UI
        self._create_widgets()

    def _create_widgets(self):
        """Create all dialog widgets."""

        # Main container
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=25, pady=20)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="Password Generator",
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF",
        )
        title.pack(pady=(0, 15))

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
        options_label = ctk.CTkLabel(
            frame, text="Character Types", font=("Arial", 13), text_color="#AAAAAA"
        )
        options_label.pack(anchor="w", pady=(0, 10))

        # Checkbox frame
        checkbox_frame = ctk.CTkFrame(frame, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=(0, 15))

        # Uppercase checkbox
        self.uppercase_var = ctk.BooleanVar(value=True)
        uppercase_cb = ctk.CTkCheckBox(
            checkbox_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        uppercase_cb.pack(anchor="w", pady=3)

        # Lowercase checkbox
        self.lowercase_var = ctk.BooleanVar(value=True)
        lowercase_cb = ctk.CTkCheckBox(
            checkbox_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        lowercase_cb.pack(anchor="w", pady=3)

        # Digits checkbox
        self.digits_var = ctk.BooleanVar(value=True)
        digits_cb = ctk.CTkCheckBox(
            checkbox_frame,
            text="Numbers (0-9)",
            variable=self.digits_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        digits_cb.pack(anchor="w", pady=3)

        # Symbols checkbox
        self.symbols_var = ctk.BooleanVar(value=True)
        symbols_cb = ctk.CTkCheckBox(
            checkbox_frame,
            text="Symbols (!@#$%^&*)",
            variable=self.symbols_var,
            font=("Arial", 12),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        symbols_cb.pack(anchor="w", pady=3)

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

        # Button frame
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x")

        # Generate button
        generate_btn = ctk.CTkButton(
            button_frame,
            text="⚡ Generate",
            command=self._generate_password,
            width=120,
            height=38,
            font=("Arial", 13, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
        )
        generate_btn.pack(side="left", padx=(0, 10))

        # Copy button
        copy_btn = ctk.CTkButton(
            button_frame,
            text="📋 Copy",
            command=self._copy_password,
            width=100,
            height=38,
            font=("Arial", 13),
            fg_color="#3B82F6",
            hover_color="#2563EB",
        )
        copy_btn.pack(side="left", padx=(0, 10))

        # Use button (confirm selection)
        use_btn = ctk.CTkButton(
            button_frame,
            text="Use Password",
            command=self._use_password,
            width=120,
            height=38,
            font=("Arial", 13, "bold"),
            fg_color="#2B5EA7",
            hover_color="#1E4080",
        )
        use_btn.pack(side="right")

    def _on_length_change(self, value):
        """
        Update the length label when slider changes.

        Args:
            value: Current slider value
        """
        length = int(value)
        self.length_label.configure(text=f"Password Length: {length}")

    def _generate_password(self):
        """Generate a new password based on selected options."""
        try:
            password = PasswordGenerator.generate_password(
                length=int(self.length_slider.get()),
                use_uppercase=self.uppercase_var.get(),
                use_lowercase=self.lowercase_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
            )

            # Display the password
            self.password_display.configure(text=password)

            # Calculate and display strength
            score, label = PasswordGenerator.calculate_strength(password)
            colors = ["#FF4444", "#FF8800", "#FFCC00", "#88FF00", "#00FF00"]
            self.strength_label.configure(
                text=f"Strength: {label}", text_color=colors[score]
            )

        except ValueError as e:
            self.password_display.configure(text=str(e))

    def _copy_password(self):
        """Copy the generated password to clipboard."""
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
        """Confirm and use the generated password."""
        password = self.password_display.cget("text")

        if password and password not in [
            "Click 'Generate' to create a password",
            "✓ Copied to clipboard!",
        ]:
            self.generated_password = password
            self.grab_release()
            self.destroy()
