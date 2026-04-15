#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))


STATE_ROOT = codex_home() / "state" / "preference-model-zh"
PROFILE_JSON = STATE_ROOT / "profile.json"
PROFILE_MD = STATE_ROOT / "profile.md"
SESSION_BRIEF = STATE_ROOT / "session-brief.md"
INTERVIEW_LOG = STATE_ROOT / "interview-log.md"
CHANGE_LOG = STATE_ROOT / "change-log.md"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def default_profile() -> dict[str, Any]:
    timestamp = now_iso()
    return {
        "meta": {
            "version": 1,
            "created_at": timestamp,
            "updated_at": timestamp,
            "revision": 0,
            "sources": [],
        },
        "identity": {
            "preferred_name": "",
            "roles": [],
            "context": "",
        },
        "interaction_style": {
            "language": "zh-CN",
            "tone": [],
            "verbosity": "",
            "structure": [],
            "challenge_level": "",
            "humor": "",
            "pace": "",
        },
        "workflow": {
            "autonomy": "",
            "ask_vs_assume": "",
            "planning_style": "",
            "options_style": "",
            "risk_tolerance": "",
            "decision_style": "",
            "tool_use": "",
        },
        "output_preferences": {
            "default_format": "",
            "code_explanations": "",
            "summaries": "",
            "examples": "",
            "tables": "",
            "citations": "",
        },
        "domain_preferences": {
            "coding": {},
            "writing": {},
            "research": {},
            "general": {},
        },
        "anti_preferences": [],
        "decision_rules": [],
        "examples": [],
        "open_questions": [],
        "confidence_notes": [],
        "assistant_prompts": {
            "session_preamble": "",
            "custom_instructions_snippet": "",
        },
    }


def ensure_state() -> dict[str, Any]:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    if PROFILE_JSON.exists():
        profile = load_profile()
    else:
        profile = default_profile()
        write_profile(profile)
    if not INTERVIEW_LOG.exists():
        INTERVIEW_LOG.write_text("# Interview Log\n\n", encoding="utf-8")
    if not CHANGE_LOG.exists():
        CHANGE_LOG.write_text("# Change Log\n\n", encoding="utf-8")
    if not PROFILE_MD.exists() or not SESSION_BRIEF.exists():
        write_profile(profile)
    return profile


