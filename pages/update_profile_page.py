from playwright.sync_api import Page
from pages.base_page import BasePage


class UpdateProfilePage(BasePage):
    URL = "/app/challenge/learn/updateNickname"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Form inputs ──────────────────────────────────────────────────────
        self.nickname = page.get_by_placeholder("Nickname")
        self.first_name = page.get_by_placeholder("First name")
        self.last_name = page.get_by_placeholder("Last name")

        # ── Buttons ──────────────────────────────────────────────────────────
        self.submit_btn = page.get_by_role("button", name="Submit!")
        self.clear_btn = page.get_by_role("button", name="Clear form")
        self.start_over_btn = page.get_by_role("button", name="Start over")

        # ── Output & instruction ─────────────────────────────────────────────
        self.result = page.get_by_test_id("result")
        self.instruction_text = page.locator("ol li").first
        self.progress = page.locator("text=out of")

    def open(self):
        self.navigate(self.URL)
        self.dismiss_cookie_popup()
        self.wait_for_element(self.nickname)
        self.dismiss_tutorial()

    def enter_profile(self, nickname: str, first_name: str, last_name: str):
        self.fill(self.nickname, nickname)
        self.fill(self.first_name, first_name)
        self.fill(self.last_name, last_name)

    def click_submit(self):
        self.prepare_result_wait()
        self.click(self.submit_btn)

    def click_clear(self):
        self.click_if_enabled(self.clear_btn)

    def click_start_over(self):
        self.confirm_start_over(self.start_over_btn)

    def get_result(self) -> str:
        """Return the validation result text shown after submission."""
        return self.read_result_value()

    def get_progress(self) -> str:
        """Return the progress counter text e.g. '2 out of 6'."""
        return self.get_text(self.progress)

    def get_instruction(self) -> str:
        """Return the current visible instruction text."""
        return self.get_text(self.instruction_text)

    def submit_step(self, nickname: str, first_name: str, last_name: str):
        """Fill all three fields and click Submit in one call."""
        self.enter_profile(nickname, first_name, last_name)
        self.click_submit()
