# simple-password-manager - Work Plan

## TL;DR (For humans)
<!-- Fill this LAST, after the detailed plan below is written, so it summarizes the REAL plan. -->

**What you'll get:** A complete, working password manager application with modern CustomTkinter UI, master password login, encrypted JSON storage, password generator, and search functionality - all with beginner-friendly code you can explain in your presentation.

**Why this approach:** Using CustomTkinter for modern UI (standing out from Tkinter projects), Fernet encryption for security (beginner-friendly API), and JSON for storage (simple to understand and demo). Single-file modules keep code organized and easy to explain.

**What it will NOT do:** No cloud sync, no multi-user support, no browser integration, no complex OOP patterns - keeping it focused and presentable for a school project.

**Effort:** Medium
**Risk:** Low - straightforward Python project with well-documented libraries

**Decisions to sanity-check:**
1. Fernet encryption (cryptography library) vs raw AES - Fernet is simpler and safer for beginners
2. Predefined categories (Social, Email, Banking, Other) vs dynamic category management
3. PBKDF2 for master password hashing (built-in hashlib) vs bcrypt (requires extra dependency)

Your next move: Run `$start-work simple-password-manager` to execute this plan in a worker session. Or run a high-accuracy review first with `/review`.

---

> TL;DR (machine): Medium effort, Low risk - complete password manager with CTK UI, master password login, encrypted JSON storage, password generator, and search. 7 implementation tasks + 4 final verification tasks across 3 waves.

## Scope
### Must have
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

### Must NOT have (guardrails, anti-slop, scope boundaries)
- No cloud sync or network features
- No multi-user support
- No password strength meter
- No import/export functionality
- No browser integration
- No two-factor authentication
- No password history/audit log
- No complex OOP patterns (keep it procedural/simple classes)
- No external databases (SQLite, PostgreSQL, etc.)
- No async/await patterns (keep it synchronous for simplicity)

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after + manual QA
- Evidence: .omo/evidence/ulw/<session>/<goalId>/a<attempt>/

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means under-split.

**Wave 1:** Foundation (storage layer + encryption + project setup)
**Wave 2:** Core UI (login + dashboard + password management)
**Wave 3:** Features + Polish (generator + search + clipboard + final touches)

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
|---|---|---|---|
| 1. Project setup + requirements.txt | None | All others | None |
| 2. Encryption layer (storage/manager.py) | 1 | 3, 4, 5 | None |
| 3. Master password system | 2 | 4 | None |
| 4. Password CRUD operations | 2 | 5, 6 | 3 |
| 5. Login screen UI | 3 | 6 | 4 |
| 6. Dashboard + password list UI | 4, 5 | 7 | None |
| 7. Add/Edit password form UI | 6 | 8 | None |
| 8. Password generator | None | 9 | 6, 7 |
| 9. Search + clipboard + polish | 6, 7, 8 | F1-F4 | None |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->

- [x] 1. Project setup + requirements.txt
  What to do / Must NOT do: Create requirements.txt with customtkinter, cryptography, and pyperclip. Create src/__init__.py with proper imports. Set up project structure with empty placeholder files in components/ and storage/. Do NOT install packages yet - just document them.
  Parallelization: Wave 1 | Blocked by: None | Blocks: 2-9
  References: src/__init__.py (empty), src/interface/main_window.py (existing CTK setup)
  Acceptance criteria (agent-executable): requirements.txt exists with correct packages, all __init__.py files exist, project structure is complete
  QA scenarios (name the exact tool + invocation): happy - run `pip install -r requirements.txt` successfully; failure - verify error message if package name is wrong. Evidence .omo/evidence/ulw/simple-password-manager/task-1.txt
  Commit: Y | feat(project): add project setup and dependencies

