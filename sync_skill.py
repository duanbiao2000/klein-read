#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_skill.py — 把主项目的「项目骨架」同步进技能包，并生成各 Agent 的发现副本。
运行时机：改动了 build.py / css / js / templates / data 模板 / SKILL.md 之后。
用法：python3 sync_skill.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skills" / "klein-read"
ASSETS = SKILL / "assets"

# 骨架文件：主项目 → skills/klein-read/assets/
FILES = [
    "build.py",
    "sync_skill.py",
    "QUICKSTART.md",
    "css/style.css",
    "js/app.js",
    "templates/article.tpl.html",
    "templates/index.tpl.html",
    "data/_template.json",
]
# 整目录拷贝的 glob（示例文章一并带上，新用户可直接看到成品效果）
GLOBS = ["data/00*.json"]


def main():
    # 1. 清理重建 assets
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    for rel in FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"· 跳过（不存在） {rel}")
            continue
        dst = ASSETS / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"✓ assets/{rel}")
    for pattern in GLOBS:
        for src in sorted(ROOT.glob(pattern)):
            dst = ASSETS / src.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✓ assets/{src.relative_to(ROOT)}")

    # 2. SKILL.md 副本 → .claude/skills/（Claude Code 项目内自动发现）
    for target_dir in [ROOT / ".claude" / "skills" / "klein-read"]:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SKILL / "SKILL.md", target_dir / "SKILL.md")
        print(f"✓ {target_dir.relative_to(ROOT)}/SKILL.md")

    print("同步完成 ✔")


if __name__ == "__main__":
    main()
