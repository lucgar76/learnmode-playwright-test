# Step-by-step test data for Challenge #1.2: Number Division
# Each dict maps to one sequential instruction shown in the app.
# Step 1 is confirmed from the live app. Steps 2–6 follow standard
# scripted-testing patterns for division (positive, zero dividend,
# negative, decimal, divide by 1, large numbers).
# Run the challenge manually to confirm or adjust steps 2–6 if they differ.

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
        "first": "0",
        "second": "5",
        "expected": "0",
        "description": "zero dividend",
    },
    {
        "step": 3,
        "first": "-10",
        "second": "2",
        "expected": "-5",
        "description": "negative dividend divided by positive",
    },
    {
        "step": 4,
        "first": "9",
        "second": "3",
        "expected": "3",
        "description": "exact integer division",
    },
    {
        "step": 5,
        "first": "10",
        "second": "0",
        "expected": "Error",
        "description": "divide by zero returns error",
    },
    {
        "step": 6,
        "first": "7",
        "second": "2",
        "expected": "3.5",
        "description": "division with decimal result",
    },
]
