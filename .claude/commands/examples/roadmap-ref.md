# Implementation Roadmap Reference

> This is a condensed reference showing the EXACT structure for generated roadmaps.

## Structure Overview

```
1. Progress Overview
   - Last updated date
   - Current status
   - Commits completed (X/Y)
   - Branch name (if applicable)

2. Now/Next/Later Section
   - 🔥 NOW: Current focus
   - ⏭️ NEXT: Up coming
   - 📅 LATER: Remaining work

3. Detailed Commit Plan
   - One section per commit
   - Status indicators (✅ Done, 🚧 In Progress, ⏳ Todo)
   - Objectives, key files, acceptance criteria
   - Completion notes (added after finishing)

4. Known Blockers & Risks

5. Session Notes (living log of progress)
```

---

## Example Roadmap

```markdown
# [Project Name] Implementation Roadmap

> **Living Document**: Updated after each commit to track progress across conversation resets.

## 📊 Progress Overview

**Last Updated**: YYYY-MM-DD
**Current Status**: In Progress
**Commits Completed**: 2/6
**Branch**: feature/branch-name

---

## 🎯 Now / Next / Later

### 🔥 NOW (Current Focus)
- **Commit 3**: [Title of current commit]

### ⏭️ NEXT (Up Coming)
- **Commit 4**: [Next commit title]
- **Commit 5**: [Following commit title]

### 📅 LATER (Remaining Work)
- **Commits 6+**: [Brief summary of remaining work]

---

## 📋 Detailed Commit Plan

### ✅ Commit 1: [Title]
**Status**: ✅ Done
**Priority**: Critical | High | Medium | Low
**Estimated Effort**: [time estimate]

**Objectives**:
- [Objective 1]
- [Objective 2]

**Key Files**:
- path/to/file1.ext - [Description]
- path/to/file2.ext - [Description]

**Acceptance Criteria**:
- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

**Risks**: [Any identified risks or none]
**Blockers**: [Dependencies or none]

**Completion Notes**:
- [What was actually done]
- [Any deviations from plan]
- [Issues encountered and resolved]
- [Commit hash if applicable]
- [Actual time taken vs estimate]

---

### 🚧 Commit 2: [Title]
**Status**: 🚧 In Progress
**Priority**: Critical
**Estimated Effort**: 45 min

**Objectives**:
- [What needs to be done]

**Key Files**:
- path/to/file.ext

**Acceptance Criteria**:
- [ ] Criterion 1
- [x] Criterion 2 (if partially done)
- [ ] Criterion 3

**Risks**: [Any concerns]
**Blockers**: None

**Completion Notes**: _[Add notes when complete]_

---

### ⏳ Commit 3: [Title]
**Status**: ⏳ Todo
**Priority**: High
**Estimated Effort**: 30 min

**Objectives**:
- [Future work]

**Key Files**:
- path/to/file.ext

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Risks**: None
**Blockers**: Depends on Commit 2

**Completion Notes**: _[Add notes after completing]_

---

## 🚧 Known Blockers & Risks

**Active Blockers**:
- None

**Risks to Monitor**:
- [Risk 1 and mitigation strategy]
- [Risk 2 and mitigation strategy]

---

## 📝 Session Notes

### Session 1: YYYY-MM-DD
- Created initial roadmap
- ✅ Completed Commit 1: [Title]
  - [Detail 1]
  - [Detail 2]
  - Commit hash: `abc123`
- 🚧 Started Commit 2: [Title]
  - [Progress made]
  - [What's left]

### Session 2: YYYY-MM-DD
- ✅ Completed Commit 2: [Title]
  - [What was done]
  - [Issues resolved]
- ⏳ Next: Commit 3

---

## 🔄 Update Instructions for Future Sessions

**When resuming in a new session:**
1. Read this file to understand current progress
2. Check which commits are ✅ Done, 🚧 In Progress, ⏳ Todo
3. Continue from the first incomplete commit

**After completing each commit:**
1. Update commit status: ⏳ Todo → ✅ Done
2. Check all acceptance criteria boxes [x]
3. Add completion notes (what was done, issues found, decisions made)
4. Update "Progress Overview" section (commits completed count)
5. Update "Now / Next / Later" section
6. Add entry to "Session Notes"
7. Git commit this ROADMAP.md file

**Status Indicators**:
- ⏳ Todo - Not started
- 🚧 In Progress - Currently working
- ✅ Done - Completed and committed
- ⚠️ Blocked - Waiting on dependency
- ❌ Skipped - Decided not to implement
```

