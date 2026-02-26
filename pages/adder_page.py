from playwright.sync_api import Page
from pages.base_page import BasePage


class AdderPage(BasePage):
    URL = "/app/challenge/learn/adder"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Form inputs ──────────────────────────────────────────────────────
        self.first_number = page.get_by_label("First Number")
        self.second_number = page.get_by_label("Second Number")

        # ── Buttons ──────────────────────────────────────────────────────────
        self.calculate_btn = page.get_by_role("button", name="Calculate!")
        self.clear_btn = page.get_by_role("button", name="Clear Form")
        self.start_over_btn = page.get_by_role("button", name="Start Over")

        # ── Output & instruction ─────────────────────────────────────────────
        self.result = page.locator("p", has_text="Result:")
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
        self.click(self.calculate_btn)

    def click_clear(self):
        self.click(self.clear_btn)

    def click_start_over(self):
        self.click(self.start_over_btn)

    def get_result(self) -> str:
        """Return the numeric result text shown after calculation."""
        self.wait_for_element(self.result)
        raw = self.result.inner_text().strip()
        # Strip the "Result:" label — returns the value portion only
        return raw.replace("Result:", "").strip()

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
