# Implementation Playbook Reference

> This is a condensed reference showing the EXACT structure for generated playbooks.

## Structure Overview

```
1. Master Agent Profile
   - Role definition
   - Non-negotiables/Rules
   - Workflow rules (quality checks, progress tracking)
   - Goal statement

2. Commit Task Cards (6-12 commits)
   - Each card: numbered commit with title
   - Tasks (2-5 concrete tasks)
   - Key files to create/modify
   - Acceptance criteria
   - "Stop and report" instruction

3. Session Handoff (optional)
   - How to update progress
   - How to resume after reset
```

---

## Example Master Agent Profile

```markdown
# Master Agent Profile: [Project Name]

## Role
You are **Claude Code** implementing [project name] exactly as defined in:
- [Reference doc 1]
- [Reference doc 2]

## Non-Negotiables
- [Key rule 1]
- [Key rule 2]
- [Key rule 3]

## Workflow Rules
- **Progress Tracking**:
  - Read ROADMAP.md to understand current progress
  - Update ROADMAP.md after each commit
- Work **commit-by-commit** (don't skip ahead)
- **After each commit (MANDATORY QUALITY CHECKS)**:
  1. Run quality checks (tests, linting, type checking)
  2. Verify acceptance criteria
  3. If checks pass: commit with conventional commit message
  4. Update ROADMAP.md with completion notes
  5. Stop and wait for next commit card

## Goal
[What success looks like - concrete acceptance criteria]

---

## Immediately do this (session initialization)
1. Read ROADMAP.md to understand current progress
2. Report which commits are done, which is next
3. Wait for user to provide commit card
```

---

## Example Commit Card Format

```markdown
### Commit 1 — [Descriptive Title]

# Commit 1: [Title]

Tasks:
- [Concrete task 1]
- [Concrete task 2]
- [Concrete task 3]

Key Files:
- path/to/file1.ext
- path/to/file2.ext

Acceptance:
- [Verifiable criterion 1]
- [Verifiable criterion 2]

Quality Checks:
- Run [test command] - Must pass
- Run [lint command] - Must pass
- Run [typecheck command] - Must pass
- Verify acceptance criteria above

Stop and report.
```

---

## Technology-Specific Quality Checks

**Python:**
```
1. Run `pytest` - All tests must pass
2. Run `mypy .` - Type checking must pass
3. Run `ruff check .` - Linting must pass
4. Verify acceptance criteria
```

**Node.js/TypeScript:**
```
1. Run `npm test` or `bun run test` - All tests must pass
2. Run `tsc --noEmit` or `bun run typecheck` - TypeScript must compile
3. Run `npm run lint` or `bun run lint` - ESLint must pass
4. Verify acceptance criteria
```

**Go:**
```
1. Run `go test ./...` - All tests must pass
2. Run `go build ./...` - Code must compile
3. Run `golangci-lint run` - Linting must pass
4. Verify acceptance criteria
```

**Rust:**
```
1. Run `cargo test` - All tests must pass
2. Run `cargo build` - Code must compile
3. Run `cargo clippy` - Linting must pass
4. Verify acceptance criteria
```

---

## Full Example: 3-Commit Playbook

```markdown
# Master Agent Profile: Authentication System

## Role
Implement secure authentication system with JWT tokens and password hashing.

## Non-Negotiables
- All passwords must be bcrypt hashed (cost factor 12)
- JWT tokens expire after 24 hours
- All endpoints require authentication except /login and /register
- Input validation on all user inputs

## Workflow Rules
- Read ROADMAP.md for progress tracking
- Work commit-by-commit
- After each commit:
  1. Run `pytest` - Must pass
  2. Run `mypy .` - Must pass
  3. Run `ruff check .` - Must pass
  4. Update ROADMAP.md
  5. Stop and wait

## Goal
Complete authentication system with user registration, login, JWT validation, and password reset.

---

## Commit 1: Database Models & Schema

# Commit 1: Database Models

Tasks:
- Create User model in `models/user.py` with email, password_hash, created_at
- Create database migration with Alembic
- Add unique constraint on email field
- Create password hashing utilities in `utils/crypto.py`

Key Files:
- models/user.py (new)
- alembic/versions/001_create_users.py (new)
- utils/crypto.py (new)

Acceptance:
- Migration runs successfully
- User model has all required fields
- Password hashing works with bcrypt cost 12
- Email uniqueness enforced at database level

Quality Checks:
- pytest - All tests pass
- mypy . - Type checking passes
- ruff check . - Linting passes

Stop and report.

---

## Commit 2: Registration & Login Endpoints

# Commit 2: Auth Endpoints

Tasks:
- Create `/register` POST endpoint in `routes/auth.py`
- Create `/login` POST endpoint with JWT generation
- Add input validation (email format, password strength)
- Add error handling for duplicate emails

Key Files:
- routes/auth.py (new)
- utils/jwt.py (new)
- schemas/auth.py (new - Pydantic models)

Acceptance:
- Registration creates user with hashed password
- Login returns JWT token valid for 24 hours
- Invalid credentials return 401
- Duplicate email returns 409

Quality Checks:
- pytest - All tests pass
- mypy . - Type checking passes
- ruff check . - Linting passes

Stop and report.

---

## Commit 3: JWT Middleware

# Commit 3: JWT Middleware

Tasks:
- Create JWT validation middleware in `middleware/auth.py`
- Protect all routes except /login and /register
- Extract user from token and add to request context
- Handle expired/invalid tokens gracefully

Key Files:
- middleware/auth.py (new)
- main.py (modify - add middleware)

Acceptance:
- Protected endpoints require valid JWT
- Expired tokens return 401
- Invalid tokens return 401
- User context available in protected routes

Quality Checks:
- pytest - All tests pass
- mypy . - Type checking passes
- ruff check . - Linting passes

Stop and report.
```

---

## Key Patterns

**Commit Titles:** Use descriptive, action-oriented names
- ✅ "Database Models & Schema"
- ✅ "Registration & Login Endpoints"
- ❌ "Setup"
- ❌ "Changes"

**Tasks:** Concrete, actionable items
- ✅ "Create User model in models/user.py with email, password_hash"
- ❌ "Add user stuff"

**Acceptance Criteria:** Verifiable conditions
- ✅ "Migration runs successfully"
- ✅ "Invalid credentials return 401"
- ❌ "Everything works"

**Quality Checks:** Must match project technology stack
- Detect from planning docs (imports, dependencies, file extensions)
- Use appropriate commands for the language/framework
- Always include: tests, linting, type checking (if applicable)
