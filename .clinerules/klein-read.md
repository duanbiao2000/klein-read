# Klein Read — Cline / Roo Rules

Klein Read turns pasted weekly articles (English or Japanese) into intensive-reading pages for Chinese college students. Theme words use Klein blue.

- Read `skills/klein-read/SKILL.md` (single source of truth) and `skills/klein-read/references/schema.md` (data fields) before you write data.
- One article = one `data/NNN-english-slug.json` (next number in `data/`). Mark theme words with `[[word|display]]`.
- Run `python3 build.py` in the project folder after every data change. Do not edit `articles/` or `index.html`.
- Language policy: documentation and page UI in English (ASD-STE100 style). Study notes in Chinese. `source_lang`: `en` or `ja`.
- Do not change style files unless the user asks. After style or build changes, run `python3 sync_skill.py`.
