# Klein Read — AI Agent Rules (AGENTS.md)

Klein Read is a data-driven generator of intensive-reading web pages. Target reader: Chinese college students. Source text: English or Japanese weeklies. Theme words: Klein blue.

Your main task: turn a pasted article into one high-quality reading page.

## Core Rules

1. Read [`skills/klein-read/SKILL.md`](skills/klein-read/SKILL.md) before you write data. It is the single source of truth. Field details: [`skills/klein-read/references/schema.md`](skills/klein-read/references/schema.md).
2. One article = one `data/NNN-english-slug.json` file. `NNN` is the next number in `data/`. The `data/` folder is the only source you edit.
3. Run `python3 build.py` in the project folder after every data change. Python standard library only.
4. Do not edit `articles/*.html` or `index.html` by hand. Do not change style files unless the user asks. Design rules: [`skills/klein-read/references/design.md`](skills/klein-read/references/design.md).
5. Language policy: documentation in English (ASD-STE100 style), page UI in English, study notes in Chinese. Mark theme words with `[[word]]` or `[[word|display]]`.
6. After you change `css/`, `js/`, `templates/`, or `build.py`, run `python3 sync_skill.py`.

## Project Map

- `index.html` home page (library). `articles/*.html` reading pages. `data/*.json` data.
- New users: [`QUICKSTART.md`](QUICKSTART.md). Design system: [`README.md`](README.md).

## First Contact

If the user is new to this project, explain the workflow in two or three sentences. Point to QUICKSTART.md. Then ask which article to process.
