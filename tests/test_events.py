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


def open_add_event(page: Page):

    page.get_by_test_id(
        "add-event-button"
    ).click()

    expect(
        page.get_by_test_id("event-modal")
    ).to_be_visible()


def test_add_valid_event(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Team Meeting")

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "save-event"
    ).click()

    expect(
        page.locator(".event-title")
    ).to_contain_text("Team Meeting")


def test_empty_event_title(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "save-event"
    ).click()

    expect(
        page.get_by_test_id("title-error")
    ).to_be_visible()

    expect(
        page.get_by_test_id("event-modal")
    ).to_be_visible()


def test_missing_event_date(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Meeting")

    page.get_by_test_id(
        "save-event"
    ).click()

    expect(
        page.get_by_test_id("date-error")
    ).to_be_visible()

    expect(
        page.get_by_test_id("event-modal")
    ).to_be_visible()


def test_empty_title_and_date(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "save-event"
    ).click()

    expect(
        page.get_by_test_id("title-error")
    ).to_be_visible()

    expect(
        page.get_by_test_id("date-error")
    ).to_be_visible()


def test_cancel_event(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Cancelled Event")

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "cancel-event"
    ).click()

    expect(
        page.get_by_test_id("event-modal")
    ).to_be_hidden()

    assert page.locator(
        ".event-title"
    ).count() == 0


def test_close_event_modal(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "close-modal"
    ).click()

    expect(
        page.get_by_test_id("event-modal")
    ).to_be_hidden()


def test_edit_event(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Original Event")

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "save-event"
    ).click()

    expect(
        page.locator(".event-title")
    ).to_contain_text("Original Event")


    edit_button = page.locator(
        '[data-testid^="edit-event-"]'
    ).first

    edit_button.click()


    expect(
        page.get_by_test_id("event-modal")
    ).to_be_visible()


    page.get_by_test_id(
        "event-title"
    ).fill("Updated Event")

    page.get_by_test_id(
        "save-event"
    ).click()


    expect(
        page.locator(".event-title")
    ).to_contain_text("Updated Event")

    assert page.locator(
        ".event-title"
    ).filter(
        has_text="Original Event"
    ).count() == 0


def test_delete_event(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Delete Me")

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "save-event"
    ).click()


    expect(
        page.locator(".event-title")
    ).to_contain_text("Delete Me")


    delete_button = page.locator(
        '[data-testid^="delete-event-"]'
    ).first

    delete_button.click()


    assert page.locator(
        ".event-title"
    ).filter(
        has_text="Delete Me"
    ).count() == 0


def test_multiple_events(page: Page):

    events = [
        ("Meeting", "2026-09-15"),
        ("Doctor Appointment", "2026-09-16"),
        ("Project Deadline", "2026-09-17")
    ]

    for title, date in events:

        open_add_event(page)

        page.get_by_test_id(
            "event-title"
        ).fill(title)

        page.get_by_test_id(
            "event-date"
        ).fill(date)

        page.get_by_test_id(
            "save-event"
        ).click()


    for title, date in events:

        expect(
            page.locator(".event-title").filter(
	    	has_text=title
		)
        ).to_be_visible()


def test_event_remains_after_refresh(page: Page):

    open_add_event(page)

    page.get_by_test_id(
        "event-title"
    ).fill("Persistent Event")

    page.get_by_test_id(
        "event-date"
    ).fill("2026-09-15")

    page.get_by_test_id(
        "save-event"
    ).click()


    expect(
        page.locator(".event-title")
    ).to_contain_text("Persistent Event")


    page.reload()


    expect(
        page.get_by_test_id("calendar-page")
    ).to_be_visible()


    expect(
        page.locator(".event-title")
    ).to_contain_text("Persistent Event")
