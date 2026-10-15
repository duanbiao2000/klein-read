# ASD-STE100 Style Rules for Klein Read Documentation

All Klein Read documentation uses Simplified Technical English (STE). STE is the controlled language of ASD-STE100. The full standard has 53 writing rules and a dictionary of about 900 approved words. The dictionary is proprietary. We apply the writing rules and the spirit of the dictionary.

When you write or edit any documentation file (README, QUICKSTART, SKILL, AGENTS, references, rule files), follow these rules.

## 1. Sentences

- Keep sentences short. Target: 20 words or fewer. Hard limit: 25 words.
- Put one instruction in one sentence. Do not join two steps with "and".
- Use the active voice. Write "Run build.py", not "build.py should be run".
- Use the imperative mood for steps. Write "Copy the folder", not "You can copy the folder".

## 2. Words

- Use short, common words. Write "use", not "utilize". Write "help", not "facilitate". Write "start", not "initiate".
- Give one word one meaning. Do not use synonyms for a key term.
- Use technical terms only when they are standard. Spell them the same way every time.

## 3. Terminology (use these exact terms)

| Term | Meaning | Do not use |
|---|---|---|
| article file | One JSON file in `data/` | data file, config, record |
| build script | `build.py` | generator, builder tool |
| project folder | The Klein Read root directory | repo root, workspace |
| skill package | `skills/klein-read/` | skill set, bundle |
| theme word | A key word in Klein blue | keyword, core word |
| study notes | Chinese notes for learners | annotations, commentary |
| source text | The original article text | original, passage |
| word note | The `note_zh` field content | usage note, remark |

## 4. Structure

- Put the action first in a procedure. Number the steps.
- Put conditions before actions. Write "If the project does not exist, create it".
- Use lists for three or more parallel items.
- Use tables for field lists and comparisons.

## 5. Avoid

- Do not use "and/or", "etc.", "respectively", or Latin abbreviations (e.g., i.e.).
- Do not use words like "obviously", "simply", "just".
- Do not use idioms or culture-specific metaphors in documentation.
- Do not use hedging: "might potentially be able to".

## 6. Punctuation

- Use the serial comma in English lists: "Translation, Words, and Analysis".
- Use two spaces after a sentence end is optional. Pick one style and stay with it. This project uses one space.

## Quick Check Before You Finish a Doc

1. Are all sentences 25 words or shorter?
2. Is every instruction in the active voice?
3. Did I use each key term exactly as in the table above?
4. Can a reader who does not speak English well follow the steps?
