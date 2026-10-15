# Klein Read 🔵

Klein Read turns weekly magazine articles into intensive-reading web pages for Chinese college students. It supports English articles and Japanese articles. The study notes are in Chinese. Theme words use Klein blue.

Style target: a bright, lively paper notebook.

> 🚀 New users: start with [`QUICKSTART.md`](QUICKSTART.md).
> 🤖 AI agents: read [`skills/klein-read/SKILL.md`](skills/klein-read/SKILL.md). You can install it as a skill in any major agent.
> ▶️ Preview: open `index.html`, or run `python3 -m http.server 8000` in this folder and open http://localhost:8000
> ☁️ Publish: push to GitHub and enable GitHub Pages. The workflow `.github/workflows/deploy-pages.yml` deploys the site on every push to `main`.

---

## 1. Design System

### 1.1 Color — Klein blue leads, candy colors add energy

| Role | Color | Hex | Use |
|---|---|---|---|
| Theme words / primary | Klein blue | `#002FA7` | Theme word cards, marked words in text, titles, navigation, primary buttons |
| Bright blue | Klein bright | `#2B5CE6` | Hover state, POS pills |
| Blue mist | Klein mist | `#F3F7FF` | Translation panel fill |
| Lemon | Lemon | `#FFD23F` | Marker highlights, sticker shadow, stars |
| Coral | Coral | `#FF6B57` | Wrong answers, warnings |
| Mint | Mint | `#19C2A8` | Correct answers, background icon |
| Violet | Violet | `#8B5CF6` | Sentence analysis panel |
| Pink | Pink | `#FF8FAB` | Decoration, expression icons |
| Paper | Paper | `#FFFDF6` | Page background with a blue dot grid |
| Ink | Ink | `#17233D` | Body text |

Rule: use at most three accent colors per screen. Klein blue stays dominant. The site is lively but not noisy.

### 1.2 Type

- English source text: Georgia, line height 2.05.
- Japanese source text: Hiragino Mincho ProN or Yu Mincho.
- Chinese notes and UI: PingFang SC or Microsoft YaHei.

### 1.3 Shape language

1. Sticker: section labels rotate −1.5° with a lemon hard shadow.
2. Marker: highlights use a half-width gradient fill.
3. Dots and radii: card radii 16–22 px. Dividers are dashed.

### 1.4 Page structure (split view)

```
1. Top bar          Logo, meta chips, A- / A+, demo mode
2. Header           Chinese and source titles, blue guide card
3. Split window     Left (55%): source text. Right (45%): study notes.
                    Notes group by paragraph: Translation / Words / Analysis.
4. Post-reading     Background, Expressions, Practice, Discussion, Writing
5. Footer
```

Interactions for screen recording: click a paragraph to sync the notes pane. Press `J` / `K` to move between paragraphs. Press `D` for demo mode. Demo mode fills the viewport with the split window. Also: reading progress bar, click-to-note theme words, A- / A+ source font size, topic and language filters on the home page.

## 2. How to Add an Article

### Option A: Paste to your AI agent (recommended)

1. Open this project folder in your AI agent.
2. Paste the article text and say "Make a reading page".
3. The agent writes `data/NNN-slug.json` and runs `python3 build.py`.

### Option B: Manual

```bash
cp data/_template.json data/003-my-article.json   # Fill the fields.
python3 build.py                                   # Rebuild all pages.
```

### Data rules

- One article = one JSON file in `data/`. This is the only source you edit.
- The build script generates `articles/*.html` and `index.html`. Do not edit them by hand.
- Field reference: `skills/klein-read/references/schema.md`.
- Mark theme words with `[[word]]` or `[[word|display]]` in `paragraphs[].text`.

## 3. Folder Structure

```
klein-read/
├── QUICKSTART.md         # New-user guide
├── README.md             # This file
├── AGENTS.md             # AI agent rules (Codex, Jules, and others)
├── CLAUDE.md             # Claude Code pointer
├── build.py              # Generator: data/*.json -> pages
├── sync_skill.py         # Syncs the skill package assets
├── index.html            # Generated home page
├── css/ js/ templates/   # Style, interactions, page templates
├── data/                 # Data. One JSON file per article.
├── articles/             # Generated article pages
├── skills/klein-read/    # Distributable skill package
│   ├── SKILL.md          # Workflow and quality rules (single source of truth)
│   ├── references/       # schema.md, design.md, ste-style.md
│   └── assets/           # Project skeleton for new projects
├── .claude/skills/       # Claude Code project skill (from sync_skill.py)
├── .claude-plugin/       # Claude Code plugin manifest
├── .cursor/rules/        # Cursor rules (pointers)
├── .github/              # GitHub Copilot instructions (pointers)
├── .clinerules/          # Cline / Roo rules (pointers)
└── .windsurf/rules/      # Windsurf rules (pointers)
```

## 4. Design Changes

- Change the theme color: edit the `:root` tokens in `css/style.css`.
- Add a topic: add one line to `TOPIC_COLORS` in `build.py`.
- After you change style or build files, run `python3 sync_skill.py`.

## 5. Documentation Language and Style

All documentation is in English. It follows ASD-STE100 (Simplified Technical English) rules as far as possible. The core rules: short sentences, active voice, one instruction per sentence, and consistent terms. The full style list is in `skills/klein-read/references/ste-style.md`.

## 6. Publish with GitHub Pages

The repository is ready to push. It includes a Pages workflow. Follow these steps once.

### 6.1 Push the repository

```bash
git remote add origin git@github.com:YOUR_NAME/klein-read.git
git push -u origin main
```

### 6.2 Enable GitHub Pages

1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Source: GitHub Actions**.
4. Push any change to `main`. The workflow builds the site and publishes it.

The site URL looks like `https://YOUR_NAME.github.io/klein-read/`. The workflow runs `python3 build.py` before it deploys. The published site is always in sync with `data/`.

### 6.3 Alternative: deploy from a branch

1. Go to **Settings → Pages**.
2. Select **Deploy from a branch**.
3. Choose `main` and `/ (root)`.

This option serves the committed `index.html`. It does not run the build script.

### 6.4 Notes

- All page links are relative. The site works in a project subpath and at a custom domain.
- The workflow deploys only site files: `index.html`, `css/`, `js/`, and `articles/`.
- To change the license, edit `LICENSE` (default: MIT).

## 7. License

MIT. See `LICENSE`.
