from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
from pathlib import Path
from config import settings
from datetime import date, datetime
import json


def main(*, internship_file: str):

    with open(internship_file, "r", encoding="utf-8") as f:
        internship_data = json.load(f)

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)

        if Path("state.json").is_file():
            context: BrowserContext = browser.new_context(storage_state="state.json")
        else:
            context: BrowserContext = browser.new_context()

        page: Page = context.new_page()
        counter: int = 0
        for date_str, data in internship_data.items():
            run_actions(
                page,
                context,
                datetime.strptime(date_str, "%Y-%m-%d").date(),
                data,
            )
            print("filled entry for: ", date_str)
            counter += 1
            if counter == 4:
                page.wait_for_timeout(30_000)
                counter = 0

        page.wait_for_timeout(30000)
        browser.close()


def run_actions(page: Page, context: BrowserContext, current_date: date, data):

    page.goto("https://vtu.internyet.in/dashboard/student", wait_until="networkidle")
    check_login(page, context)

    pop_up = page.get_by_role("button", name="I Understand")
    if pop_up.count() > 0:
        pop_up.first.wait_for(state="visible")
        pop_up.first.click()

    open_diary_page(page, context, current_date)
    create_diary_entry(page,context, data)


def check_login(page: Page, context: BrowserContext):
    try:

        if "sign-in" not in page.url:
            return
        page.get_by_placeholder("Enter your email address").fill(settings.VTU_EMAIL)
        page.get_by_placeholder("Enter your password").fill(settings.VTU_PASSWORD)
        page.get_by_role("button", name="Sign In").click()

        page.wait_for_url("**/dashboard/student", timeout=10000)
        context.storage_state(path="state.json")

    except Exception as e:
        print(f"Login exception: {e}")


def open_diary_page(page: Page, context: BrowserContext, current_date: date):
    try:
        check_login(page, context)

        if current_date.weekday() > 5:
            return

        page.goto(
            "https://vtu.internyet.in/dashboard/student/student-diary",
            wait_until="networkidle",
        )

        page.locator("#internship_id").wait_for(state="visible")
        page.locator("#internship_id").click()
        page.keyboard.press("Enter")

        page.get_by_text("Pick a Date").click()

        page.locator('select[aria-label="Choose the Year"]').select_option(
            str(current_date.year)
        )

        page.locator('select[aria-label="Choose the Month"]').select_option(
            str(current_date.month - 1)
        )

        page.locator(f'td[data-day="{str(current_date)}"]').wait_for(state="visible")
        page.locator(f'td[data-day="{str(current_date)}"]').click()

        page.get_by_role("button", name="Continue").click()

    except Exception as e:
        print(f"Diary page exception: {e}")


def create_diary_entry(page: Page, context: BrowserContext, data):

    check_login(page, context)


    work_summary = data["work_summary"]
    learning_outcome = data["learning_outcome"]
    blockers_risks = data["blockers_risks"] if data["blockers_risks"] else ""
    skills = data["skills"]

    page.get_by_placeholder("Briefly describe the work you did today…").fill(work_summary)
    page.get_by_placeholder("e.g. 6.5").fill(str(settings.DAILY_WORK_HRS))
    page.get_by_placeholder("What did you learn or ship today?").fill(learning_outcome)
    page.get_by_placeholder("Anything that slowed you down?").fill(blockers_risks)

    dropdown = page.locator(".react-select__input-container")

    for skill in skills:

        dropdown.click()

        page.locator(".react-select__menu").wait_for(state="visible")

        option = page.locator(".react-select__option", has_text=skill)

        if option.count() > 0:
            option.first.click()

        page.locator(".react-select__menu").wait_for(state="hidden")

    page.wait_for_timeout(500)
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(1000)
    page.wait_for_load_state("networkidle")