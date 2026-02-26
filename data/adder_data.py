# Step-by-step test data for Challenge #1.1: Number Addition
# Each dict maps to one sequential instruction shown in the app.
# Step 1 is confirmed from the live app. Steps 2–6 follow standard
# scripted-testing patterns (positive, zero, negative, decimal, large).
# Run the challenge manually to confirm or adjust steps 2–6 if they differ.

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
        "first": "0",
        "second": "0",
        "expected": "0",
        "description": "both inputs are zero",
    },
    {
        "step": 3,
        "first": "-1",
        "second": "1",
        "expected": "0",
        "description": "negative plus positive equals zero",
    },
    {
        "step": 4,
        "first": "10",
        "second": "20",
        "expected": "30",
        "description": "two-digit positive numbers",
    },
    {
        "step": 5,
        "first": "-5",
        "second": "-3",
        "expected": "-8",
        "description": "negative plus negative",
    },
    {
        "step": 6,
        "first": "1.5",
        "second": "2.5",
        "expected": "4",
        "description": "decimal numbers",
    },
]
