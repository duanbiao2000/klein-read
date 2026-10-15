# Design System — Klein Read

Style target: a bright, lively paper notebook. Theme words use Klein blue. Do not change the design unless the user asks. New articles only need JSON. The build script applies the style.

## Colors

| Role | Hex | Use |
|---|---|---|
| Klein blue | `#002FA7` | Theme words, labels, titles, navigation, primary buttons |
| Bright blue | `#2B5CE6` | Hover state, part-of-speech pills |
| Blue mist / blue paper | `#EAF0FF` / `#F3F7FF` | Translation panel, light fills |
| Lemon | `#FFD23F` | Highlight marks, sticker shadow, decoration |
| Coral | `#FF6B57` | Wrong answers, warnings |
| Mint | `#19C2A8` | Correct answers, background icon |
| Violet | `#8B5CF6` | Sentence analysis panel |
| Pink | `#FF8FAB` | Decoration, expression icons |
| Paper | `#FFFDF6` | Page background with a blue dot grid |
| Ink | `#17233D` | Body text |

Rule: use at most three accent colors per screen. Klein blue stays dominant.

## Fonts

- Source text (English): Georgia, 17.5 px, line height 2.05.
- Source text (Japanese): Hiragino Mincho ProN, Yu Mincho, or Noto Serif JP. The build script sets this from `source_lang`.
- Chinese notes and UI: PingFang SC, Microsoft YaHei, or Noto Sans SC.
- Theme words: Klein blue, bold, dotted underline. Click opens the word note.

## Shape Language (three devices)

1. Sticker: section labels rotate −1.5°. Blue fill with a lemon hard shadow.
2. Marker: highlights use `linear-gradient(transparent 58%, color 58%)`.
3. Dots and radii: cards use 16–22 px radii. Dividers are dashed. Shadow: `0 8px 24px rgba(0,47,167,.08)`.

## Page Structure (split view)

```
1. Top bar       Logo, meta chips, A- / A+, demo mode button
2. Header        Chinese and source titles, blue guide card
3. Split window  The core layout. Two panes, each with its own scroll:
   - Left  (55%)  Source text. Serif type, paragraph numbers, Klein-blue theme words.
   - Right (45%)  Study notes. Theme words group, then one group per paragraph:
                  Translation (blue) / Words (lemon) / Analysis (violet) cards.
4. Post-reading  Background, Expressions, Practice, Discussion, Writing
5. Footer
```

Sync behavior: click a source paragraph to move the notes pane to its group. Click a group head to move the source pane. Keys `J`, `K`, or arrows move between paragraphs. Key `D` toggles demo mode. Demo mode hides all chrome and fills the viewport with the split window. This is the layout for screen recording.

## Component Names (css/style.css)

- Chips: `.chip`, `.chip-theme`, `.chip-lemon`, `.chip-mint`, `.chip-coral`, `.chip-violet`
- Sticker: `.sticker`. Highlights: `.mark-lemon`, `.mark-mint`, `.mark-coral`
- Buttons: `.btn`, `.btn-primary`, `.btn-secondary`. Top tools: `.tool`, `.tool.primary`
- Home cards: `.article-card` with `data-topic` and `data-source-lang` filters
- Split view: `.split-window`, `.pane-left`, `.pane-right`, `.pane-head`, `.sync-pill`
- Source text: `.source-text`, `.src-title`, `.src-sub`, `.src-para` (+ `.active`), `.para-no`, `.tword`
- Note groups: `.note-group` (+ `.active`), `.ng-head`, `.note-card`, `.nc-theme`
- Note cards: `.nc-tr` (translation), `.nc-words` (words), `.nc-analysis` (analysis), `.tr-text`, `.w-item`, `.w-note`
- Structure tags: `.struct-tag` with `.t-main`, `.t-clause`, `.t-phrase`, `.t-tip`
- Post-reading: `.bg-card`, `.expr-card`, `.quiz-card`, `.discuss-item`, `.write-card`, `.pager`

## When You Change the Design

- All tokens are in the `:root` block of `css/style.css`. Change `--klein` there to change the theme color.
- To add a topic, add one line to `TOPIC_COLORS` in `build.py`.
- After you change `css/`, `js/`, `templates/`, or `build.py`, run `python3 sync_skill.py`.
