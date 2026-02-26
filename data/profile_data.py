# Step-by-step test data for Challenge #1.4: Update Profile
# Each dict maps to one sequential instruction shown in the app.
# Step 1 is confirmed from the live app. Steps 2–6 follow standard
# profile validation scripted-testing patterns covering:
#   - Valid profile (all fields filled correctly)
#   - Missing required fields (nickname, first name, last name)
#   - Invalid nickname format (spaces, special characters)
#   - Empty submission
# Run the challenge manually to confirm or adjust steps 2–6 if they differ.
#
# Common basic profile criteria tested by this form:
#   ✓ Nickname: required, alphanumeric, no spaces
#   ✓ First Name: required, letters only
#   ✓ Last Name: required, letters only

PROFILE_STEPS = [
    {
        "step": 1,
        "nickname": "skyline7",
        "first_name": "Michael",
        "last_name": "Henderson",
        "expected": "Your profile updated",
        "description": "valid profile — all fields correctly filled",
    },
    {
        "step": 2,
        "nickname": "",
        "first_name": "Michael",
        "last_name": "Henderson",
        "expected": "Invalid Profile",
        "description": "missing nickname",
    },
    {
        "step": 3,
        "nickname": "skyline7",
        "first_name": "",
        "last_name": "Henderson",
        "expected": "Invalid Profile",
        "description": "missing first name",
    },
    {
        "step": 4,
        "nickname": "skyline7",
        "first_name": "Michael",
        "last_name": "",
        "expected": "Invalid Profile",
        "description": "missing last name",
    },
    {
        "step": 5,
        "nickname": "sky line 7",
        "first_name": "Michael",
        "last_name": "Henderson",
        "expected": "Invalid Profile",
        "description": "nickname contains spaces",
    },
    {
        "step": 6,
        "nickname": "nova42",
        "first_name": "Sarah",
        "last_name": "Collins",
        "expected": "Your profile updated",
        "description": "valid profile with different user data",
    },
]
