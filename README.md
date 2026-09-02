# Simple Password Manager v1.0

A beginner-friendly password manager with modern CustomTkinter UI, Fernet encryption, and secure storage.

## Features

- **Master Password Login** - Secure authentication with PBKDF2 hashing
- **Password Storage** - Encrypted JSON storage using Fernet (AES-128)
- **Password Generator** - Create secure passwords with customizable options
- **Search & Filter** - Find passwords by title or username
- **Copy to Clipboard** - One-click copy for usernames and passwords
- **Modern UI** - Dark-themed CustomTkinter interface

## Requirements

- Python 3.8+
- CustomTkinter (modern UI)
- cryptography (Fernet encryption)
- pyperclip (clipboard operations)

## Installation

```bash
# Clone or download this project
cd Simple Password Manager

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## First Run

1. Launch the application
2. You'll see "Set Master Password" screen
3. Enter a master password (minimum 4 characters)
4. Confirm your password
5. Click "Set Password"

## Subsequent Runs

1. Launch the application
2. Enter your master password
3. Click "Login"

## Usage

### Adding Passwords
1. Click "+ Add Password" button
2. Fill in title, username, and password
3. Select a category (Social, Email, Banking, Other)
4. Add notes (optional)
5. Click "Save"

### Using Password Generator
1. In the Add/Edit form, click "⚡ Generate"
2. Adjust length with the slider
3. Select character types (uppercase, lowercase, digits, symbols)
4. Click "Generate" to create a password
5. Click "Use Password" to fill the form

### Searching Passwords
1. Type in the search bar
2. Results filter automatically as you type
3. Click "Clear" to show all passwords

### Copying to Clipboard
- Click the clipboard icon next to any username or password
- A toast notification confirms the copy

### Editing Passwords
1. Click "✏️ Edit" on any password card
2. Modify the fields
3. Click "Update"

### Deleting Passwords
1. Click "🗑️ Delete" on any password card
2. Type "DELETE" to confirm
3. The password is permanently removed

## Project Structure

```
Simple Password Manager/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── src/
│   ├── __init__.py           # VERSION and APP_NAME constants
│   ├── storage/
│   │   ├── __init__.py
│   │   └── manager.py        # PasswordManager (encryption, CRUD)
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── main_window.py    # Main application window
│   │   ├── login.py          # Login/setup screen
│   │   ├── dashboard.py      # Password list view
│   │   └── add_password.py   # Add/Edit form
│   └── components/
│       ├── __init__.py
│       └── generator.py      # Password generator
└── test files (optional)
```

## Security Features

- **Fernet Encryption** - AES-128-CBC with HMAC-SHA256 authentication
- **PBKDF2 Hashing** - 100,000 iterations for master password
- **Random Salts** - Each master password hash uses unique salt
- **Encrypted Storage** - All passwords encrypted in JSON file

## Technical Details

### Encryption
- Uses `cryptography` library's Fernet implementation
- Symmetric encryption with randomly generated key
- Key stored in `secret.key` file

### Master Password
- Hashed with PBKDF2-HMAC-SHA256
- 16-byte random salt per password
- 100,000 iterations for brute-force resistance
- Stored in `master.key` file

### Storage
- Passwords stored in `passwords.json`
- Entire file encrypted with Fernet
- Supports add, update, delete, search operations

## Development

### Running Tests
```bash
python test_manager.py      # Test storage operations
python test_generator.py    # Test password generator
```

### Code Structure
- **Beginner-friendly** - Simple classes and functions
- **Well-commented** - Every function has docstrings
- **No complex patterns** - Easy to understand and modify

## License

This is a student project for educational purposes.

## Version History

- **v1.0** - Initial release with all core features
