# Step-by-step test data for Challenge #1.4: Update Profile.
# Values and expected results are the instructions shown by the live challenge.

PROFILE_STEPS = [
    {
        "step": 1,
        "nickname": "skyline7",
        "first_name": "Michael",
        "last_name": "Henderson",
        "expected": "Your profile updated",
        "description": "valid profile",
    },
    {
        "step": 2,
        "nickname": "k_3",
        "first_name": "J",
        "last_name": "Z",
        "expected": "User input error",
        "description": "shorter than the minimum length",
    },
    {
        "step": 3,
        "nickname": "longnick9_",
        "first_name": "MaximilianaElizabethMontgomery",
        "last_name": "AlexanderHamiltonJeffersonSmith",
        "expected": "User input error",
        "description": "longer than the maximum length",
    },
    {
        "step": 4,
        "nickname": "",
        "first_name": "",
        "last_name": "",
        "expected": "User input error",
        "description": "all fields empty",
    },
    {
        "step": 5,
        "nickname": "123-AA",
        "first_name": "X Æ A-12",
        "last_name": "X Æ A-12",
        "expected": "User input error",
        "description": "disallowed characters in every field",
    },
    {
        "step": 6,
        "nickname": "@@@@@",
        "first_name": "Christopher",
        "last_name": "Williams",
        "expected": "User input error",
        "description": "disallowed characters in the nickname",
    },
]
