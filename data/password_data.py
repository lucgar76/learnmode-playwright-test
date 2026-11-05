# Step-by-step test data for Challenge #1.3: Password Restore.
# Values and expected results are the instructions shown by the live challenge.

PASSWORD_STEPS = [
    {
        "step": 1,
        "password": "P@ssw0rD",
        "expected": "Valid password",
        "description": "meets all requirements",
    },
    {
        "step": 2,
        "password": "hElloW0rld",
        "expected": "Invalid password",
        "description": "does not meet all requirements",
    },
    {
        "step": 3,
        "password": "Passw0rd!7",
        "expected": "Invalid password",
        "description": "same as the saved password",
    },
    {
        "step": 4,
        "password": "",
        "expected": "Invalid password",
        "description": "empty password",
    },
    {
        "step": 5,
        "password": "Mo7%",
        "expected": "Invalid password",
        "description": "shorter than 5 characters",
    },
    {
        "step": 6,
        "password": "asdfghjklpoiuytrewq",
        "expected": "Invalid password",
        "description": "longer than 15 characters",
    },
    {
        "step": 7,
        "password": "ONLYCAPITAL",
        "expected": "Invalid password",
        "description": "uppercase letters only",
    },
    {
        "step": 8,
        "password": "onlylower",
        "expected": "Invalid password",
        "description": "lowercase letters only",
    },
    {
        "step": 9,
        "password": "001122",
        "expected": "Invalid password",
        "description": "digits only",
    },
    {
        "step": 10,
        "password": "@@@@@",
        "expected": "Invalid password",
        "description": "special characters only",
    },
    {
        "step": 11,
        "password": "Κωδικός",
        "expected": "Invalid password",
        "description": "disallowed characters",
    },
]
