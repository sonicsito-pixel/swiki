#!/usr/bin/env python3
"""원본 자료를 LLM 위키에 자동 등록한다.

이 스크립트는 심층 정리를 대체하지 않는다. Obsidian/wiki 메타데이터를
최신으로 유지하고, 안정적인 리소스 페이지를 만들며, 새로 추가되거나
변경된 파일을 사람/LLM 검토 대기열에 올린다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOTS = [
    ("원본", ROOT / "raw" / "sources"),
    ("첨부", ROOT / "raw" / "assets"),
]
WIKI_ROOT = ROOT / "wiki"
RESOURCE_DIR = WIKI_ROOT / "resources" / "auto"
STATE_DIR = ROOT / ".wiki_state"
STATE_FILE = STATE_DIR / "resource-state.json"

SKIP_NAMES = {"README.md", ".DS_Store", "Thumbs.db"}

EXT_KIND = {
    ".md": "마크다운",
    ".txt": "텍스트",
    ".html": "html",
    ".htm": "html",
    ".pdf": "PDF",
    ".doc": "문서",
    ".docx": "문서",
    ".xls": "스프레드시트",
    ".xlsx": "스프레드시트",
    ".csv": "스프레드시트",
    ".tsv": "스프레드시트",
    ".ppt": "프레젠테이션",
    ".pptx": "프레젠테이션",
    ".svg": "이미지",
    ".png": "이미지",
    ".jpg": "이미지",
    ".jpeg": "이미지",
    ".webp": "이미지",
    ".gif": "이미지",
    ".zip": "압축파일",
}

TERM_TAGS = {
    "FONE": "fone",
    "FA-ONE": "fa-one",
    "F-ONE": "fone",
    "ASIS": "현행",
    "AS-IS": "현행",
    "TOBE": "목표",
    "TO-BE": "목표",
    "PLM": "plm",
    "WMS": "wms",
    "POS": "pos",
    "Centric": "centric",
    "센트릭": "centric",
    "영업관리": "영업관리",
    "상품기획": "상품기획",
    "물류": "물류",
    "정산": "정산",
    "회의": "회의",
    "인터뷰": "인터뷰",
}


@dataclass(frozen=True)
class Resource:
    kind: str
    path: Path
    rel_path: str
    title: str
    ext: str
    size: int
    modified: str
    content_hash: str
    page_slug: str
    tags: tuple[str, ...]
    page_rel: str


def now_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def iso_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def safe_slug(text: str, fallback: str) -> str:
    ascii_text = text.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return ascii_text[:60].strip("-") or fallback


def page_slug_for(rel_path: str, title: str) -> str:
    path_hash = hashlib.sha1(rel_path.encode("utf-8")).hexdigest()[:10]
    base = safe_slug(title, "resource")
    return f"{base}-{path_hash}"


def infer_tags(rel_path: str, ext: str) -> tuple[str, ...]:
    tags = {"리소스", EXT_KIND.get(ext, "파일")}
    for needle, tag in TERM_TAGS.items():
        if needle.lower() in rel_path.lower():
            tags.add(tag)
    return tuple(sorted(tags))


def scan_resources() -> list[Resource]:
    resources: list[Resource] = []
    for kind, raw_root in RAW_ROOTS:
        if not raw_root.exists():
            continue
        for path in sorted(raw_root.rglob("*")):
            if not path.is_file():
                continue
            if path.name in SKIP_NAMES:
                continue
            if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            ext = path.suffix.lower()
            rel_path = rel_posix(path)
            title = path.stem
            page_slug = page_slug_for(rel_path, title)
            page_rel = f"resources/auto/{page_slug}.md"
            resources.append(
                Resource(
                    kind=kind,
                    path=path,
                    rel_path=rel_path,
                    title=title,
                    ext=ext or "(none)",
                    size=path.stat().st_size,
                    modified=iso_mtime(path),
                    content_hash=sha256_file(path),
                    page_slug=page_slug,
                    tags=infer_tags(rel_path, ext),
                    page_rel=page_rel,
                )
            )
    return resources


def load_state() -> dict[str, dict[str, str]]:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(resources: Iterable[Resource]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        r.rel_path: {
            "hash": r.content_hash,
            "modified": r.modified,
            "page": r.page_rel,
        }
        for r in resources
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def event_for(resource: Resource, previous: dict[str, dict[str, str]], baseline: bool) -> str:
    if baseline:
        return "등록됨"
    old = previous.get(resource.rel_path)
    if old is None:
        return "신규"
    if old.get("hash") != resource.content_hash:
        return "변경됨"
    return "등록됨"


def covered_by_page(resource: Resource) -> str:
    if resource.rel_path.startswith("raw/sources/ASIS분석자료(FONE)/"):
        return "asis-fone-folder-ingest"
    if resource.rel_path.startswith("raw/sources/현업인터뷰자료/"):
        return "field-interview-master-data-summary"
    return ""


def covered_page_label(page_slug: str) -> str:
    labels = {
        "asis-fone-folder-ingest": "FONE AS-IS 자료 묶음 정리",
        "field-interview-master-data-summary": "현업인터뷰 기준정보 분석",
    }
    return labels.get(page_slug, page_slug)


def wiki_link(page_rel: str, label: str) -> str:
    return f"[[{Path(page_rel).stem}|{label}]]"


def yaml_list(items: Iterable[str]) -> str:
    values = list(items)
    if not values:
        return "[]"
    return "\n" + "\n".join(f"  - {item}" for item in values)


def write_resource_page(resource: Resource, event: str) -> None:
    RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    page_path = WIKI_ROOT / resource.page_rel
    covered = covered_by_page(resource)
    status = "심층정리-대기" if event in {"신규", "변경됨"} and not covered else "등록됨"
    if covered and event in {"신규", "변경됨"}:
        status = "검토대기"

    content = f"""---
