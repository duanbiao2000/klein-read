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

## Page Structure (fixed seven blocks)

```
1. Header      Chinese and source titles, meta chips, blue guide card
2. Theme Words Klein-blue word cards
3. Close Reading  One card per paragraph with three panels:
   - Translation  blue mist
   - Words        lemon (word, POS pill, meaning, note)
   - Analysis     violet (main / clause / phrase / tip tags)
4. Background  mint icon
5. Expressions grid cards
6. Practice    choice quiz with instant feedback, fill quiz with answer key
7. Discussion and Writing
```

## Component Names (css/style.css)

- Chips: `.chip`, `.chip-theme`, `.chip-lemon`, `.chip-mint`, `.chip-coral`, `.chip-violet`
- Sticker: `.sticker`. Highlights: `.mark-lemon`, `.mark-mint`, `.mark-coral`
- Buttons: `.btn`, `.btn-primary`, `.btn-secondary`
- Home cards: `.article-card` with `data-topic` and `data-source-lang` filters
- Article page: `.lead-card`, `.theme-word-card`, `.para-card`, `.panel-cn`, `.panel-words`, `.panel-sent`, `.word-list`, `.sent-block`, `.struct-tag tag-main|tag-clause|tag-phrase|tag-tip`, `.quiz-card`, `.discuss-item`, `.expr-card`

## When You Change the Design

- All tokens are in the `:root` block of `css/style.css`. Change `--klein` there to change the theme color.
- To add a topic, add one line to `TOPIC_COLORS` in `build.py`.
- After you change `css/`, `js/`, `templates/`, or `build.py`, run `python3 sync_skill.py`.
