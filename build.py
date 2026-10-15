#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Klein Read generator.

Usage:
    python3 build.py            # Rebuild all article pages and the index.

Add an article:
    1. Copy data/_template.json to data/NNN-slug.json and fill it.
       (Or ask your AI agent to create it from a pasted article.)
    2. Run python3 build.py.

Layout:
    Article pages use a split view. The left pane shows the source text.
    The right pane shows the study notes, grouped by paragraph.

Output:
    articles/NNN-slug.html and index.html. Do not edit these files by hand.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
TPL_DIR = ROOT / "templates"
ART_DIR = ROOT / "articles"

# Topic -> accent color on cards.
TOPIC_COLORS = {
    "Workplace": "#002FA7", "Tech": "#8B5CF6", "Economy": "#FFB800",
    "Society": "#FF6B57", "Environment": "#19C2A8", "Education": "#2B5CE6",
    "Culture": "#FF8FAB", "Health": "#19C2A8", "World": "#002FA7",
    "Business": "#FFB800",
}
DEFAULT_COLOR = "#002FA7"

# Sentence-structure tag labels. Notes are in Chinese. The labels follow
# the source language so that the grammar terms stay correct.
STRUCT_TAGS = {
    "en": {"main": "主句", "clause": "从句", "phrase": "短语", "tip": "考点"},
    "ja": {"main": "主干", "clause": "从句", "phrase": "修饰语", "tip": "考点"},
}

SOURCE_LANG_LABEL = {"en": "English", "ja": "Japanese"}


def esc(s):
    return html.escape(str(s), quote=True)


def render(tpl_name, ctx):
    t = (TPL_DIR / tpl_name).read_text(encoding="utf-8")
    for k, v in ctx.items():
        t = t.replace("{{" + k + "}}", v)
    return t


def markup_keywords(s):
    """Turn [[word]] or [[word|display]] marks into Klein-blue theme words."""
    s = esc(s)

    def repl(m):
        key, disp = m.group(1), m.group(2)
        return f'<span class="tword" data-word="{key}">{disp}</span>'

    s = re.sub(r"\[\[([^|\[\]]+)\|([^\[\]]+)\]\]", repl, s)
    s = re.sub(
        r"\[\[([^\[\]]+)\]\]",
        lambda m: f'<span class="tword" data-word="{m.group(1)}">{m.group(1)}</span>',
        s,
    )
    return s


def difficulty_html(level):
    level = int(level or 3)
    stars = "".join(
        "★" if i < level else '<span class="off">★</span>' for i in range(1, 6)
    )
    return f'<span class="stars">{stars}</span> Difficulty {level}/5'


def get_text(p, *keys):
    for k in keys:
        if p.get(k) is not None:
            return p[k]
    return ""


# ---------------- Block renderers ----------------

def render_theme_words(words):
    cards = []
    for w in words:
        ph = " · ".join(
            x for x in [esc(w.get("phonetic", "")), esc(w.get("pos", ""))] if x
        )
        cards.append(
            f'<div class="theme-word-card"><span class="w">{esc(w["word"])}</span>'
            f'<span class="ph">{ph}</span><span class="m">{esc(get_text(w, "meaning_zh", "meaning"))}</span></div>'
        )
    return "\n".join(cards)


def render_source_paras(paras, source_lang):
    """Left pane: typeset source text with paragraph numbers."""
    lang_attr = source_lang if source_lang in ("en", "ja") else "en"
    out = []
    for i, p in enumerate(paras, 1):
        out.append(
            f'<p class="src-para" id="sp{i}" data-para="{i}" lang="{lang_attr}">'
            f'<span class="para-no">P{i}</span> {markup_keywords(get_text(p, "text", "en"))}</p>'
        )
    return "\n".join(out)


def render_note_groups(paras, source_lang):
    """Right pane: study-note card groups, one group per paragraph."""
    tags = STRUCT_TAGS.get(source_lang, STRUCT_TAGS["en"])
    out = []
    for i, p in enumerate(paras, 1):
        cards = []

        zh = get_text(p, "zh", "cn")
        if zh:
            cards.append(
                f'<div class="note-card nc-tr"><div class="nc-title">参考译文 · TRANSLATION</div>'
                f'<p class="tr-text" lang="zh-CN">{esc(zh)}</p></div>'
            )

        word_items = ""
        for w in p.get("words", []):
            note = get_text(w, "note_zh", "note")
            word_items += (
                f'<div class="w-item"><span class="w">{esc(w["word"])}</span>'
                f'<span class="pos">{esc(w.get("pos", ""))}</span>'
                f'<span class="m">{esc(get_text(w, "meaning_zh", "meaning"))}</span></div>'
            )
            if note:
                word_items += f'<div class="w-note">💡 {esc(note)}</div>'
        if word_items:
            cards.append(
                f'<div class="note-card nc-words"><div class="nc-title">本段词汇 · WORDS</div>{word_items}</div>'
            )

        sent_blocks = ""
        for s in p.get("sentences", []):
            tip = get_text(s, "tip_zh", "tip")
            lines = ""
            for l in s.get("structure", []):
                tag = l.get("tag") or tags.get(l.get("type", "phrase"), "")
                lines += (
                    f'<div class="struct-line"><span class="struct-tag t-{esc(l.get("type", "phrase"))}">{esc(tag)}</span>'
                    f'<span class="struct-text">{esc(l.get("text", ""))}</span></div>'
                )
            sent_blocks += (
                f'<p class="sent-quote">{esc(get_text(s, "text", "en"))}</p>{lines}'
            )
            if tip:
                sent_blocks += (
                    f'<div class="struct-line"><span class="struct-tag t-tip">{esc(tags["tip"])}</span>'
                    f'<span class="struct-text">{esc(tip)}</span></div>'
                )
        if sent_blocks:
            cards.append(
                f'<div class="note-card nc-analysis"><div class="nc-title">长难句解析 · ANALYSIS</div>{sent_blocks}</div>'
            )

        out.append(
            f'<div class="note-group" id="ng{i}" data-para="{i}">'
            f'<div class="ng-head">PARA {i} · 讲解</div>{"".join(cards)}</div>'
        )
    return "\n".join(out)