type: resource
title: {json.dumps(resource.title, ensure_ascii=False)}
resource_kind: {resource.kind}
source_path: {json.dumps(resource.rel_path, ensure_ascii=False)}
extension: {resource.ext}
size_bytes: {resource.size}
modified_utc: {resource.modified}
content_hash: {resource.content_hash}
status: {status}
auto_generated: true
updated: {now_date()}
tags:{yaml_list(resource.tags)}
---

# {resource.title}

## 원본 정보

- 경로: `{resource.rel_path}`
- 구분: `{resource.kind}`
- 확장자: `{resource.ext}`
- 크기: {resource.size:,} bytes
- 수정시각(UTC): `{resource.modified}`
- SHA-256: `{resource.content_hash}`

## 정리 상태

- 자동 감지 상태: `{event}`
- 현재 상태: `{status}`
"""
    if covered:
        content += f"- 묶음 요약 페이지: [[{covered}|{covered_page_label(covered)}]]\n"
    else:
        content += "- 묶음 요약 페이지: 없음\n"

    content += """
## 메모

이 페이지는 원본 리소스 목록에서 자동 생성된 등록 페이지다. 심층 요약 페이지가 아니라 자료의 존재와 상태를 추적하기 위한 메타데이터 페이지다.

## 다음 작업

