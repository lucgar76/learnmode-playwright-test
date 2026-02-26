from playwright.sync_api import Page, Locator


class BasePage:
    TIMEOUT = 10_000  # 10 seconds explicit wait timeout

    def __init__(self, page: Page):
        self.page = page

    # ── Navigation ──────────────────────────────────────────────────────────

    def navigate(self, path: str):
        """Navigate to a relative path. Base URL is set in conftest.py."""
        self.page.goto(path)

    # ── Waits ───────────────────────────────────────────────────────────────

    def wait_for_element(self, locator: Locator) -> Locator:
        """Wait until a locator is visible, then return it."""
        locator.wait_for(state="visible", timeout=self.TIMEOUT)
        return locator

    def wait_for_result(self, locator: Locator, expected: str):
        """Poll until the locator's text contains the expected value."""
        self.page.wait_for_function(
            "(el, val) => el.textContent.includes(val)",
            arg=[locator.element_handle(), expected],
            timeout=self.TIMEOUT,
        )

    # ── Actions ─────────────────────────────────────────────────────────────

    def fill(self, locator: Locator, value: str):
        """Clear then fill an input field."""
        self.wait_for_element(locator)
        locator.clear()
        locator.fill(value)

    def click(self, locator: Locator):
        """Wait for element then click it."""
        self.wait_for_element(locator)
        locator.click()

    # ── Data Retrieval ───────────────────────────────────────────────────────

    def get_text(self, locator: Locator) -> str:
        """Wait for element and return its trimmed text content."""
        self.wait_for_element(locator)
        return locator.inner_text().strip()

    # ── Cookie / Terms Popup ─────────────────────────────────────────────────

    def dismiss_cookie_popup(self):
        """
        Dismiss the cookie/terms modal that blocks interactions on first load.
        Tries common button labels. Waits for the dialog to fully hide before
        returning. Falls through silently if no popup is present.
        """
        dialog = self.page.locator("[role='dialog']")
        try:
            dialog.wait_for(state="visible", timeout=3_000)
        except Exception:
            return  # No dialog present — nothing to dismiss

        for label in ("Accept", "OK", "Got it", "I agree", "Close", "Accept All", "Agree"):
            btn = self.page.get_by_role("button", name=label)
            try:
                btn.wait_for(state="visible", timeout=1_000)
                btn.click()
                dialog.wait_for(state="hidden", timeout=3_000)
                return
            except Exception:
                continue

    # ── Tutorial Overlay ─────────────────────────────────────────────────────

    def dismiss_tutorial(self):
        """
        Dismiss the tutorial overlay present on first page load.
        Uses 'Skip' to bypass the intro without cycling through all steps.
        Falls through silently if no overlay is present.
        """
        skip_btn = self.page.get_by_role("button", name="Skip")
        try:
            skip_btn.wait_for(state="visible", timeout=3_000)
            skip_btn.click()
        except Exception:
            pass
