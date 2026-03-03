from datetime import date
from ai import GeminiService
from prompts import build_prompt_generate_diary_json
import json
from pathlib import Path


def main(*, start_date: date, end_date: date, holidays: list[str], content: str):

    save_holidays(holidays, start_date, end_date)
    ai_internship_details: str = generate_ai_response(
        start_date=start_date, end_date=end_date, content=content, holidays=holidays
    )
    save_internship_details(start_date, end_date, ai_internship_details)


def generate_ai_response(
    start_date: date,
    end_date: date,
    content: str,
    holidays: list[str],
):
    prompt = build_prompt_generate_diary_json(
        start_date=start_date, end_date=end_date, content=content, holidays=holidays
    )
    gemini_service = GeminiService()
    response = gemini_service.get_response(prompt)
    return response


def save_holidays(holidays: list[str], start_date: date, end_date: date):
    holidays_json = f"{str(start_date)}_{str(end_date)}_holidays.json"
    # delete existing holiday file
    if Path(holidays_json).is_file():
        Path(holidays_json).unlink()
    with open(holidays_json, "w", encoding="utf-8") as file:
        json_data = {"holidays": holidays}
        json.dump(json_data, file, indent=4)
        print("Holiday json saved into file:", holidays_json)


def save_internship_details(
    start_date: date, end_date: date, ai_internship_details: str
):
    internship_details_json = (
        f"{str(start_date)}_{str(end_date)}_internship_details.json"
    )
    # delete existing internship details file
    if Path(internship_details_json).is_file():
        Path(internship_details_json).unlink()
    with open(internship_details_json, "w", encoding="utf-8") as file:
        json_data = json.loads(ai_internship_details)
        json.dump(json_data, file, indent=4)
        print("Internship json saved into file:", internship_details_json)


