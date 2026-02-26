# learnmode-playwright-test

Python + Playwright test automation for the [BugEater](https://bugeater.web.app/app/list) Learn Mode challenges.

## Challenges Covered

| # | Challenge | URL | Steps |
|---|-----------|-----|-------|
| 1.1 | Number Addition | `/app/challenge/learn/adder` | 6 |
| 1.2 | Number Division | `/app/challenge/learn/divider` | 6 |
| 1.3 | Password Restore | `/app/challenge/learn/passwordRestore` | 11 |
| 1.4 | Update Profile | `/app/challenge/learn/updateNickname` | 6 |

---

## Project Structure

```
learnmode-playwright-test/
├── conftest.py                   # Browser & page fixtures
├── pytest.ini                    # Base URL, markers, headed mode
├── requirements.txt              # Dependencies
├── pages/
│   ├── base_page.py              # Shared helpers: navigate, wait, fill, click
│   ├── list_page.py              # Challenge list landing page
│   ├── adder_page.py             # Number Addition page
│   ├── divider_page.py           # Number Division page
│   ├── password_restore_page.py  # Password Restore page
│   └── update_profile_page.py    # Update Profile page
├── tests/
│   ├── test_list_page.py         # Verify all challenge links
│   ├── test_adder.py             # Number Addition tests
│   ├── test_divider.py           # Number Division tests
│   ├── test_password_restore.py  # Password Restore tests
│   └── test_update_profile.py    # Update Profile tests
└── data/
    ├── adder_data.py             # 6-step input/expected data
    ├── divider_data.py           # 6-step input/expected data
    ├── password_data.py          # 11-step input/expected data
    └── profile_data.py           # 6-step input/expected data
```

---

## Setup

### 1. Clone and enter the project

```bash
cd /path/to/learnmode-playwright-test
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Chromium browser

```bash
playwright install chromium
```

---

## Running Tests

> Make sure your virtual environment is active: `source .venv/bin/activate`

### Run all tests

```bash
pytest
```

### Run a specific challenge

```bash
pytest tests/test_adder.py -v
pytest tests/test_divider.py -v
pytest tests/test_password_restore.py -v
pytest tests/test_update_profile.py -v
```

### Run only smoke tests (landing page link checks)

```bash
pytest -m smoke -v
```

### Run only Learn Mode tests

```bash
pytest -m learn_mode -v
```

### Run in headless mode (no browser window)

```bash
pytest --headless
```

### Run with a specific browser

```bash
pytest --browser firefox
pytest --browser webkit
```

### Run a single test by name

```bash
pytest tests/test_adder.py::TestAdder::test_all_six_steps_in_sequence -v
```

### Run parametrized tests for one step only

```bash
pytest tests/test_adder.py -k "step_1" -v
```

---

## Test Data

Step-by-step input/expected data lives in the `data/` folder. Step 1 of each challenge is confirmed from the live application. Steps 2 onwards follow standard scripted-testing patterns — run each challenge manually in the browser to verify and adjust expected values if needed.

### Updating a step

Open the relevant data file and edit the `expected` value:

```python
# data/adder_data.py
{
    "step": 2,
    "first": "0",
    "second": "0",
    "expected": "0",   # <-- update this if the app shows a different value
    "description": "both inputs are zero",
},
```

---

## Architecture

### Page Object Model

Every challenge page inherits from `BasePage`, which provides:

| Method | Description |
|--------|-------------|
| `navigate(path)` | Go to a relative URL |
| `wait_for_element(locator)` | Explicit 10s visibility wait |
| `fill(locator, value)` | Clear + type into an input |
| `click(locator)` | Wait then click |
| `get_text(locator)` | Return trimmed inner text |
| `dismiss_tutorial()` | Skip the intro overlay if present |

### Locator Strategy (priority order)

1. `get_by_label()` — form inputs
2. `get_by_role()` — buttons and headings
3. `get_by_text()` — result / instruction text
4. `locator("css")` — structural fallback

### Explicit Waits

All interactions use `locator.wait_for(state="visible", timeout=10_000)` before acting — no `time.sleep()` anywhere in the codebase.

---

## Markers

| Marker | Usage |
|--------|-------|
| `learn_mode` | All Learn Mode challenge tests |
| `smoke` | Fast link-visibility checks on the list page |
