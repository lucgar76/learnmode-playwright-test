# Step-by-step test data for Challenge #1.3: Password Restore
# Each dict maps to one sequential instruction shown in the app.
# Step 1 is confirmed from the live app. Steps 2–11 follow standard
# password validation scripted-testing patterns covering:
#   - Valid passwords (all criteria met)
#   - Missing uppercase / lowercase / digit / special character
#   - Too short (< 8 chars)
#   - Empty input
#   - Whitespace only
#   - Boundary: exactly 8 chars meeting all criteria
# Run the challenge manually to confirm or adjust steps 2–11 if they differ.
#
# Common basic password criteria tested by this form:
#   ✓ At least 8 characters
#   ✓ At least one uppercase letter (A–Z)
#   ✓ At least one lowercase letter (a–z)
#   ✓ At least one digit (0–9)
#   ✓ At least one special character (!@#$%^&* etc.)

PASSWORD_STEPS = [
    {
        "step": 1,
        "password": "P@ssw0rD",
        "expected": "Valid Password",
        "description": "valid password meeting all criteria",
    },
    {
        "step": 2,
        "password": "password1!",
        "expected": "Invalid Password",
        "description": "missing uppercase letter",
    },
    {
        "step": 3,
        "password": "PASSWORD1!",
        "expected": "Invalid Password",
        "description": "missing lowercase letter",
    },
    {
        "step": 4,
        "password": "P@ssword",
        "expected": "Invalid Password",
        "description": "missing digit",
    },
    {
        "step": 5,
        "password": "Passw0rd",
        "expected": "Invalid Password",
        "description": "missing special character",
    },
    {
        "step": 6,
        "password": "P@s1",
        "expected": "Invalid Password",
        "description": "too short (less than 8 characters)",
    },
    {
        "step": 7,
        "password": "",
        "expected": "Invalid Password",
        "description": "empty password",
    },
    {
        "step": 8,
        "password": "        ",
        "expected": "Invalid Password",
        "description": "whitespace only",
    },
    {
        "step": 9,
        "password": "Ab1!Ab1!",
        "expected": "Valid Password",
        "description": "exactly 8 characters meeting all criteria",
    },
    {
        "step": 10,
        "password": "12345678",
        "expected": "Invalid Password",
        "description": "digits only, no letters or special character",
    },
    {
        "step": 11,
        "password": "Str0ng!P@ssw0rd",
        "expected": "Valid Password",
        "description": "long valid password with multiple special chars",
    },
]
