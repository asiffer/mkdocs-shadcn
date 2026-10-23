from playwright.sync_api import Page, expect


def test_layout_toggle_visibility_and_saved_preferences(
    page: Page, local_deployment: str
):
    page.set_viewport_size({"width": 1599, "height": 900})
    page.goto(local_deployment + "/", wait_until="domcontentloaded")

    layout_toggle = page.locator('button[onclick="toggleLayout(event)"]')
    expect(layout_toggle).to_be_hidden()
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-fixed')"
    )

    page.set_viewport_size({"width": 1600, "height": 900})
    expect(layout_toggle).to_be_visible()

    page.set_viewport_size({"width": 1599, "height": 900})
    expect(layout_toggle).to_be_hidden()
    page.set_viewport_size({"width": 1600, "height": 900})
    expect(layout_toggle).to_be_visible()

    fixed_width = page.locator("header .container-wrapper").evaluate(
        "(element) => element.getBoundingClientRect().width"
    )
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-fixed')"
    )

    layout_toggle.click()
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-full')"
    )
    assert page.evaluate("localStorage.getItem('html-layout')") == "layout-full"
    full_width = page.locator("header .container-wrapper").evaluate(
        "(element) => element.getBoundingClientRect().width"
    )
    assert full_width > fixed_width

    page.reload(wait_until="domcontentloaded")
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-full')"
    )
    expect(layout_toggle).to_be_visible()

    layout_toggle.click()
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-fixed')"
    )
    assert page.evaluate("localStorage.getItem('html-layout')") == "layout-fixed"
    page.reload(wait_until="domcontentloaded")
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('layout-fixed')"
    )
    expect(layout_toggle).to_be_visible()

    page.evaluate(
        "localStorage.setItem('theme', 'light'); "
        "document.documentElement.classList.remove('dark')"
    )
    page.get_by_title("Toggle theme").click()
    assert page.locator("html").evaluate(
        "(element) => element.classList.contains('dark')"
    )
    assert page.evaluate("localStorage.getItem('theme')") == "dark"
