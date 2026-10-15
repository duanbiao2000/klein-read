# Klein Read

This project turns a pasted English or Japanese weekly article into an intensive-reading web page for Chinese college students. Theme words use Klein blue.

Read and follow these files:
1. [`AGENTS.md`](AGENTS.md) — core rules and project map.
2. [`skills/klein-read/SKILL.md`](skills/klein-read/SKILL.md) — full workflow, data schema, and note quality rules. Single source of truth.

Key points: write each article to `data/NNN-slug.json`. Run `python3 build.py`. Do not edit `articles/` or `index.html`. Documentation in English (ASD-STE100 style). Study notes in Chinese.
