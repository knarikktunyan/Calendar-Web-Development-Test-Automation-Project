import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=True)
def login_user(page: Page):
    page.goto(BASE_URL)

    page.evaluate("localStorage.clear()")

    page.get_by_test_id("username-input").fill("admin")
    page.get_by_test_id("password-input").fill("admin123")
    page.get_by_test_id("login-button").click()


def test_calendar_page_loads(page: Page):

    expect(
        page.get_by_test_id("calendar-page")
    ).to_be_visible()

    expect(
        page.get_by_test_id("current-month")
    ).to_be_visible()

    expect(
        page.get_by_test_id("calendar-days")
    ).to_be_visible()


def test_calendar_has_42_day_cells(page: Page):

    days = page.locator(".calendar-day")

    expect(days).to_have_count(42)


def test_current_month_is_displayed(page: Page):

    month = page.get_by_test_id(
        "current-month"
    )

    expect(month).to_be_visible()

    text = month.text_content()

    assert text is not None
    assert len(text) > 4


def test_previous_month(page: Page):

    month_element = page.get_by_test_id(
        "current-month"
    )

    original_month = month_element.text_content()

    page.get_by_test_id(
        "previous-month"
    ).click()

    new_month = month_element.text_content()

    assert new_month != original_month


def test_next_month(page: Page):

    month_element = page.get_by_test_id(
        "current-month"
    )

    original_month = month_element.text_content()

    page.get_by_test_id(
        "next-month"
    ).click()

    new_month = month_element.text_content()

    assert new_month != original_month


def test_previous_then_next_returns_to_original_month(
    page: Page
):

    month_element = page.get_by_test_id(
        "current-month"
    )

    original_month = month_element.text_content()

    page.get_by_test_id(
        "previous-month"
    ).click()

    page.get_by_test_id(
        "next-month"
    ).click()

    final_month = month_element.text_content()

    assert final_month == original_month


def test_logout_returns_to_login(page: Page):

    page.get_by_test_id(
        "logout-button"
    ).click()

    expect(
        page.get_by_test_id("login-page")
    ).to_be_visible()

    expect(
        page.get_by_test_id("calendar-page")
    ).to_be_hidden()
