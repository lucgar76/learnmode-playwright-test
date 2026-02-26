from playwright.sync_api import Page
from pages.base_page import BasePage


class PasswordRestorePage(BasePage):
    URL = "/app/challenge/learn/passwordRestore"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Form inputs ──────────────────────────────────────────────────────
        self.password_input = page.get_by_label("New Password")

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
        self.wait_for_element(self.password_input)
        self.dismiss_tutorial()

    def enter_password(self, password: str):
        self.fill(self.password_input, password)

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
        """Return the progress counter text e.g. '3 out of 11'."""
        return self.get_text(self.progress)

    def get_instruction(self) -> str:
        """Return the current visible instruction text."""
        return self.get_text(self.instruction_text)

    def submit_step(self, password: str):
        """Enter password and click Submit in one call."""
        self.enter_password(password)
        self.click_submit()