def load_profile() -> dict[str, Any]:
    if not PROFILE_JSON.exists():
        return default_profile()
    try:
        data = json.loads(PROFILE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {PROFILE_JSON}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{PROFILE_JSON} must contain a JSON object.")
    return data


def deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        merged = copy.deepcopy(base)
        for key, value in patch.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = copy.deepcopy(value)
        return merged
    return copy.deepcopy(patch)


def collect_changes(before: Any, after: Any, prefix: str = "") -> list[str]:
    if type(before) is not type(after):
        return [prefix or "<root>"]
    if isinstance(before, dict):
        changes: list[str] = []
        keys = set(before) | set(after)
        for key in sorted(keys):
            path = f"{prefix}.{key}" if prefix else key
            if key not in before or key not in after:
                changes.append(path)
                continue
            changes.extend(collect_changes(before[key], after[key], path))
        return changes
    if before != after:
        return [prefix or "<root>"]
    return []


def compact_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def bulletify(values: list[Any], empty: str = "- none") -> str:
    if not values:
        return empty
    lines = []
    for value in values:
        if isinstance(value, dict):
            lines.append(f"- {json.dumps(value, ensure_ascii=False, sort_keys=True)}")
        else:
            lines.append(f"- {value}")
    return "\n".join(lines)


def key_values(data: dict[str, Any], empty: str = "- none") -> str:
    pairs = []
    for key, value in data.items():
        if value in ("", [], {}, None):
            continue
        if isinstance(value, list):
            pairs.append(f"- {key}: {', '.join(str(item) for item in value)}")
        elif isinstance(value, dict):
            pairs.append(f"- {key}: {json.dumps(value, ensure_ascii=False, sort_keys=True)}")
        else:
            pairs.append(f"- {key}: {value}")
    return "\n".join(pairs) if pairs else empty


def build_session_preamble(profile: dict[str, Any]) -> str:
    style = profile.get("interaction_style", {})
    workflow = profile.get("workflow", {})
    output = profile.get("output_preferences", {})
    anti = profile.get("anti_preferences", [])
    rules = profile.get("decision_rules", [])

    lines = [
        "Apply these defaults unless the user overrides them in the current chat.",
    ]
    if style:
        tone = ", ".join(style.get("tone", []))
        if tone or style.get("verbosity") or style.get("language"):
            lines.append(
                "Style: "
                + "; ".join(
                    part
                    for part in [
                        f"language={style.get('language')}" if style.get("language") else "",
                        f"tone={tone}" if tone else "",
                        f"verbosity={style.get('verbosity')}" if style.get("verbosity") else "",
                    ]
                    if part
                )
            )
    if workflow:
        workflow_bits = [
            f"autonomy={workflow.get('autonomy')}" if workflow.get("autonomy") else "",
            f"ask-vs-assume={workflow.get('ask_vs_assume')}" if workflow.get("ask_vs_assume") else "",
            f"planning={workflow.get('planning_style')}" if workflow.get("planning_style") else "",
            f"decision-style={workflow.get('decision_style')}" if workflow.get("decision_style") else "",
        ]
        workflow_bits = [item for item in workflow_bits if item]
        if workflow_bits:
            lines.append("Workflow: " + "; ".join(workflow_bits))
    if output:
        output_bits = [
            output.get("default_format", ""),
            output.get("summaries", ""),
            output.get("code_explanations", ""),
        ]
        output_bits = [item for item in output_bits if item]
        if output_bits:
            lines.append("Output: " + " | ".join(output_bits))
    if anti:
        lines.append("Avoid: " + "; ".join(str(item) for item in anti[:5]))
    if rules:
        lines.append("Decision rules: " + "; ".join(str(item) for item in rules[:5]))
    return "\n".join(lines)


def render_profile_markdown(profile: dict[str, Any]) -> str:
    meta = profile.get("meta", {})
    assistant_prompts = profile.setdefault("assistant_prompts", {})
    assistant_prompts["session_preamble"] = build_session_preamble(profile)

    lines = [
        "# User Preference Model",
        "",
        f"- Updated: {meta.get('updated_at', '')}",
        f"- Revision: {meta.get('revision', 0)}",
        "",
        "## Identity",
        key_values(profile.get("identity", {})),
        "",
        "## Interaction Style",
        key_values(profile.get("interaction_style", {})),
        "",
        "## Workflow",
        key_values(profile.get("workflow", {})),
        "",
        "## Output Preferences",
        key_values(profile.get("output_preferences", {})),
        "",
        "## Domain Preferences",
        key_values(profile.get("domain_preferences", {})),
        "",
        "## Anti-Preferences",
        bulletify(profile.get("anti_preferences", [])),
        "",
        "## Decision Rules",
        bulletify(profile.get("decision_rules", [])),
        "",
        "## Examples",
        bulletify(profile.get("examples", [])),
        "",
        "## Open Questions",
        bulletify(profile.get("open_questions", [])),
        "",
        "## Confidence Notes",
        bulletify(profile.get("confidence_notes", [])),
        "",
        "## Session Preamble",
        assistant_prompts["session_preamble"] or "- none",
        "",
        "## Custom Instructions Snippet",
        assistant_prompts.get("custom_instructions_snippet") or "- none",
        "",
    ]
    return "\n".join(lines)


def render_session_brief(profile: dict[str, Any]) -> str:
    meta = profile.get("meta", {})
    style = profile.get("interaction_style", {})
    workflow = profile.get("workflow", {})
    output = profile.get("output_preferences", {})

    lines = [
        "# Session Brief",
        "",
        "Apply these defaults unless the user overrides them in the current chat.",
        "",
        f"- Updated: {meta.get('updated_at', '')}",
    ]

    if style.get("language"):
        lines.append(f"- Language: {style.get('language')}")
    if style.get("tone"):
        lines.append(f"- Tone: {', '.join(style.get('tone', []))}")
    if style.get("verbosity"):
        lines.append(f"- Verbosity: {style.get('verbosity')}")
    if style.get("structure"):
        lines.append(f"- Structure: {', '.join(style.get('structure', []))}")
    if workflow.get("autonomy"):
        lines.append(f"- Autonomy: {workflow.get('autonomy')}")
    if workflow.get("ask_vs_assume"):
        lines.append(f"- Ask vs Assume: {workflow.get('ask_vs_assume')}")
    if workflow.get("planning_style"):
        lines.append(f"- Planning: {workflow.get('planning_style')}")
    if workflow.get("decision_style"):
        lines.append(f"- Decision Style: {workflow.get('decision_style')}")
    if output.get("default_format"):
        lines.append(f"- Default Format: {output.get('default_format')}")
    if output.get("summaries"):
        lines.append(f"- Summary Preference: {output.get('summaries')}")
    anti = profile.get("anti_preferences", [])
    if anti:
        lines.append(f"- Avoid: {'; '.join(str(item) for item in anti[:5])}")
    rules = profile.get("decision_rules", [])
    if rules:
        lines.append(f"- Rules: {'; '.join(str(item) for item in rules[:5])}")
    open_questions = profile.get("open_questions", [])
    if open_questions:
        lines.append(f"- Open Questions: {'; '.join(str(item) for item in open_questions[:3])}")
    return "\n".join(lines) + "\n"


def write_profile(profile: dict[str, Any]) -> None:
    PROFILE_JSON.write_text(compact_json(profile) + "\n", encoding="utf-8")
    PROFILE_MD.write_text(render_profile_markdown(profile), encoding="utf-8")
    SESSION_BRIEF.write_text(render_session_brief(profile), encoding="utf-8")


def append_log(path: Path, title: str, body: str) -> None:
    timestamp = now_iso()
    entry = f"## {timestamp} | {title}\n\n{body.strip()}\n\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def read_stdin_text() -> str:
    payload = sys.stdin.read().strip()
    if not payload:
        raise SystemExit("Expected content on stdin.")
    return payload


def command_ensure(_: argparse.Namespace) -> int:
    ensure_state()
    print(STATE_ROOT)
    return 0


def command_show(args: argparse.Namespace) -> int:
    profile = ensure_state()
    if args.format == "json":
        print(compact_json(profile))
        return 0
    if args.format == "markdown":
        print(PROFILE_MD.read_text(encoding="utf-8"), end="")
        return 0
    if args.format == "brief":
        print(SESSION_BRIEF.read_text(encoding="utf-8"), end="")
        return 0
    if args.format == "paths":
        print(
            compact_json(
                {
                    "state_root": str(STATE_ROOT),
                    "profile_json": str(PROFILE_JSON),
                    "profile_md": str(PROFILE_MD),
                    "session_brief": str(SESSION_BRIEF),
                    "interview_log": str(INTERVIEW_LOG),
                    "change_log": str(CHANGE_LOG),
                }
            )
        )
        return 0
    raise SystemExit(f"Unsupported format: {args.format}")


def command_merge(args: argparse.Namespace) -> int:
    before = ensure_state()
    patch = json.loads(read_stdin_text())
    if not isinstance(patch, dict):
        raise SystemExit("Expected a JSON object on stdin.")
    after = deep_merge(before, patch)
    if not isinstance(after, dict):
        raise SystemExit("Merged profile must be a JSON object.")

    changes = [item for item in collect_changes(before, after) if not item.startswith("meta.")]
    meta = after.setdefault("meta", {})
    meta["version"] = int(meta.get("version", 1) or 1)
    meta["created_at"] = before.get("meta", {}).get("created_at", now_iso())
    meta["updated_at"] = now_iso()
    meta["revision"] = int(before.get("meta", {}).get("revision", 0) or 0) + 1
    sources = list(before.get("meta", {}).get("sources", []))
    if args.source and args.source not in sources:
        sources.append(args.source)
    meta["sources"] = sources

    prompts = after.setdefault("assistant_prompts", {})
    provided_prompts = patch.get("assistant_prompts", {}) if isinstance(patch.get("assistant_prompts", {}), dict) else {}
    prompts["session_preamble"] = build_session_preamble(after)
    # Keep the reusable snippet aligned with the latest model unless the caller explicitly overrides it.
    prompts["custom_instructions_snippet"] = provided_prompts.get(
        "custom_instructions_snippet",
        prompts["session_preamble"],
    )

    write_profile(after)
    summary = {
        "updated_at": meta["updated_at"],
        "revision": meta["revision"],
        "source": args.source,
        "changed_keys": changes,
    }
    append_log(
        CHANGE_LOG,
        f"merge:{args.source}",
        "\n".join(
            [
                f"- note: {args.note or 'n/a'}",
                f"- changed_keys: {', '.join(changes) if changes else 'none'}",
                "",
                "```json",
                compact_json(patch),
                "```",
            ]
        ),
    )
    print(compact_json(summary))
    return 0


def command_log_interview(args: argparse.Namespace) -> int:
    ensure_state()
    append_log(INTERVIEW_LOG, args.title, read_stdin_text())
    print(INTERVIEW_LOG)
    return 0


def command_log_change(args: argparse.Namespace) -> int:
    ensure_state()
    append_log(CHANGE_LOG, args.title, read_stdin_text())
    print(CHANGE_LOG)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the preference-model-zh state files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ensure_parser = subparsers.add_parser("ensure", help="Create state files if they do not exist.")
    ensure_parser.set_defaults(func=command_ensure)

    show_parser = subparsers.add_parser("show", help="Show the stored preference model.")
    show_parser.add_argument(
        "--format",
        choices=["json", "markdown", "brief", "paths"],
        default="brief",
        help="Output format.",
    )
    show_parser.set_defaults(func=command_show)

    merge_parser = subparsers.add_parser("merge", help="Merge a JSON patch from stdin into the profile.")
    merge_parser.add_argument("--source", default="manual", help="Update source label.")
    merge_parser.add_argument("--note", default="", help="Optional note for the changelog.")
    merge_parser.set_defaults(func=command_merge)

    interview_parser = subparsers.add_parser("log-interview", help="Append a markdown note to the interview log.")
    interview_parser.add_argument("--title", required=True, help="Interview log entry title.")
    interview_parser.set_defaults(func=command_log_interview)

    change_parser = subparsers.add_parser("log-change", help="Append a markdown note to the change log.")
    change_parser.add_argument("--title", required=True, help="Change log entry title.")
    change_parser.set_defaults(func=command_log_change)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
