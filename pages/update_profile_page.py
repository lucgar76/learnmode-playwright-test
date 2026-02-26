from playwright.sync_api import Page
from pages.base_page import BasePage


class UpdateProfilePage(BasePage):
    URL = "/app/challenge/learn/updateNickname"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Form inputs ──────────────────────────────────────────────────────
        self.nickname = page.get_by_label("Nickname")
        self.first_name = page.get_by_label("First Name")
        self.last_name = page.get_by_label("Last Name")

        # ── Buttons ──────────────────────────────────────────────────────────
        self.submit_btn = page.get_by_role("button", name="Submit!")
        self.clear_btn = page.get_by_role("button", name="Clear Form")
        self.start_over_btn = page.get_by_role("button", name="Start Over")

        # ── Output & instruction ─────────────────────────────────────────────
        self.result = page.locator("p", has_text="Result:")
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
        self.click(self.submit_btn)

    def click_clear(self):
        self.click(self.clear_btn)

    def click_start_over(self):
        self.click(self.start_over_btn)

    def get_result(self) -> str:
        """Return the validation result text shown after submission."""
        self.wait_for_element(self.result)
        raw = self.result.inner_text().strip()
        return raw.replace("Result:", "").strip()

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
