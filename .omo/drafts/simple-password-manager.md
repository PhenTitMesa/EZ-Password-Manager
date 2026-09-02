---
slug: simple-password-manager
status: awaiting-approval
intent: clear
review_required: true
plan_path: .omo/plans/simple-password-manager.md
plan_sha256: null
review_round_id: null
pending-action: write and review .omo/plans/simple-password-manager.md
review:
  momus:
    status: pending
    workspace_root: null
    runtime_home: null
    target: .omo/plans/simple-password-manager.md
    round_id: null
    plan_sha256: null
    launch_id: null
    session: null
    result: null
  independent:
    status: pending
    workspace_root: null
    runtime_home: null
    target: .omo/plans/simple-password-manager.md
    round_id: null
    plan_sha256: null
    launch_id: null
    session: null
    result: null
approach: Build a complete password manager with master password login, JSON file storage, Fernet encryption, and modern CTK UI. Beginner-friendly code structure with comments explaining each part.
---

# Draft: simple-password-manager

## Components (topology ledger)
| id | outcome | status | evidence |
|---|---|---|---|
| C1 | Master password login screen | active | src/interface/login.py |
| C2 | Password storage + encryption layer | active | src/storage/manager.py |
| C3 | Dashboard + password list UI | active | src/interface/dashboard.py |
| C4 | Add/Edit password form | active | src/interface/add_password.py |
| C5 | Password generator utility | active | src/components/generator.py |
| C6 | Search functionality | active | src/interface/dashboard.py |

## Open assumptions (announced defaults)
| assumption | adopted default | rationale | reversible? |
|---|---|---|---|
| Encryption library | Fernet (cryptography) | Beginner-friendly, secure enough for school project | Yes |
| Storage format | JSON file | Simple, human-readable, easy to explain in presentation | Yes |
| UI framework | CustomTkinter | Already in project, modern look vs Tkinter | No |
| Password categories | Predefined list (Social, Email, Banking, Other) | Simple for beginners, avoids complex tree structure | Yes |
| Master password hashing | PBKDF2 with SHA-256 | Standard, secure, available in hashlib | Yes |

## Findings (cited - path:lines)
- src/interface/main_window.py:1-50 - Existing skeleton with CTK setup, dark theme, basic dashboard bar
- No requirements.txt or dependency management exists
- Empty components/ and storage/ directories ready for implementation
- Project has no commits yet, clean slate

## Decisions (with rationale)
1. **Fernet encryption** over raw AES - Fernet handles IV generation, padding, and authentication automatically; beginner doesn't need to understand crypto internals
2. **JSON over pickle** - JSON is human-readable (can demo the file), safer (no arbitrary code execution), and simpler to debug
3. **Single-file modules** - Each Python file does ONE thing; easy to explain in presentation and easy for beginner to navigate
4. **Predefined categories** - Avoids implementing a full category management system; keeps scope manageable for 3-5 days
5. **PBKDF2 for master password** - Standard key derivation, available in Python's built-in hashlib, no extra dependencies

## Scope IN
- Master password login screen with "Set Master Password" on first run
- Add, view, edit, delete password entries
- Each entry: title, username, password, category, notes, date created/modified
- Password generator (length, uppercase, lowercase, digits, symbols)
- Search/filter by title or username
- Copy password to clipboard
- Modern dark-themed CTK UI
- JSON file storage with Fernet encryption
- requirements.txt with all dependencies
- Well-commented code for presentation

## Scope OUT (Must NOT have)
- No cloud sync or network features
- No multi-user support
- No password strength meter (keeps it simple)
- No import/export (out of scope for school project)
- No browser integration
- No two-factor authentication
- No password history/audit log
- No complex OOP patterns (keep it procedural/simple classes)

## Open questions
None - all forks resolved via user answers and best-practice defaults.

## Approval gate
status: awaiting-approval
<!-- Exploration complete, all unknowns resolved. Awaiting user approval to write the plan. -->
