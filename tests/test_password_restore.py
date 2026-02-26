import pytest
from playwright.sync_api import Page
from pages.password_restore_page import PasswordRestorePage
from data.password_data import PASSWORD_STEPS


@pytest.mark.learn_mode
class TestPasswordRestore:

    def test_page_loads_and_shows_first_instruction(self, page: Page):
        """Challenge page loads, tutorial is dismissed, and form elements are visible."""
        pw = PasswordRestorePage(page)
        pw.open()
        assert pw.password_input.is_visible()
        assert pw.submit_btn.is_visible()
        assert pw.clear_btn.is_visible()

    def test_all_eleven_steps_in_sequence(self, page: Page):
        """
        Walk through all 11 step-by-step instructions in order on a single page.
        Each step enters a password, clicks Submit, asserts the validation result,
        then clears the form before the next instruction appears.
        """
        pw = PasswordRestorePage(page)
        pw.open()

        for step_data in PASSWORD_STEPS:
            step_num = step_data["step"]
            password = step_data["password"]
            expected = step_data["expected"]
            description = step_data["description"]

            pw.submit_step(password)

            result = pw.get_result()
            assert result == expected, (
                f"Step {step_num} ({description}): "
                f"expected '{expected}' but got '{result}' "
                f"for password '{password}'"
            )

            if step_num < len(PASSWORD_STEPS):
                pw.click_clear()

    @pytest.mark.parametrize("step_data", PASSWORD_STEPS, ids=[
        f"step_{s['step']}_{s['description'].replace(' ', '_')}"
        for s in PASSWORD_STEPS
    ])
    def test_individual_step(self, page: Page, step_data: dict):
        """
        Run each step independently — page restarts from step 1 each time.
        Useful for isolating and debugging a single step failure.
        """
        pw = PasswordRestorePage(page)
        pw.open()

        for prior_step in PASSWORD_STEPS:
            pw.submit_step(prior_step["password"])

            if prior_step["step"] == step_data["step"]:
                result = pw.get_result()
                assert result == step_data["expected"], (
                    f"Step {step_data['step']} ({step_data['description']}): "
                    f"expected '{step_data['expected']}' but got '{result}'"
                )
                break

            pw.click_clear()

    def test_clear_form_resets_password_input(self, page: Page):
        """Clear Form button empties the password field."""
        pw = PasswordRestorePage(page)
        pw.open()

        pw.enter_password("P@ssw0rD")
        pw.click_clear()

        assert pw.password_input.input_value() == ""

    def test_start_over_resets_progress(self, page: Page):
        """Start Over resets the instruction counter back to the beginning."""
        pw = PasswordRestorePage(page)
        pw.open()

        pw.submit_step(PASSWORD_STEPS[0]["password"])
        pw.click_start_over()

        progress = pw.get_progress()
        assert "0" in progress

    # ── Targeted boundary tests ──────────────────────────────────────────────

    def test_valid_password_accepted(self, page: Page):
        """A password meeting all criteria returns 'Valid Password'."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("P@ssw0rD")
        assert pw.get_result() == "Valid Password"

    def test_missing_uppercase_rejected(self, page: Page):
        """Password without an uppercase letter is rejected."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("p@ssw0rd")
        assert pw.get_result() == "Invalid Password"

    def test_missing_digit_rejected(self, page: Page):
        """Password without a digit is rejected."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("P@ssword")
        assert pw.get_result() == "Invalid Password"

    def test_missing_special_char_rejected(self, page: Page):
        """Password without a special character is rejected."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("Passw0rd")
        assert pw.get_result() == "Invalid Password"

    def test_too_short_rejected(self, page: Page):
        """Password shorter than 8 characters is rejected."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("P@s1")
        assert pw.get_result() == "Invalid Password"

    def test_empty_password_rejected(self, page: Page):
        """Empty password submission is rejected."""
        pw = PasswordRestorePage(page)
        pw.open()
        pw.submit_step("")
        assert pw.get_result() == "Invalid Password"