- [x] 2. Encryption layer (storage/manager.py)
  What to do / Must NOT do: Create src/storage/__init__.py and src/storage/manager.py. Implement PasswordManager class with: generate_key() using Fernet, encrypt_data() and decrypt_data() methods, save_to_file() and load_from_file() for JSON storage, hash_password() using PBKDF2. Do NOT implement UI logic - only storage operations.
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 3, 4, 5
  References: src/storage/ (empty directory), requirements.txt (cryptography package)
  Acceptance criteria (agent-executable): PasswordManager class exists, all methods work correctly, encryption/decryption round-trip test passes
  QA scenarios (name the exact tool + invocation): happy - create PasswordManager, encrypt "test" data, decrypt and verify matches; failure - try to decrypt with wrong key, verify error. Evidence .omo/evidence/ulw/simple-password-manager/task-2.txt
  Commit: Y | feat(storage): add encryption layer with Fernet

- [x] 3. Master password system
  What to do / Must NOT do: Extend PasswordManager with: set_master_password() that hashes and stores, verify_master_password() that checks input, is_master_set() to check if password exists. Store master password hash in separate file (master.key). Do NOT create UI - only backend logic.
  Parallelization: Wave 1 | Blocked by: 2 | Blocks: 4, 5
  References: src/storage/manager.py (PasswordManager class)
  Acceptance criteria (agent-executable): master password can be set, verified, and checked; hash is stored securely
  QA scenarios (name the exact tool + invocation): happy - set master password, verify correct password returns True, wrong returns False; failure - try to set master password twice, verify it doesn't overwrite. Evidence .omo/evidence/ulw/simple-password-manager/task-3.txt
  Commit: Y | feat(storage): add master password system

- [x] 4. Password CRUD operations
  What to do / Must NOT do: Extend PasswordManager with: add_password(entry), get_password(id), get_all_passwords(), update_password(id, entry), delete_password(id), search_passwords(query). Each entry is a dict with: id, title, username, password, category, notes, created_date, modified_date. Store in passwords.json (encrypted).
  Parallelization: Wave 1 | Blocked by: 2 | Blocks: 5, 6
  References: src/storage/manager.py (PasswordManager class)
  Acceptance criteria (agent-executable): all CRUD operations work, search returns correct results, entries have all required fields
  QA scenarios (name the exact tool + invocation): happy - add 3 passwords, search for one, update it, delete it, verify changes; failure - try to get password with invalid ID, verify error handling. Evidence .omo/evidence/ulw/simple-password-manager/task-4.txt
  Commit: Y | feat(storage): add password CRUD operations

- [x] 5. Login screen UI
  What to do / Must NOT do: Create src/interface/login.py with LoginWindow class using CTK. Show "Set Master Password" form on first run (two input fields + confirm button). Show "Enter Master Password" form on subsequent runs (one input field + login button). Use dark theme matching main_window.py. Handle success (open main window) and failure (show error message).
  Parallelization: Wave 2 | Blocked by: 3, 4 | Blocks: 6
  References: src/interface/main_window.py (existing CTK setup, dark theme), src/storage/manager.py (master password methods)
  Acceptance criteria (agent-executable): login window appears, master password can be set on first run, login works on subsequent runs, error message shows for wrong password
  QA scenarios (name the exact tool + invocation): happy - run app, set master password, close, reopen, login successfully; failure - enter wrong password, verify error appears. Evidence .omo/evidence/ulw/simple-password-manager/task-5.txt
  Commit: Y | feat(interface): add login screen with master password

- [x] 6. Dashboard + password list UI
  What to do / Must NOT do: Create src/interface/dashboard.py with DashboardWindow class using CTK. Show list of all passwords in a scrollable frame (title, username, category, copy button). Add "Add New Password" button. Add search bar at top. Use dark theme. Handle empty state (no passwords yet). Include edit/delete buttons for each entry.
  Parallelization: Wave 2 | Blocked by: 4, 5 | Blocks: 7
  References: src/interface/main_window.py (existing Dashboard class), src/storage/manager.py (get_all_passwords, search_passwords)
  Acceptance criteria (agent-executable): dashboard shows password list, search works, add button exists, edit/delete buttons exist, empty state shows message
  QA scenarios (name the exact tool + invocation): happy - add passwords via backend, verify they appear in dashboard, search works; failure - verify empty state when no passwords. Evidence .omo/evidence/ulw/simple-password-manager/task-6.txt
  Commit: Y | feat(interface): add dashboard with password list