- TODO(user): 이 리소스를 심층 정리할지 결정한다.
- TODO(user): 필요하면 LLM에게 이 파일의 원문 요약 페이지를 만들거나 갱신하도록 요청한다.
"""
    page_path.write_text(content, encoding="utf-8", newline="\n")


def write_registry(resources: list[Resource], events: dict[str, str]) -> None:
    by_kind: dict[str, list[Resource]] = {}
    by_ext: dict[str, list[Resource]] = {}
    for r in resources:
        by_kind.setdefault(r.kind, []).append(r)
        by_ext.setdefault(r.ext, []).append(r)

    lines = [
        "---",
        "type: registry",
        f"updated: {now_date()}",
        f"resource_count: {len(resources)}",
        "---",
        "",
        "# 원본 자료 목록",
        "",
        "이 파일은 `raw/` 아래 리소스를 자동으로 스캔해 만든 레지스트리다.",
        "직접 편집하지 말고 `tools/wiki_auto_index.py`를 다시 실행해 갱신한다.",
        "",
        "## 요약",
        "",
        f"- 전체 리소스: {len(resources)}",
    ]
    for kind, rows in sorted(by_kind.items()):
        lines.append(f"- {kind}: {len(rows)}")
    lines += ["", "## 확장자별 현황", ""]
    for ext, rows in sorted(by_ext.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append(f"- `{ext}`: {len(rows)}")

    lines += ["", "## 리소스 목록", ""]
    lines.append("| 리소스 | 구분 | 확장자 | 상태 | 크기 | 경로 |")
    lines.append("| --- | --- | --- | --- | ---: | --- |")
    for r in resources:
        event = events.get(r.rel_path, "registered")
        status = "대기" if event in {"신규", "변경됨"} else "등록됨"
        if covered_by_page(r):
            status = "묶음정리됨" if status == "등록됨" else "검토대기"
        lines.append(
            f"| {wiki_link(r.page_rel, r.title)} | {r.kind} | `{r.ext}` | {status} | {r.size:,} | `{r.rel_path}` |"
        )
    lines.append("")
    (WIKI_ROOT / "source-registry.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_pending(resources: list[Resource], events: dict[str, str], baseline: bool) -> None:
    pending = [r for r in resources if events.get(r.rel_path) in {"new", "changed"}]
    lines = [
        "---",
        "type: pending-ingest",
        f"updated: {now_date()}",
        f"pending_count: {len(pending)}",
        "---",
        "",
        "# 심층 정리 대기열",
        "",
        "새로 추가되거나 변경된 원본 리소스를 심층 정리하기 위한 대기열이다.",
        "",
    ]
    if baseline:
        lines += [
            "현재 실행은 기준 등록 모드였다. 기존 파일들은 대기열에 넣지 않고 원본 자료 목록에 등록했다.",
            "",
        ]
    if not pending:
        lines += [
            "## 대기열",
            "",
            "현재 새로 심층 정리해야 할 리소스가 없다.",
            "",
        ]
    else:
        lines += ["## 대기열", ""]
        for r in pending:
            event = events[r.rel_path]
            lines += [
                f"### {r.title}",
                "",
                f"- 리소스 페이지: {wiki_link(r.page_rel, r.title)}",
                f"- 감지 상태: `{event}`",
                f"- 경로: `{r.rel_path}`",
                f"- 확장자: `{r.ext}`",
                f"- 크기: {r.size:,} bytes",
                "",
                "TODO(user): 이 리소스를 심층 정리할지 결정한다.",
                "",
            ]
    lines += [
        "## 추천 요청문",
        "",
        "```text",
        "wiki/pending-ingest.md의 대기열을 보고 우선순위가 높은 리소스를 심층 정리해줘.",
        "원문 요약을 만들고, 관련 개념/대상 페이지를 갱신하고,",
        "index.md와 log.md도 업데이트해줘.",
        "판단이 필요한 항목은 TODO(user)로 남겨줘.",
        "```",
        "",
    ]
    (WIKI_ROOT / "pending-ingest.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_obsidian_home(resources: list[Resource]) -> None:
    lines = [
        "---",
        "type: dashboard",
        f"updated: {now_date()}",
        "---",
        "",
        "# 옵시디언 홈",
        "",
        "이 페이지는 Obsidian에서 열었을 때의 시작점이다.",
        "",
        "## 바로가기",
        "",
        "- [[overview|전체 개요]]",
        "- [[index|위키 목차]]",
        "- [[source-registry|원본 자료 목록]]",
        "- [[pending-ingest|심층 정리 대기열]]",
        "- [[log|작업 기록]]",
        "- [[fone-next-decisions|FONE 다음 의사결정]]",
        "",
        "## 현재 중점",
        "",
        "- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]",
        "- [[fone-as-is-analysis|FONE 현행 분석]]",
        "- [[master-data-governance|기준정보 관리 체계]]",
        "- [[plm-fone-integration|PLM-FONE 연계]]",
        "- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]",
        "- [[sales-settlement-automation|영업관리 정산 자동화]]",
        "",
        "## 리소스 현황",
        "",
        f"- 등록된 리소스: {len(resources)}",
        "",
        "## 자동화",
        "",
        "- 한 번 갱신: `python tools/wiki_auto_index.py`",
        "- 원본 폴더 감시: `powershell -ExecutionPolicy Bypass -File tools/watch_sources.ps1`",
        "",
    ]
    (WIKI_ROOT / "obsidian-home.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def update_index_links() -> None:
    index = WIKI_ROOT / "index.md"
    text = index.read_text(encoding="utf-8")
    additions = [
        "- [[source-registry|원본 자료 목록]] - `raw/` 리소스 자동 등록 현황.",
        "- [[pending-ingest|심층 정리 대기열]] - 새로 추가되거나 변경된 리소스의 심층 정리 대기열.",
        "- [[obsidian-home|옵시디언 홈]] - Obsidian용 시작 페이지.",
    ]
    if "## Automation" not in text:
        insert = "\n## Automation\n\n" + "\n".join(additions) + "\n"
        text = text.replace("\n## TODO(user)\n", insert + "\n## TODO(user)\n")
    else:
        for line in additions:
            if line not in text:
                text = text.replace("## Automation\n", f"## Automation\n\n{line}\n")
    index.write_text(text, encoding="utf-8", newline="\n")


def append_log(resources: list[Resource], events: dict[str, str], baseline: bool) -> None:
    new_count = sum(1 for e in events.values() if e == "new")
    changed_count = sum(1 for e in events.values() if e == "changed")
    log_path = WIKI_ROOT / "log.md"
    text = log_path.read_text(encoding="utf-8")
    entry_title = f"## [{now_stamp()}] 자동화 | 원본 자료 목록 갱신"
    mode = "기준등록" if baseline else "증분갱신"
    entry = f"""
{entry_title}

- 실행 모드: {mode}
- 등록 리소스: {len(resources)}
- 신규 대기 리소스: {new_count}
- 변경 대기 리소스: {changed_count}
- `wiki/source-registry.md`, `wiki/pending-ingest.md`, `wiki/obsidian-home.md`를 갱신했다.
"""
    text = text.replace("\n## [", entry + "\n## [", 1)
    log_path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Register raw resources into the wiki.")
    parser.add_argument("--baseline", action="store_true", help="Register existing files without queuing them.")
    parser.add_argument("--no-log", action="store_true", help="Do not append an automation log entry.")
    args = parser.parse_args()

    resources = scan_resources()
    previous = load_state()
    events = {r.rel_path: event_for(r, previous, args.baseline) for r in resources}

    for resource in resources:
        write_resource_page(resource, events[resource.rel_path])
    write_registry(resources, events)
    write_pending(resources, events, args.baseline)
    write_obsidian_home(resources)
    update_index_links()
    if not args.no_log:
        append_log(resources, events, args.baseline)
    save_state(resources)

    new_count = sum(1 for e in events.values() if e == "new")
    changed_count = sum(1 for e in events.values() if e == "changed")
    print(f"registered={len(resources)} new={new_count} changed={changed_count} baseline={args.baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
