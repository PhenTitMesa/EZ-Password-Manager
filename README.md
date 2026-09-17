# EZ Password Manager
#### A user-friendly password management application

## Features:
- Made with CustomTkinter for the UI
- Master password login with `PBKDF2` for hashing
- A password generator
- Search name/category and copy password to clipboard
- Default with Dark Mode UI and a customizable GUI scale
- Encrypted password storage, it stores inside your `C:\Users\%USERNAME%\AppData\Local\EZManagerStorage`
- If you forget your login password - you can delete `master.key` inside `C:\Users\%USERNAME%\AppData\Local\EZManagerStorage` then you can register back and use your password as normal.

# Instruction
## How to use the app (Release Download)
- Download the `EZ-Password-Manager.zip`
- After that, extract the `zip`
- Finally, double-click `EZ Password Manager.exe` to launch the app

## How to use the app (Source Code Method)
- Must have Python 3.8+
- Inside the app directory do `pip install -r requirements.txt` in the command prompt.
- Then, do `python main.py`