- [x] 7. Add/Edit password form UI
  What to do / Must NOT do: Create src/interface/add_password.py with AddPasswordWindow class using CTK. Form fields: title, username, password (with show/hide toggle), category (dropdown), notes (text area). Include "Generate Password" button that opens generator. Handle both add and edit modes. Validate required fields (title, username, password). Save to storage on submit.
  Parallelization: Wave 2 | Blocked by: 6 | Blocks: 8, 9
  References: src/interface/dashboard.py (add button), src/storage/manager.py (add_password, update_password)
  Acceptance criteria (agent-executable): form appears, all fields work, validation shows errors for empty required fields, save works for both add and edit modes
  QA scenarios (name the exact tool + invocation): happy - fill form, save, verify password appears in dashboard; failure - leave title empty, submit, verify error message. Evidence .omo/evidence/ulw/simple-password-manager/task-7.txt
  Commit: Y | feat(interface): add password form with validation

- [x] 8. Password generator
  What to do / Must NOT do: Create src/components/generator.py with PasswordGenerator class. Methods: generate_password(length, use_uppercase, use_lowercase, use_digits, use_symbols). Use secrets module for secure random generation. Create simple popup window with generator UI (length slider, checkboxes for character types, generate button, copy button). Integrate with AddPasswordWindow.
  Parallelization: Wave 3 | Blocked by: 7 | Blocks: 9
  References: src/interface/add_password.py (generate password button), requirements.txt (secrets is built-in)
  Acceptance criteria (agent-executable): generator creates passwords with correct length and character types, popup works, copy to clipboard works
  QA scenarios (name the exact tool + invocation): happy - generate 5 passwords, verify they meet criteria; failure - try to generate with no character types selected, verify error. Evidence .omo/evidence/ulw/simple-password-manager/task-8.txt
  Commit: Y | feat(components): add password generator

- [x] 9. Search + clipboard + final polish
  What to do / Must NOT do: Add search functionality to dashboard (filter by title/username). Add copy-to-clipboard buttons for username and password fields. Add "Password copied!" tooltip/notification. Add window icons. Add version label. Test full user flow: login -> add password -> search -> copy -> edit -> delete. Add comments explaining code for presentation.
  Parallelization: Wave 3 | Blocked by: 6, 7, 8 | Blocks: F1-F4
  References: src/interface/dashboard.py, src/interface/add_password.py, src/interface/main_window.py
  Acceptance criteria (agent-executable): search filters correctly, copy works, tooltip shows, full user flow works end-to-end
  QA scenarios (name the exact tool + invocation): happy - complete user flow test, verify all features work; failure - search for non-existent term, verify empty results. Evidence .omo/evidence/ulw/simple-password-manager/task-9.txt
  Commit: Y | feat(interface): add search, clipboard, and polish

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [ ] F1. Plan compliance audit - Verify all 9 tasks completed, all Must-Have features present, no Must-NOT-Have items included
- [ ] F2. Code quality review - Check code is beginner-friendly, well-commented, no complex patterns, proper naming conventions
- [ ] F3. Real manual QA - Run the app, test complete user flow: set master password -> login -> add password -> search -> copy -> edit -> delete -> logout -> login again
- [ ] F4. Scope fidelity - Confirm no network features, no multi-user, no extra dependencies, JSON storage works correctly

## Commit strategy
- Wave 1: feat(project): add project setup and dependencies, feat(storage): add encryption layer, feat(storage): add master password system, feat(storage): add password CRUD operations
- Wave 2: feat(interface): add login screen, feat(interface): add dashboard with password list, feat(interface): add password form with validation
- Wave 3: feat(components): add password generator, feat(interface): add search, clipboard, and polish
- Final: chore(project): final cleanup and documentation

## Success criteria
- App launches and shows login screen
- Master password can be set on first run
- Login works with correct password, fails with wrong password
- Passwords can be added, viewed, edited, deleted
- Search filters passwords correctly
- Password generator creates passwords with user-specified criteria
- Copy to clipboard works
- UI is modern and dark-themed (stands out from Tkinter)
- Code is well-commented and beginner-friendly
- All dependencies documented in requirements.txt