def render_background(items):
    if not items:
        return '<div class="card bg-card"><p>No background notes for this article.</p></div>'
    return "\n".join(
        f'<div class="card bg-card"><h3>{esc(get_text(b, "title_zh", "title"))}</h3><p lang="zh-CN">{esc(get_text(b, "body_zh", "body"))}</p></div>'
        for b in items
    )


def render_expressions(items, source_lang="en"):
    if not items:
        return '<div class="expr-card"><p class="cn">No expression cards for this article.</p></div>'
    lang_attr = source_lang if source_lang in ("en", "ja") else "en"
    return "\n".join(
        f'<div class="expr-card"><p class="en" lang="{lang_attr}">{esc(get_text(e, "expr", "en"))}</p><p class="cn" lang="zh-CN">{esc(get_text(e, "zh", "cn"))}</p>'
        f'<p class="use">📌 {get_text(e, "usage_zh", "usage")}</p></div>'
        for e in items
    )


def render_quiz(items):
    if not items:
        return '<div class="card quiz-card"><p class="quiz-q">No practice questions for this article.</p></div>'
    out = []
    for q in items:
        if q.get("type") == "fill":
            out.append(f"""
<div class="quiz-card card" data-fill-answer="{esc(q["answer"])}">
  <span class="quiz-type fill">FILL IN</span>
  <p class="quiz-q">{esc(q["q"])}</p>
  <div class="fill-row">
    <input class="fill-input" type="text" placeholder="Type the answer, then show the key">
    <button class="btn btn-primary reveal-btn" style="padding:10px 22px">Show Answer</button>
  </div>
  <div class="quiz-explain"><b>Explanation:</b> {esc(get_text(q, "explanation_zh", "explanation"))}</div>
</div>""")
        else:
            keys = "ABCD"
            opts = "".join(
                f'<button class="option"><span class="key">{keys[j]}</span><span>{esc(o)}</span></button>'
                for j, o in enumerate(q.get("options", []))
            )
            out.append(f"""
<div class="quiz-card card" data-answer="{keys[int(q.get("answer", 0))]}">
  <span class="quiz-type choice">CHOICE</span>
  <p class="quiz-q">{esc(q["q"])}</p>
  <div class="options">{opts}</div>
  <div class="quiz-explain"><b>Explanation:</b> {esc(get_text(q, "explanation_zh", "explanation"))}</div>
</div>""")
    return "\n".join(out)


def render_discussion(items):
    if not items:
        return '<div class="discuss-item"><p>No discussion questions for this article.</p></div>'
    return "\n".join(
        f'<div class="discuss-item"><span class="q-mark">Q{i}</span><p lang="zh-CN">{esc(d)}</p></div>'
        for i, d in enumerate(items, 1)
    )


def render_writing(w):
    if not w:
        return ""
    return (
        f'<div class="card quiz-card write-card"><h3>{esc(get_text(w, "title_zh", "title") or "Writing Task")}</h3>'
        f'<p lang="zh-CN">{esc(get_text(w, "prompt_zh", "prompt"))}</p></div>'
    )


def render_pager(prev_doc, next_doc):
    def link(doc, cls, label):
        if not doc:
            return (
                f'<div><p class="dir">{label}</p>'
                f'<p class="t" style="color:var(--ink-30)">No more articles</p></div>'
            )
        return (
            f'<a class="{cls}" href="{esc(doc["id"])}.html"><p class="dir">{label}</p>'
            f'<p class="t">{esc(doc["title_zh"])}</p></a>'
        )

    return link(prev_doc, "prev", "← Previous") + link(next_doc, "next", "Next →")


# ---------------- Build entry ----------------

def load_docs():
    docs = []
    for f in sorted(DATA_DIR.glob("*.json")):
        if f.name.startswith("_"):
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        doc["_file"] = f.name
        # Field aliases (v1 -> v2). Keep both names valid.
        doc.setdefault("source_lang", "en")
        if "title_src" not in doc and "title_en" in doc:
            doc["title_src"] = doc["title_en"]
        if "title_zh" not in doc and "title_cn" in doc:
            doc["title_zh"] = doc["title_cn"]
        docs.append(doc)
    docs.sort(key=lambda d: d["id"])
    return docs


