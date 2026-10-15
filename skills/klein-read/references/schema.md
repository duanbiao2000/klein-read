# Data Schema — Article JSON File

One article = one file: `data/NNN-english-slug.json`. Use UTF-8 with real Chinese characters. `data/_template.json` is the blank template.

Language policy: `source_lang` marks the language of the source text. All study notes are in Chinese. See SKILL.md for the full language policy.

## Top-level Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | yes | str | Unique ID. Must equal the file name without `.json`. Example: `002-oshi-katsu`. |
| `title_src` | yes | str | Title in the source language. |
| `title_zh` | yes | str | Chinese title. |
| `paragraphs` | yes | list | Paragraph blocks. See below. |
| `source_lang` | no | str | `en` or `ja`. Default: `en`. |
| `source` | no | str | Publication name. Example: `The Economist`. Default: `Weekly`. |
| `date` | no | str | Publication date. Format: `YYYY-MM-DD`. |
| `updated` | no | str | Last content edit date. Format: `YYYY-MM-DD`. The home page sorts by `updated` (falls back to `date`), newest first. Set it to today when you edit an existing article. |
| `audio_url` | no | str | External audio page. If set, the article page shows an Audio tag in the top bar and a link under the guide. Both links open in a new tab. |
| `topic` | no | str | Topic for filtering and card color. Values: Workplace, Tech, Economy, Society, Environment, Education, Culture, Health, World, Business. |
| `difficulty` | no | int 1–5 | Difficulty stars. |
| `read_minutes` | no | int | Estimated reading time in minutes. |
| `word_count` | no | int | Word count of the source text. |
| `lead_zh` | no | str | Chinese guide. 80–150 characters. |
| `theme_words` | no | list | Theme words (Klein-blue cards). 6–10 items. |
| `background` | no | list | Context blocks: `{title_zh, body_zh}`. |
| `expressions` | no | list | Expression cards: `{expr, zh, usage_zh}`. `usage_zh` may contain `<b>`. |
| `quiz` | no | list | Practice items. See below. |
| `discussion_zh` | no | list[str] | Discussion questions in Chinese. |
| `writing` | no | obj | `{title_zh, prompt_zh}`. |

Delete a whole key when you do not use that block. The page adapts.

## theme_words[] — Theme Word

```json
{ "word": "crowd out", "phonetic": "/ˌkraʊd ˈaʊt/", "pos": "phr.v.", "meaning_zh": "挤占；排挤掉" }
```

- For Japanese words, put the kana reading in `phonetic`. Example: `"phonetic": "おしかつ"`.
- `pos` examples: `n.`, `v.`, `adj.`, `phr.`, `名`, `動五`.

## paragraphs[] — Paragraph

```json
{
  "text": "Source text with a [[crowd out|crowds out]] mark.",
  "zh": "中文译文……",
  "words": [
    { "word": "crowd out", "pos": "phr.v.", "meaning_zh": "挤占", "note_zh": "搭配或易错点" }
  ],
  "sentences": [
    {
      "text": "The full long sentence.",
      "structure": [
        { "type": "main",   "text": "主句成分说明" },
        { "type": "clause", "text": "从句成分说明" },
        { "type": "phrase", "text": "修饰成分说明" },
        { "type": "tip",    "text": "考点或写作提示" }
      ],
      "tip_zh": "整句学习要点。可省略。"
    }
  ]
}
```

- Theme word marks: `[[word]]` or `[[word|display]]`. The left side is the word form. The right side is the display text. The left side should match a `word` in `words[]` or `theme_words[]`. This enables the click-to-note link.
- `structure[].type` sets the tag color: `main` (blue), `clause` (violet), `phrase` (mint), `tip` (lemon).
- `structure[].tag` is optional. The build script picks the right label for the source language: 主句/从句/短语/考点 for English; 主干/从句/修饰语/考点 for Japanese.
- `words` and `sentences` are optional in each paragraph.

## quiz[] — Practice Item

Choice item. `answer` is the option index (0–3). The page maps it to A–D.

```json
{
  "type": "choice",
  "q": "Question text in the source language?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": 1,
  "explanation_zh": "中文解析。"
}
```

Fill item:

```json
{
  "type": "fill",
  "q": "Sentence with a blank ______ (hint).",
  "answer": "crowds out",
  "explanation_zh": "中文解析。"
}
```

## Field Aliases (accepted for compatibility)

| Canonical | Also accepted |
|---|---|
| `title_src` | `title_en` |
| `title_zh` | `title_cn` |
| `lead_zh` | `lead` |
| `paragraphs[].text` | `paragraphs[].en` |
| `paragraphs[].zh` | `paragraphs[].cn` |
| `meaning_zh` | `meaning` |
| `note_zh` | `note` |
| `tip_zh` | `tip` |
| `title_zh` (background, writing) | `title` |
| `body_zh` | `body` |
| `expr` | `en` (expressions) |
| `zh` (expressions) | `cn` |
| `usage_zh` | `usage` |
| `explanation_zh` | `explanation` |
| `discussion_zh` | `discussion` |
| `prompt_zh` | `prompt` |

Prefer the canonical names in new files.

## Full Example

See `data/001-slow-career.json` (English source) and `data/002-oshi-katsu.json` (Japanese source). They cover all fields and both source languages.
