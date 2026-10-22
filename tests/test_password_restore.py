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

    def _result_for(self, page: Page, description: str) -> str:
        """Replay the scripted steps up to the named instruction."""
        pw = PasswordRestorePage(page)
        pw.open()
        for step_data in PASSWORD_STEPS:
            pw.submit_step(step_data["password"])
            if step_data["description"] == description:
                return pw.get_result()
            pw.click_clear()
        raise AssertionError(f"password step not found: {description}")

    def test_valid_password_accepted(self, page: Page):
        """A password meeting every requirement returns 'Valid password'."""
        assert self._result_for(page, "meets all requirements") == "Valid password"

    def test_requirements_not_met_rejected(self, page: Page):
        """A password that misses a requirement is rejected."""
        assert self._result_for(page, "does not meet all requirements") == "Invalid password"

    def test_same_as_saved_password_rejected(self, page: Page):
        """Reusing the saved password is rejected."""
        assert self._result_for(page, "same as the saved password") == "Invalid password"

    def test_too_short_rejected(self, page: Page):
        """A password shorter than 5 characters is rejected."""
        assert self._result_for(page, "shorter than 5 characters") == "Invalid password"

    def test_too_long_rejected(self, page: Page):
        """A password longer than 15 characters is rejected."""
        assert self._result_for(page, "longer than 15 characters") == "Invalid password"

    def test_empty_password_rejected(self, page: Page):
        """An empty password is rejected."""
        assert self._result_for(page, "empty password") == "Invalid password"
