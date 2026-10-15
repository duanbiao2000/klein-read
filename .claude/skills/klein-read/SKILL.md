---
name: klein-read
description: Generates and extends "Klein Read" intensive-reading web pages from weekly magazine articles (English or Japanese) for Chinese college students. Use when the user pastes an article and asks for intensive reading (精读/外刊精读), a reading page, article analysis, or a new article for the site. Covers the JSON schema, the build workflow, note quality rules, Klein-blue design rules, and ASD-STE100-style documentation.
---

# Klein Read — Work Skill

Klein Read turns one weekly magazine article into one intensive-reading web page. The page gives a Chinese translation, theme words in Klein blue, sentence analysis, and practice tasks. The site is a static site. The build script uses Python standard library only.

## When to Use

- The user pastes an English or Japanese article and wants intensive reading.
- The user wants to add, extend, or update an article in an existing Klein Read project.
- The user asks how to use this project. Then read `QUICKSTART.md` and explain.

## Language Policy (follow strictly)

| Content | Language | Rule |
|---|---|---|
| Documentation (README, QUICKSTART, SKILL, references) | English | Follow ASD-STE100 rules. See `references/ste-style.md`. |
| Page UI (buttons, section titles, navigation) | English | Fixed in templates. Do not translate. |
| Study notes (translations, meanings, tips, explanations) | Chinese | Target reader: Chinese college students. |
| Source text | English or Japanese | Set `source_lang` to `en` or `ja`. |

If the user writes in English or Japanese, still write the study notes in Chinese. Reply to the user in their language.

## Core Workflow (5 steps)

### 1. Find the project
Search the workspace for a folder that has `build.py`, `data/`, and `templates/`.
- Project exists: extend it.
- No project: create one. Make a folder (default `./klein-read/`) and copy all files from this skill's `assets/` folder into it. Then tell the user about `index.html` and `QUICKSTART.md`.

### 2. Parse the pasted article
Extract the title, source name, date, and body paragraphs. Drop figure captions, links, and ads.
- No date: use today. No source: use `Weekly`.
- The user pastes several articles: create one data file per article. Build them in order.

### 3. Write the study notes
Keep the quality level high. Do not shorten these rules.

| Block | Count | Quality rule |
|---|---|---|
| `title_zh` | 1 | A vivid Chinese title. Do not translate word by word. |
| `lead_zh` | 1 | 80–150 Chinese characters. Say what the article covers and what the reader learns. |
| `theme_words` | 6–10 | Core concepts and useful collocations. Give phonetics, part of speech, and Chinese meaning. |
| `paragraphs[].zh` | 1 per paragraph | Faithful and natural Chinese. Split long sentences at Chinese rhythm. |
| `words[]` per paragraph | 3–5 | Pick words useful for CET-4/6 and postgraduate exams. In `note_zh`, add collocations or traps. |
| `sentences[]` per paragraph | 1–2 | Pick truly long or hard sentences. Break the structure into `main`, `clause`, `phrase`, `tip`. In `tip_zh`, add a writing or exam tip. |
| `quiz` | 3–5 | Mix choice and fill items. Make distractors plausible. Explain with an elimination method. |
| `discussion_zh` | 2–3 | Open questions. Link them to student life when possible. |
| `writing` | 1 | An exam-style task. Ask the reader to reuse at least two expressions from the article. |
| `background` and `expressions` | 1–3 each | Background gives context. Expressions must be reusable in writing. |

Mark theme words in the source text with `[[word]]` or `[[word|display]]`. Example: `[[crowd out|crowds out]]`. The left side is the word form. The right side is the display text. The page renders these marks in Klein blue and links them to the word notes.

For Japanese source text, use Japanese grammar labels in `structure` (主干, 从句, 修饰语, 考点). Write the analysis text in Chinese. Put kana readings in `phonetic`.

### 4. Write the data file
Path: `data/NNN-english-slug.json`. `NNN` is the next number after the highest number in `data/`. Use three digits. Use 2–4 English words for the slug.
Read `references/schema.md` before you write the file. Use UTF-8 with real Chinese characters. Delete blocks you do not use.

### 5. Build and report
Run this command in the project folder:

```bash
python3 build.py
```

Then report to the user: the new page path, the number of theme words, and the number of quiz items.
Do not edit `articles/*.html` or `index.html` by hand. The build script generates them.

## Design Rules (do not change)

- Theme words use Klein blue `#002FA7`. The build script does this from `theme_words` and `[[..]]` marks.
- The style is bright and lively. All design tokens live in `css/style.css`.
- Change `css/`, `js/`, `templates/`, or `build.py` only if the user asks for a design change.
- After you change those files, run `python3 sync_skill.py`. This keeps the skill package in sync.

## Common Problems

- The build script reports a missing key: check `id`, `title_src`, `title_zh`, and `paragraphs`. See `references/schema.md`.
- The user pastes a partial article: process the text you have. Skip empty blocks.
- The user pastes a web page with images: use the body text only.
- Copyright: the generated page is for personal study. Fill the `source` field with the true name.

## File Map

```
skills/klein-read/           This skill. You can copy the whole folder to install it.
├── SKILL.md                 This file. The single source of truth.
├── references/schema.md     Data schema. Full field list and example.
├── references/design.md     Design system. Colors, type, components.
├── references/ste-style.md  ASD-STE100 style rules for documentation.
└── assets/                  Project skeleton. Use it to create new projects.

Project folder
├── build.py                 Generator.
├── sync_skill.py            Sync script for the skill package.
├── data/*.json              Data. One file per article. The only source.
└── articles/ index.html     Generated output. Do not edit.
```
