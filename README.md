# EZ Password Manager
#### A user-friendly local password management application

## Features
- **Modern Dark Mode UI** built with `CustomTkinter` and customizable UI scaling (`Default`, `Larger`, `Largest`)
- **Master Password Authentication** using `PBKDF2-HMAC-SHA256` (100,000 iterations) with a 30-second lockout after 5 failed attempts
- **Master-Password-Derived Encryption** using a SHA-256 counter-mode keystream and `HMAC-SHA256` integrity verification (no plaintext `secret.key` stored on disk)
- **Tamper Detection** — detects modified or corrupted `passwords.json` storage and refuses to unlock instead of overwriting data
- **Password Generator** with configurable length (4–64), character types, and strength indicator
- **Search & Clipboard** — debounced search by title or username, plus one-click copy to clipboard
- **Local-Only Storage** — stores `master.key` and encrypted `passwords.json` locally in the application directory

## Requirements
- Python 3.10+
- `customtkinter>=5.2.0`
- `pyperclip>=1.8.2`

## How to Run from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/PhenTitMesa/EZ-Password-Manager.git
   cd EZ-Password-Manager
