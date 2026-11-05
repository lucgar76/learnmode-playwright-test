# Step-by-step test data for Challenge #1.2: Number Division.
# Values and expected results are the instructions shown by the live challenge.

DIVIDER_STEPS = [
    {
        "step": 1,
        "first": "4",
        "second": "2",
        "expected": "2",
        "description": "basic positive division",
    },
    {
        "step": 2,
        "first": "-10",
        "second": "2",
        "expected": "-5",
        "description": "negative dividend",
    },
    {
        "step": 3,
        "first": "5",
        "second": "2",
        "expected": "2.5",
        "description": "decimal fraction result",
    },
    {
        "step": 4,
        "first": "abc",
        "second": "1",
        "expected": "User input error",
        "description": "non-numeric first number",
    },
    {
        "step": 5,
        "first": "",
        "second": "",
        "expected": "User input error",
        "description": "both fields blank",
    },
    {
        "step": 6,
        "first": "10",
        "second": "0",
        "expected": "Application error",
        "description": "divide by zero",
    },
]
