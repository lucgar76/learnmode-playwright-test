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

    def test_valid_profile_accepted(self, page: Page):
        """All three fields correctly filled returns 'Your profile updated'."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("skyline7", "Michael", "Henderson")
        assert profile.get_result() == "Your profile updated"

    def test_missing_nickname_rejected(self, page: Page):
        """Submission without a nickname is rejected."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("", "Michael", "Henderson")
        assert profile.get_result() == "Invalid Profile"

    def test_missing_first_name_rejected(self, page: Page):
        """Submission without a first name is rejected."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("skyline7", "", "Henderson")
        assert profile.get_result() == "Invalid Profile"

    def test_missing_last_name_rejected(self, page: Page):
        """Submission without a last name is rejected."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("skyline7", "Michael", "")
        assert profile.get_result() == "Invalid Profile"

    def test_nickname_with_spaces_rejected(self, page: Page):
        """Nickname containing spaces is rejected."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("sky line 7", "Michael", "Henderson")
        assert profile.get_result() == "Invalid Profile"

    def test_all_fields_empty_rejected(self, page: Page):
        """Submitting all empty fields is rejected."""
        profile = UpdateProfilePage(page)
        profile.open()
        profile.submit_step("", "", "")
        assert profile.get_result() == "Invalid Profile"
