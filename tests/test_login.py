import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=True)
def clear_storage(page: Page):
    page.goto(BASE_URL)
    page.evaluate("localStorage.clear()")
    page.reload()


def login(page: Page, username="admin", password="admin123"):
    page.get_by_test_id("username-input").fill(username)
    page.get_by_test_id("password-input").fill(password)
    page.get_by_test_id("login-button").click()


def test_successful_login(page: Page):
    login(page)

    expect(
        page.get_by_test_id("calendar-page")
    ).to_be_visible()

    expect(
        page.get_by_test_id("current-month")
    ).to_be_visible()


def test_wrong_username(page: Page):
    login(
        page,
        username="wronguser",
        password="admin123"
    )

    expect(
        page.get_by_test_id("login-error")
    ).to_have_text(
        "Incorrect username or password."
    )

    expect(
        page.get_by_test_id("login-page")
    ).to_be_visible()


def test_wrong_password(page: Page):
    login(
        page,
        username="admin",
        password="wrongpassword"
    )

    expect(
        page.get_by_test_id("login-error")
    ).to_have_text(
        "Incorrect username or password."
    )


def test_empty_username(page: Page):
    login(
        page,
        username="",
        password="admin123"
    )

    expect(
        page.get_by_test_id("login-error")
    ).to_have_text(
        "Username and password are required."
    )


def test_empty_password(page: Page):
    login(
        page,
        username="admin",
        password=""
    )

    expect(
        page.get_by_test_id("login-error")
    ).to_have_text(
        "Username and password are required."
    )


def test_empty_login_fields(page: Page):
    login(
        page,
        username="",
        password=""
    )

    expect(
        page.get_by_test_id("login-error")
    ).to_have_text(
        "Username and password are required."
    )