---

## Full Example: Authentication System Roadmap

```markdown
# Authentication System Implementation Roadmap

> **Living Document**: Updated after each commit to track progress.

## 📊 Progress Overview

**Last Updated**: 2025-10-03
**Current Status**: In Progress
**Commits Completed**: 1/3
**Branch**: feature/jwt-auth

---

## 🎯 Now / Next / Later

### 🔥 NOW (Current Focus)
- **Commit 2**: Registration & Login Endpoints

### ⏭️ NEXT (Up Coming)
- **Commit 3**: JWT Middleware

### 📅 LATER (Remaining Work)
- Testing and documentation

---

## 📋 Detailed Commit Plan

### ✅ Commit 1: Database Models & Schema
**Status**: ✅ Done
**Priority**: Critical
**Estimated Effort**: 45 min

**Objectives**:
- Create User model with email, password_hash, created_at
- Set up database migration
- Implement password hashing utilities

**Key Files**:
- models/user.py - User model definition
- alembic/versions/001_create_users.py - Database migration
- utils/crypto.py - Password hashing utilities

**Acceptance Criteria**:
- [x] Migration runs successfully
- [x] User model has all required fields
- [x] Password hashing uses bcrypt cost 12
- [x] Email uniqueness enforced at database level

**Risks**: None
**Blockers**: None

**Completion Notes**:
- Implemented User model with SQLAlchemy
- Created Alembic migration with unique constraint on email
- Added bcrypt hashing in utils/crypto.py with cost factor 12
- All tests pass (5 new tests added)
- Actual time: 40 minutes (under estimate)
- Commit hash: `a3f8c92`

---

### 🚧 Commit 2: Registration & Login Endpoints
**Status**: 🚧 In Progress
**Priority**: Critical
**Estimated Effort**: 60 min

**Objectives**:
- Create registration endpoint
- Create login endpoint with JWT generation
- Add input validation
- Handle errors properly

**Key Files**:
- routes/auth.py - Auth endpoints
- utils/jwt.py - JWT generation/validation
- schemas/auth.py - Pydantic request/response models

**Acceptance Criteria**:
- [x] Registration endpoint creates user
- [x] Password properly hashed on registration
- [ ] Login endpoint returns JWT token
- [ ] Invalid credentials return 401
- [ ] Duplicate email returns 409

**Risks**: JWT secret key management
**Blockers**: None

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 3: JWT Middleware
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 45 min

**Objectives**:
- Create JWT validation middleware
- Protect all routes except public ones
- Extract user from token

**Key Files**:
- middleware/auth.py - JWT middleware
- main.py - Wire middleware

**Acceptance Criteria**:
- [ ] Protected endpoints require valid JWT
- [ ] Expired tokens return 401
- [ ] User context available in routes

**Risks**: Performance impact of middleware
**Blockers**: Depends on Commit 2 (JWT generation)

**Completion Notes**: _[Add notes after completing]_

---

## 🚧 Known Blockers & Risks

**Active Blockers**: None

**Risks to Monitor**:
- JWT secret key storage (use environment variable, not hardcode)
- Token expiration edge cases (timezone handling)
- Rate limiting on auth endpoints (add in future)

---

## 📝 Session Notes

### Session 1: 2025-10-03 (Morning)
- Created initial roadmap structure
- ✅ Completed Commit 1: Database Models & Schema
  - User model implementation clean
  - Migration tested on fresh database
  - Password hashing verified with test vectors
  - Commit hash: `a3f8c92`
  - Quality checks: All pass (pytest, mypy, ruff)

### Session 1: 2025-10-03 (Afternoon)
- 🚧 Started Commit 2: Registration & Login Endpoints
  - Created routes/auth.py with registration endpoint
  - Added Pydantic schemas for request/response validation
  - Registration endpoint working and tested
  - Next: Implement login endpoint with JWT generation

---

## 🔄 Update Instructions

[Standard update instructions as shown above]
```

---

## Key Patterns

**Progress Tracking:**
- Always update after each commit
- Use emoji status indicators consistently
- Keep "Now/Next/Later" section current

**Completion Notes:**
- Write them immediately after finishing
- Include actual vs estimated time
- Note any deviations or issues
- Add commit hashes for traceability

**Session Notes:**
- Date each session
- Log what was completed
- Note decisions made
- Capture blockers encountered

**Acceptance Criteria:**
- Start as `[ ]` unchecked
- Mark `[x]` as completed
- Keep list visible to track progress
