---
id: 10
title: Fix authentication error messages
stage: misc
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5
feature: ai-todo-chatbot
branch: main
user: user
command: /sp.implement
labels: ["bugfix", "authentication", "error-handling", "ux"]
links:
  spec: null
  plan: null
  tasks: null
files:
  - phase-2-web/frontend/stores/authStore.ts
  - phase-2-web/backend/app/api/api_v1/endpoints/auth.py
tests: []
---

# Prompt

User reported authentication issues:
- Only user "shaziabashir604@gmail.com" with password "test123" can log in
- New login attempts get "invalid email or password" error
- Registration gives "Request failed with status code 409" error
- Browser console shows: "POST http://localhost:8080/api/v1/auth/register 409 (Conflict)"

# Response

## Root Cause Analysis

### Issue 1: Registration 409 Conflict
**Cause**: The email address is already registered in the database.

**Backend behavior** (auth.py:52-55):
```python
if existing_user:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email already registered"
    )
```

**Frontend issue**: The error message wasn't being extracted and displayed properly.

### Issue 2: Login Failures
**Cause**: Either:
1. User doesn't exist in database
2. Wrong password entered
3. Password hash mismatch

**Backend behavior** (auth.py:105-110):
```python
if not db_user or not verify_password(password, db_user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )
```

## Solution Implemented

### Frontend Fix (authStore.ts)

**Before:**
```typescript
catch (error: any) {
  throw new Error(error.message || 'Registration failed')
}
```

**After:**
```typescript
catch (error: any) {
  console.error('Registration error:', error)
  const errorMessage = error.response?.data?.detail || error.message || 'Registration failed'
  throw new Error(errorMessage)
}
```

**Changes:**
1. Extract `error.response?.data?.detail` to get backend error message
2. Add console.error for debugging
3. Accept both 200 and 201 status codes for successful registration

## User Instructions

### For Registration Errors (409 Conflict)

**Error message**: "Email already registered"

**Solution**:
1. The email is already in the database
2. Try logging in with that email instead
3. If you forgot the password, use password reset (if implemented)
4. Use a different email address to register

### For Login Errors (401 Unauthorized)

**Error message**: "Incorrect email or password"

**Possible causes**:
1. Email not registered - Register first
2. Wrong password - Check spelling and caps lock
3. Typo in email address

**Solution**:
1. Verify email address is correct
2. Check password (case-sensitive)
3. If new user, register first at /register

### Working Credentials

Currently working:
- Email: shaziabashir604@gmail.com
- Password: test123

## Testing

To test the fix:
1. Try registering with shaziabashir604@gmail.com → Should show "Email already registered"
2. Try registering with a new email → Should succeed
3. Try logging in with wrong password → Should show "Incorrect email or password"
4. Try logging in with correct credentials → Should succeed

## Technical Details

**Backend validation**:
- Password must be 6+ characters
- Password must be ≤72 bytes (bcrypt limit)
- Email must be unique
- Password is hashed with bcrypt

**Frontend improvements**:
- Better error message extraction
- Console logging for debugging
- User-friendly error display
