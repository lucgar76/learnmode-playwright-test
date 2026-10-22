import pytest
from playwright.sync_api import Page
from pages.update_profile_page import UpdateProfilePage
from data.profile_data import PROFILE_STEPS


@pytest.mark.learn_mode
class TestUpdateProfile:

    def test_page_loads_and_shows_form(self, page: Page):
        """Challenge page loads, tutorial is dismissed, and all form fields are visible."""
        profile = UpdateProfilePage(page)
        profile.open()
        assert profile.nickname.is_visible()
        assert profile.first_name.is_visible()
        assert profile.last_name.is_visible()
        assert profile.submit_btn.is_visible()
        assert profile.clear_btn.is_visible()

    def test_all_six_steps_in_sequence(self, page: Page):
        """
        Walk through all 6 step-by-step instructions in order on a single page.
        Each step fills all three fields, clicks Submit, asserts the result,
        then clears the form before the next instruction appears.
        """
        profile = UpdateProfilePage(page)
        profile.open()

        for step_data in PROFILE_STEPS:
            step_num = step_data["step"]
            nickname = step_data["nickname"]
            first_name = step_data["first_name"]
            last_name = step_data["last_name"]
            expected = step_data["expected"]
            description = step_data["description"]

            profile.submit_step(nickname, first_name, last_name)

            result = profile.get_result()
            assert result == expected, (
                f"Step {step_num} ({description}): "
                f"expected '{expected}' but got '{result}' "
                f"for nickname='{nickname}', "
                f"first_name='{first_name}', last_name='{last_name}'"
            )

            if step_num < len(PROFILE_STEPS):
                profile.click_clear()

    @pytest.mark.parametrize("step_data", PROFILE_STEPS, ids=[
        f"step_{s['step']}_{s['description'].replace(' ', '_')}"
        for s in PROFILE_STEPS
    ])
    def test_individual_step(self, page: Page, step_data: dict):
        """
        Run each step independently — page restarts from step 1 each time.
        Useful for isolating and debugging a single step failure.
        """
        profile = UpdateProfilePage(page)
        profile.open()

        for prior_step in PROFILE_STEPS:
            profile.submit_step(
                prior_step["nickname"],
                prior_step["first_name"],
                prior_step["last_name"],
            )

            if prior_step["step"] == step_data["step"]:
                result = profile.get_result()
                assert result == step_data["expected"], (
                    f"Step {step_data['step']} ({step_data['description']}): "
                    f"expected '{step_data['expected']}' but got '{result}'"
                )
                break

            profile.click_clear()

    def test_clear_form_resets_all_fields(self, page: Page):
        """Clear Form button empties all three input fields."""
        profile = UpdateProfilePage(page)
        profile.open()

        profile.enter_profile("skyline7", "Michael", "Henderson")
        profile.click_clear()

        assert profile.nickname.input_value() == ""
        assert profile.first_name.input_value() == ""
        assert profile.last_name.input_value() == ""

    def test_start_over_resets_progress(self, page: Page):
        """Start Over resets the instruction counter back to the beginning."""
        profile = UpdateProfilePage(page)
        profile.open()

        profile.submit_step(
            PROFILE_STEPS[0]["nickname"],
            PROFILE_STEPS[0]["first_name"],
            PROFILE_STEPS[0]["last_name"],
        )
        profile.click_start_over()

        progress = profile.get_progress()
        assert "0" in progress

    # ── Targeted boundary tests ──────────────────────────────────────────────

    def _result_for(self, page: Page, description: str) -> str:
        """Replay the scripted steps up to the named instruction."""
        profile = UpdateProfilePage(page)
        profile.open()
        for step_data in PROFILE_STEPS:
            profile.submit_step(
                step_data["nickname"],
                step_data["first_name"],
                step_data["last_name"],
            )
            if step_data["description"] == description:
                return profile.get_result()
            profile.click_clear()
        raise AssertionError(f"profile step not found: {description}")

    def test_valid_profile_accepted(self, page: Page):
        """A complete valid profile returns 'Your profile updated'."""
        assert self._result_for(page, "valid profile") == "Your profile updated"

    def test_values_shorter_than_minimum_rejected(self, page: Page):
        """Values shorter than the minimum length are rejected."""
        assert self._result_for(page, "shorter than the minimum length") == "User input error"

    def test_values_longer_than_maximum_rejected(self, page: Page):
        """Values longer than the maximum length are rejected."""
        assert self._result_for(page, "longer than the maximum length") == "User input error"

    def test_disallowed_characters_rejected(self, page: Page):
        """Disallowed characters in the profile fields are rejected."""
        assert self._result_for(page, "disallowed characters in every field") == "User input error"

    def test_nickname_with_disallowed_characters_rejected(self, page: Page):
        """A nickname made only of disallowed characters is rejected."""
        assert self._result_for(page, "disallowed characters in the nickname") == "User input error"

    def test_all_fields_empty_rejected(self, page: Page):
        """Submitting every field empty is rejected."""
        assert self._result_for(page, "all fields empty") == "User input error"
