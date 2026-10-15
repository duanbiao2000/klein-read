---
trigger: always_on
---

# Klein Read Project Rules

Klein Read turns pasted weekly articles (English or Japanese) into intensive-reading pages for Chinese college students. Theme words use Klein blue.

- Read `skills/klein-read/SKILL.md` (workflow and quality rules) and `skills/klein-read/references/schema.md` (data fields) before you write data.
- One article = one `data/NNN-english-slug.json` (next number in `data/`). Mark theme words with `[[word|display]]`.
- Run `python3 build.py` after every data change. Do not edit `articles/` or `index.html`.
- Language policy: documentation and page UI in English (ASD-STE100 style). Study notes in Chinese.
- Do not change style files unless the user asks.
