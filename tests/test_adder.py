import pytest
from playwright.sync_api import Page
from pages.adder_page import AdderPage
from data.adder_data import ADDER_STEPS


@pytest.mark.learn_mode
class TestAdder:

    def test_page_loads_and_shows_first_instruction(self, page: Page):
        """Challenge page loads, tutorial is dismissed, and first instruction is visible."""
        adder = AdderPage(page)
        adder.open()
        assert adder.first_number.is_visible()
        assert adder.calculate_btn.is_visible()
        assert adder.clear_btn.is_visible()

    def test_all_six_steps_in_sequence(self, page: Page):
        """
        Walk through all 6 step-by-step instructions in order on a single page.
        Each step fills the inputs, clicks Calculate, asserts the result,
        then clears the form before the next instruction appears.
        """
        adder = AdderPage(page)
        adder.open()

        for step_data in ADDER_STEPS:
            step_num = step_data["step"]
            first = step_data["first"]
            second = step_data["second"]
            expected = step_data["expected"]
            description = step_data["description"]

            adder.submit_step(first, second)

            result = adder.get_result()
            assert result == expected, (
                f"Step {step_num} ({description}): "
                f"expected '{expected}' but got '{result}' "
                f"for inputs '{first}' + '{second}'"
            )

            # Clear form before next step (unless it's the last step)
            if step_num < len(ADDER_STEPS):
                adder.click_clear()

    @pytest.mark.parametrize("step_data", ADDER_STEPS, ids=[
        f"step_{s['step']}_{s['description'].replace(' ', '_')}"
        for s in ADDER_STEPS
    ])
    def test_individual_step(self, page: Page, step_data: dict):
        """
        Run each step independently — page restarts from step 1 each time.
        Useful for isolating and debugging a single step failure.
        """
        adder = AdderPage(page)
        adder.open()

        # Navigate through earlier steps to reach the target step
        for prior_step in ADDER_STEPS:
            adder.submit_step(prior_step["first"], prior_step["second"])

            if prior_step["step"] == step_data["step"]:
                result = adder.get_result()
                assert result == step_data["expected"], (
                    f"Step {step_data['step']} ({step_data['description']}): "
                    f"expected '{step_data['expected']}' but got '{result}'"
                )
                break

            adder.click_clear()

    def test_clear_form_resets_inputs(self, page: Page):
        """Clear Form button empties both input fields."""
        adder = AdderPage(page)
        adder.open()

        adder.enter_numbers("5", "10")
        adder.click_clear()

        assert adder.first_number.input_value() == ""
        assert adder.second_number.input_value() == ""

    def test_start_over_resets_progress(self, page: Page):
        """Start Over button resets the instruction counter back to the beginning."""
        adder = AdderPage(page)
        adder.open()

        # Complete step 1 to advance the counter
        adder.submit_step(
            ADDER_STEPS[0]["first"],
            ADDER_STEPS[0]["second"],
        )
        adder.click_start_over()

        # Progress should be back at 0
        progress = adder.get_progress()
        assert "0" in progress
