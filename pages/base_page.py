from playwright.sync_api import Page, Locator


class BasePage:
    TIMEOUT = 10_000  # 10 seconds explicit wait timeout

    def __init__(self, page: Page):
        self.page = page
        self._entered_before = ""

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
        Dismiss the modals that block the form on first load.

        The guide dialog is stacked above the cookie dialog, so it has to go
        first. Otherwise the cookie Accept button is visible but not clickable.
        """
        try:
            self.page.locator("[role='dialog']").first.wait_for(state="visible", timeout=3_000)
        except Exception:
            return

        for _ in range(3):
            if self._click_button_if_visible("No, thanks"):
                continue
            if self._click_button_if_visible("Skip"):
                continue
            if any(
                self._click_button_if_visible(label)
                for label in ("Accept", "OK", "Got it", "I agree", "Close", "Accept All", "Agree")
            ):
                continue
            break

    def dismiss_tutorial(self):
        """Dismiss a leftover guide overlay. The guide is normally closed first."""
        self._click_button_if_visible("No, thanks")
        self._click_button_if_visible("Skip")

    def _click_button_if_visible(self, name: str) -> bool:
        button = self.page.get_by_role("button", name=name)
        try:
            if button.count() == 0 or not button.first.is_visible():
                return False
            button.first.click(timeout=3_000)
            return True
        except Exception:
            return False

    # ── Result text ──────────────────────────────────────────────────────────

    def prepare_result_wait(self):
        """Remember the current submission summary so the next result can be told apart."""
        entered = self.page.locator("p", has_text="Entered value")
        if entered.count() and entered.first.is_visible():
            self._entered_before = entered.first.inner_text().strip()
        else:
            self._entered_before = ""

    def read_result_value(self) -> str:
        """
        Return the value shown after 'Result:'.

        The label is on screen before the value, and a later step can show the
        same message as the previous one, so wait until the entered-values
        summary changes and the result text has settled.
        """
        previous = self._entered_before
        self.page.wait_for_function(
            """(prev) => {
                const enteredEl = [...document.querySelectorAll('p')]
                    .find((node) => node.innerText.includes('Entered value'));
                const resultEl = document.querySelector("[data-testid='result']");
                if (!enteredEl || !resultEl) return false;
                const entered = enteredEl.innerText.trim();
                const value = resultEl.innerText.replace(/Result:\\s*/, '').trim();
                if (!value || (prev && entered === prev)) return false;
                const key = entered + '\\n' + value;
                const now = Date.now();
                if (window.__pwResultKey !== key) {
                    window.__pwResultKey = key;
                    window.__pwResultAt = now;
                    return false;
                }
                return now - window.__pwResultAt >= 400;
            }""",
            arg=previous,
            timeout=self.TIMEOUT,
        )
        raw = self.page.locator("[data-testid='result']").inner_text().strip()
        return raw.replace("Result:", "", 1).strip()

    def confirm_start_over(self, button: Locator):
        """Start over asks for confirmation before it clears the progress."""
        self.click(button)
        confirm = self.page.get_by_role("button", name="Yes")
        try:
            confirm.wait_for(state="visible", timeout=3_000)
            confirm.click()
        except Exception:
            return

    def click_if_enabled(self, locator: Locator):
        """Click a button when it is enabled. A disabled Clear control is already empty."""
        self.wait_for_element(locator)
        if locator.is_enabled():
            locator.click()
