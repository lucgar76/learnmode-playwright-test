import pytest
from playwright.sync_api import Page
from pages.list_page import ListPage


@pytest.mark.learn_mode
@pytest.mark.smoke
class TestListPage:

    def test_page_loads_successfully(self, page: Page):
        """Landing page navigates and shows the main heading."""
        list_page = ListPage(page)
        list_page.open()
        assert list_page.heading.is_visible()

    def test_adder_link_is_visible(self, page: Page):
        """Number Addition challenge link is present on the list page."""
        list_page = ListPage(page)
        list_page.open()
        assert list_page.link_adder.is_visible()

    def test_divider_link_is_visible(self, page: Page):
        """Number Division challenge link is present on the list page."""
        list_page = ListPage(page)
        list_page.open()
        assert list_page.link_divider.is_visible()

    def test_password_restore_link_is_visible(self, page: Page):
        """Password Restore challenge link is present on the list page."""
        list_page = ListPage(page)
        list_page.open()
        assert list_page.link_password.is_visible()

    def test_update_profile_link_is_visible(self, page: Page):
        """Update Profile challenge link is present on the list page."""
        list_page = ListPage(page)
        list_page.open()
        assert list_page.link_profile.is_visible()

    def test_adder_link_navigates_correctly(self, page: Page):
        """Clicking Number Addition link routes to the correct challenge URL."""
        list_page = ListPage(page)
        list_page.open()
        list_page.go_to_adder()
        assert "learn/adder" in page.url

    def test_divider_link_navigates_correctly(self, page: Page):
        """Clicking Number Division link routes to the correct challenge URL."""
        list_page = ListPage(page)
        list_page.open()
        list_page.go_to_divider()
        assert "learn/divider" in page.url

    def test_password_link_navigates_correctly(self, page: Page):
        """Clicking Password Restore link routes to the correct challenge URL."""
        list_page = ListPage(page)
        list_page.open()
        list_page.go_to_password_restore()
        assert "learn/passwordRestore" in page.url

    def test_profile_link_navigates_correctly(self, page: Page):
        """Clicking Update Profile link routes to the correct challenge URL."""
        list_page = ListPage(page)
        list_page.open()
        list_page.go_to_update_profile()
        assert "learn/updateNickname" in page.url
