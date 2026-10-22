# Step-by-step test data for Challenge #1.1: Number Addition.
# Values and expected results are the instructions shown by the live challenge.

ADDER_STEPS = [
    {
        "step": 1,
        "first": "1",
        "second": "2",
        "expected": "3",
        "description": "basic positive addition",
    },
    {
        "step": 2,
        "first": "-2",
        "second": "4",
        "expected": "2",
        "description": "one number is negative",
    },
    {
        "step": 3,
        "first": "1.5",
        "second": "2.5",
        "expected": "4.0",
        "description": "decimal fractions",
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
        "first": "10000000000",
        "second": "1",
        "expected": "Application error",
        "description": "first number is too large",
    },
]
