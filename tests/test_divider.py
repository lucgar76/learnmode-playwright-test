import pytest
from playwright.sync_api import Page
from pages.divider_page import DividerPage
from data.divider_data import DIVIDER_STEPS


@pytest.mark.learn_mode
class TestDivider:

    def test_page_loads_and_shows_first_instruction(self, page: Page):
        """Challenge page loads, tutorial is dismissed, and form elements are visible."""
        divider = DividerPage(page)
        divider.open()
        assert divider.first_number.is_visible()
        assert divider.second_number.is_visible()
        assert divider.calculate_btn.is_visible()
        assert divider.clear_btn.is_visible()

    def test_all_six_steps_in_sequence(self, page: Page):
        """
        Walk through all 6 step-by-step instructions in order on a single page.
        Each step fills the inputs, clicks Calculate, asserts the result,
        then clears the form before the next instruction appears.
        """
        divider = DividerPage(page)
        divider.open()

        for step_data in DIVIDER_STEPS:
            step_num = step_data["step"]
            first = step_data["first"]
            second = step_data["second"]
            expected = step_data["expected"]
            description = step_data["description"]

            divider.submit_step(first, second)

            result = divider.get_result()
            assert result == expected, (
                f"Step {step_num} ({description}): "
                f"expected '{expected}' but got '{result}' "
                f"for inputs '{first}' ÷ '{second}'"
            )

            if step_num < len(DIVIDER_STEPS):
                divider.click_clear()

    @pytest.mark.parametrize("step_data", DIVIDER_STEPS, ids=[
        f"step_{s['step']}_{s['description'].replace(' ', '_')}"
        for s in DIVIDER_STEPS
    ])
    def test_individual_step(self, page: Page, step_data: dict):
        """
        Run each step independently — page restarts from step 1 each time.
        Useful for isolating and debugging a single step failure.
        """
        divider = DividerPage(page)
        divider.open()

        for prior_step in DIVIDER_STEPS:
            divider.submit_step(prior_step["first"], prior_step["second"])

            if prior_step["step"] == step_data["step"]:
                result = divider.get_result()
                assert result == step_data["expected"], (
                    f"Step {step_data['step']} ({step_data['description']}): "
                    f"expected '{step_data['expected']}' but got '{result}'"
                )
                break

            divider.click_clear()

    def test_clear_form_resets_inputs(self, page: Page):
        """Clear Form button empties both input fields."""
        divider = DividerPage(page)
        divider.open()

        divider.enter_numbers("10", "2")
        divider.click_clear()

        assert divider.first_number.input_value() == ""
        assert divider.second_number.input_value() == ""

    def test_start_over_resets_progress(self, page: Page):
        """Start Over button resets the instruction counter back to the beginning."""
        divider = DividerPage(page)
        divider.open()

        divider.submit_step(
            DIVIDER_STEPS[0]["first"],
            DIVIDER_STEPS[0]["second"],
        )
        divider.click_start_over()

        progress = divider.get_progress()
        assert "0" in progress

    def test_divide_by_zero_shows_error(self, page: Page):
        """
        Dividing by zero should display an error message rather than a numeric result.
        This is a key boundary condition for any division form.
        """
        divider = DividerPage(page)
        divider.open()

        divider.submit_step("10", "0")
        result = divider.get_result()

        assert result != "Infinity" and result != "", (
            f"Expected an error indicator for division by zero, got: '{result}'"
        )
