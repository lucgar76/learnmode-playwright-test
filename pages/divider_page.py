from playwright.sync_api import Page
from pages.base_page import BasePage


class DividerPage(BasePage):
    URL = "/app/challenge/learn/divider"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Form inputs ──────────────────────────────────────────────────────
        self.first_number = page.get_by_placeholder("First number")
        self.second_number = page.get_by_placeholder("Second number")

        # ── Buttons ──────────────────────────────────────────────────────────
        self.calculate_btn = page.get_by_role("button", name="Calculate!")
        self.clear_btn = page.get_by_role("button", name="Clear form")
        self.start_over_btn = page.get_by_role("button", name="Start over")

        # ── Output & instruction ─────────────────────────────────────────────
        self.result = page.get_by_test_id("result")
        self.instruction_text = page.locator("ol li").first
        self.progress = page.locator("text=out of")

    def open(self):
        self.navigate(self.URL)
        self.dismiss_cookie_popup()
        self.wait_for_element(self.first_number)
        self.dismiss_tutorial()

    def enter_numbers(self, first: str, second: str):
        self.fill(self.first_number, first)
        self.fill(self.second_number, second)

    def click_calculate(self):
        self.prepare_result_wait()
        self.click(self.calculate_btn)

    def click_clear(self):
        self.click_if_enabled(self.clear_btn)

    def click_start_over(self):
        self.confirm_start_over(self.start_over_btn)

    def get_result(self) -> str:
        """Return the value shown after calculation."""
        return self.read_result_value()

    def get_progress(self) -> str:
        """Return the progress counter text e.g. '1 out of 6'."""
        return self.get_text(self.progress)

    def get_instruction(self) -> str:
        """Return the current visible instruction text."""
        return self.get_text(self.instruction_text)

    def submit_step(self, first: str, second: str):
        """Fill both fields and click Calculate in one call."""
        self.enter_numbers(first, second)
        self.click_calculate()