def build_article(doc, prev_doc, next_doc):
    source_lang = doc.get("source_lang", "en")
    paras = doc.get("paragraphs", [])
    ctx = {
        "TITLE_ZH": esc(doc.get("title_zh", "")),
        "TITLE_SRC": esc(doc.get("title_src", "")),
        "SOURCE": esc(doc.get("source", "Weekly")),
        "DATE": esc(doc.get("date", "")),
        "TOPIC": esc(doc.get("topic", "General")),
        "SOURCE_LANG_LABEL": SOURCE_LANG_LABEL.get(source_lang, source_lang),
        "SOURCE_LANG": esc(source_lang),
        "DIFFICULTY_HTML": difficulty_html(doc.get("difficulty", 3)),
        "READ_MIN": esc(doc.get("read_minutes", 10)),
        "WORD_COUNT": esc(doc.get("word_count", "")),
        "LEAD": esc(get_text(doc, "lead_zh", "lead")),
        "THEME_WORDS": render_theme_words(doc.get("theme_words", [])),
        "SOURCE_PARAS": render_source_paras(paras, source_lang),
        "NOTE_GROUPS": render_note_groups(paras, source_lang),
        "BACKGROUND": render_background(doc.get("background", [])),
        "EXPRESSIONS": render_expressions(doc.get("expressions", []), source_lang),
        "QUIZ": render_quiz(doc.get("quiz", [])),
        "DISCUSSION": render_discussion(doc.get("discussion_zh") or doc.get("discussion") or []),
        "WRITING": render_writing(doc.get("writing")),
        "PAGER": render_pager(prev_doc, next_doc),
    }
    out = ART_DIR / f'{doc["id"]}.html'
    out.write_text(render("article.tpl.html", ctx), encoding="utf-8")
    return out


def build_index(docs):
    cards = []
    topics = []
    for d in docs:
        topic = d.get("topic", "General")
        if topic not in topics:
            topics.append(topic)
        color = TOPIC_COLORS.get(topic, DEFAULT_COLOR)
        stars = difficulty_html(d.get("difficulty", 3))
        src_lang = d.get("source_lang", "en")
        theme = " ".join(
            f'<span class="chip chip-theme" style="font-size:11px;padding:2px 10px">{esc(w["word"])}</span>'
            for w in d.get("theme_words", [])[:3]
        )
        cards.append(f"""
<a class="article-card" href="articles/{esc(d["id"])}.html" data-topic="{esc(topic)}" data-source-lang="{esc(src_lang)}">
  <span class="accent" style="background:{color}"></span>
  <div class="card-meta">
    <span class="card-source">{esc(d.get("source", "Weekly"))}</span>
    <span class="chip" style="font-size:11px;padding:2px 10px">{esc(topic)}</span>
    <span class="chip chip-violet" style="font-size:11px;padding:2px 10px">{esc(SOURCE_LANG_LABEL.get(src_lang, src_lang))}</span>
    <span class="card-date">{esc(d.get("date", ""))}</span>
  </div>
  <h3 lang="zh-CN">{esc(d.get("title_zh", ""))}</h3>
  <p class="card-title-en">{esc(d.get("title_src", ""))}</p>
  <p class="card-desc" lang="zh-CN">{esc(get_text(d, "lead_zh", "lead"))}</p>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 0">{theme}</div>
  <div class="card-foot">
    <span>{stars}</span>
    <span class="card-go">Start reading →</span>
  </div>
</a>""")

    filters = '<button class="filter-chip active" data-topic="all">All topics</button>' + "".join(
        f'<button class="filter-chip" data-topic="{esc(t)}">{esc(t)}</button>' for t in topics
    )
    lang_filters = (
        '<button class="filter-chip active" data-source-lang="all">All languages</button>'
        '<button class="filter-chip" data-source-lang="en">English</button>'
        '<button class="filter-chip" data-source-lang="ja">Japanese</button>'
    )
    first = f'articles/{docs[0]["id"]}.html' if docs else "#library"
    ctx = {
        "ARTICLE_CARDS": "\n".join(cards)
        or "<p>No articles yet. Add a JSON file in data/ and run build.py.</p>",
        "FILTERS": filters,
        "LANG_FILTERS": lang_filters,
        "COUNT": str(len(docs)),
        "FIRST_ARTICLE_URL": first,
    }
    out = ROOT / "index.html"
    out.write_text(render("index.tpl.html", ctx), encoding="utf-8")
    return out


def main():
    ART_DIR.mkdir(exist_ok=True)
    docs = load_docs()
    for i, doc in enumerate(docs):
        prev_doc = docs[i - 1] if i > 0 else None
        next_doc = docs[i + 1] if i < len(docs) - 1 else None
        out = build_article(doc, prev_doc, next_doc)
        print(f"OK  article page  {out.relative_to(ROOT)}")
    out = build_index(docs)
    print(f"OK  index page    {out.relative_to(ROOT)}  ({len(docs)} articles)")


if __name__ == "__main__":
    main()
