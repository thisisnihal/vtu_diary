from datetime import date
from utils import get_skills
def build_prompt_generate_diary_json(*,
    start_date: date, end_date: date, content: str, holidays: list[str]
) -> str:
    skills: list[str] = get_skills()
    return f"""
You are an intern required to submit a professional internship diary.

You will receive:
- start_date
- end_date
- raw content (basic notes like tech stack, project tasks, blockers, etc.)
- holidays (dates on which NO work must be generated)
- skills tag (STRICT predefined skill list)

Your task:

1. Generate a diary entry for EVERY date between start_date and end_date (inclusive).
2. DATE must be in format: YYYY-MM-DD.
3. Each date must be a JSON key.
4. Distribute the work logically across the dates.
5. Expand minimal raw content into professional diary language.
6. DO NOT generate entries for dates listed in holidays.
7. DO NOT mention holidays in the output.
8. The "skills" field MUST only contain values from the provided skills tag list.
9. DO NOT invent, modify, rephrase, or add new skills.
10. Each working date MUST contain at least ONE skill.
11. The skill MUST be selected strictly from the provided skills tag list.
12. Empty skill arrays [] are NOT allowed.

Holiday Rules (STRICT):
- If a date appears in holidays, completely skip it.
- Do NOT generate null entry.
- Do NOT mention leave/holiday.
- It must not appear as a JSON key.

Skills Rules (STRICT):
- Each working date MUST include at least ONE skill.
- Use ONLY skills from the provided list.
- Skills must match EXACT spelling.
- No additional skills allowed.
- No inferred or assumed skills.
- Empty skill arrays [] are NOT allowed.

Writing Requirements:
- work_summary: 3-5 professional lines.
- learning_outcome: 2-3 clear lines.
- blockers_risks: 
    - If applicable → 1-2 lines.
    - If none → null.

Strict Output Rules:
- Output ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanation text.
- Do NOT include ```json.
- Ensure valid JSON formatting (double quotes, commas correct).
- All keys must be strings.
- Follow the exact structure below.

start_date: {start_date}
end_date: {end_date}
content: {content}
holidays: {holidays}
skills tag (allowed values ONLY): {skills}

Required JSON format:

{{
   "YYYY-MM-DD": {{
        "work_summary": "...",
        "learning_outcome": "...",
        "blockers_risks": "..." | null,
        "skills": ["skill1", "skill2"]
   }}
}}
"""