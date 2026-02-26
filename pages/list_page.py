from playwright.sync_api import Page
from pages.base_page import BasePage


class ListPage(BasePage):
    URL = "/app/list"

    def __init__(self, page: Page):
        super().__init__(page)
        # ── Page heading ────────────────────────────────────────────────────
        self.heading = page.get_by_role("heading", name="List of Challenges")

        # ── Learn Mode challenge links ───────────────────────────────────────
        self.link_adder = page.get_by_role("link", name="Challenge #1.1: Number Addition")
        self.link_divider = page.get_by_role("link", name="Challenge #1.2: Number Division")
        self.link_password = page.get_by_role("link", name="Challenge #1.3: Password Restore")
        self.link_profile = page.get_by_role("link", name="Challenge #1.4: Update Profile")

    def open(self):
        self.navigate(self.URL)
        self.dismiss_cookie_popup()
        self.wait_for_element(self.heading)

    def go_to_adder(self):
        self.click(self.link_adder)

    def go_to_divider(self):
        self.click(self.link_divider)

    def go_to_password_restore(self):
        self.click(self.link_password)

    def go_to_update_profile(self):
        self.click(self.link_profile)
