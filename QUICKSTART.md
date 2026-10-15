# 📘 QUICKSTART

**Klein Read** turns one weekly magazine article into one intensive-reading web page for Chinese college students. Paste an English or Japanese article. Get a Chinese translation, Klein-blue theme words, sentence analysis, and practice tasks in one page.

> Requirements: Python 3.8 or newer (standard library only). A web browser.

---

## 3 Steps to Start (no AI needed)

```bash
# 1. Enter the project folder.
cd klein-read

# 2. Open the site (or double-click index.html).
python3 -m http.server 8000      # Open http://localhost:8000

# 3. Rebuild after every data change.
python3 build.py
```

Article data lives in `data/*.json`. The build script generates `articles/*.html` and `index.html`. Do not edit the generated files.

---

## 🤖 Recommended: Let Your AI Agent Build Pages

This project ships rules for all major AI agents. The agent knows the workflow when it opens the project.

1. Open the `klein-read/` folder in your AI agent.
2. Paste an article and say: **"Make a reading page."**
3. The agent writes `data/NNN-slug.json` and runs `build.py`. Refresh the browser.

Supported agents and their rule files:

| AI agent | Rule file (included) | Note |
|---|---|---|
| Claude Code / Claude Desktop | `.claude/skills/klein-read/SKILL.md` | Auto-detected in the project |
| Cursor | `.cursor/rules/klein-read.mdc` | Auto-applied |
| GitHub Copilot | `.github/copilot-instructions.md` | Auto-applied |
| Codex CLI / Jules | `AGENTS.md` | Open standard |
| Windsurf | `.windsurf/rules/klein-read.md` | Auto-applied |
| Cline / Roo Code | `.clinerules/klein-read.md` | Auto-applied |
| Any other agent | `skills/klein-read/SKILL.md` | Import it as a skill or a system prompt |

All rule files are pointers. The single source of truth is `skills/klein-read/SKILL.md`. It has the full workflow, data schema, and quality rules.

---

## 🧩 Three Advanced Installs

**A. Global skill (install once, use in any project)**
```bash
# Claude Code, all projects:
cp -r skills/klein-read ~/.claude/skills/

# Other agents with skill support: copy skills/klein-read/ into the agent's
# skills folder, or upload the folder as a zip.
```
After install, say "Create a Klein Read project" in any empty folder. The agent copies the `assets/` skeleton and builds the full site.

**B. Claude Code plugin** — the repo root has `.claude-plugin/plugin.json`. Publish or install this repo as a plugin with `/plugin`.

**C. Manual** — copy `data/_template.json` to `data/NNN-slug.json`, fill it (see `skills/klein-read/references/schema.md`), and run `python3 build.py`.

---

## ❓ FAQ

- **What languages does the site use?** The UI is in English. The study notes are in Chinese. Source text can be English or Japanese.
- **How do I sync style or build changes?** Run `python3 sync_skill.py` after you change `css/`, `js/`, `templates/`, or `build.py`.
- **How do I add a topic?** Add one line to `TOPIC_COLORS` in `build.py`.
- **Can I paste several articles at once?** Yes. The agent creates one data file per article in order.
- **What do I back up?** Back up the `data/` folder. The site can be rebuilt at any time.
- **How do I publish the site?** Push to GitHub and set **Settings → Pages → Source: GitHub Actions**. The workflow deploys on every push to `main`. See README section 6.
- **Copyright:** the generated page is for personal study. Fill the `source` field with the true publication name.

---

## 📁 Folder Map

```
klein-read/
├── QUICKSTART.md          This file
├── README.md              Design system and full documentation
├── build.py               Generator
├── sync_skill.py          Skill sync script
├── index.html / articles/ Generated output (do not edit)
├── css/ js/ templates/    Style and templates
├── data/                  ★ Data. One JSON file per article.
└── skills/klein-read/     ★ Skill package (SKILL.md + references + assets)
```
