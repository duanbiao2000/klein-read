# Klein Read — Copilot Instructions

This project turns pasted weekly articles (English or Japanese) into intensive-reading web pages for Chinese college students. Theme words use Klein blue (#002FA7).

Rules:
1. Read `skills/klein-read/SKILL.md` (workflow and quality rules) and `skills/klein-read/references/schema.md` (data fields) before you write data.
2. One article = one `data/NNN-english-slug.json` (next number in `data/`). Mark theme words with `[[word]]` or `[[word|display]]`.
3. Run `python3 build.py` after every data change. Python standard library only.
4. Do not edit generated files: `articles/*.html`, `index.html`. Do not change `css/`, `js/`, `templates/` unless the user asks.
5. Language policy: documentation and page UI in English (ASD-STE100 style). Study notes in Chinese.
6. New users: see `QUICKSTART.md`.
