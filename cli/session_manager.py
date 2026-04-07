"""Research session management — isolates context across research topics.

Each session gets a globally unique ID: {date}-{slug}-{uuid8}.
Context files live in context/sessions/{session_id}/.

Concurrent-safe: every tool call receives an explicit session_id,
no shared mutable state (symlink kept only as convenience for CLI).

Usage:
    session_manager.py new "agent harness 2026"
    session_manager.py list
    session_manager.py switch <session-id>
    session_manager.py current
    session_manager.py context-path <session-id>
"""
from __future__ import annotations

import json
import re
import sys
import uuid
from datetime import date
from pathlib import Path

CONTEXT_DIR = Path(__file__).parent.parent / "context"
SESSIONS_DIR = CONTEXT_DIR / "sessions"
CURRENT_LINK = CONTEXT_DIR / "current"


def _slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:50]


def _make_session_id(topic: str) -> str:
    """Generate a globally unique session ID: {date}-{slug}-{uuid8}."""
    today = date.today().isoformat()
    slug = _slugify(topic)
    uid = uuid.uuid4().hex[:8]
    parts = [today]
    if slug:
        parts.append(slug)
    parts.append(uid)
    return "-".join(parts)


def _ensure_sessions_dir() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def _update_symlink(session_id: str) -> None:
    """Update the convenience symlink (non-critical, best-effort)."""
    if CURRENT_LINK.is_symlink() or CURRENT_LINK.exists():
        CURRENT_LINK.unlink()
    CURRENT_LINK.symlink_to(f"sessions/{session_id}")


def get_context_path(session_id: str) -> Path:
    """Return the absolute context directory for a session ID.

    This is the ONLY function tools should use to resolve where to
    read/write context files. It does NOT touch the symlink.
    Concurrent-safe: purely derives path from session_id string.
    """
    _ensure_sessions_dir()
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def new_session(topic: str) -> dict[str, str]:
    """Create a new research session with a globally unique ID.

    Returns dict with session_id, session_path, topic, and previous_session.
    Also updates the convenience symlink.
    """
    _ensure_sessions_dir()

    session_id = _make_session_id(topic)
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Record previous session before switching symlink
    previous = ""
    if CURRENT_LINK.is_symlink():
        previous = CURRENT_LINK.resolve().name

    _update_symlink(session_id)

    return {
        "session_id": session_id,
        "session_path": str(session_dir),
        "topic": topic,
        "previous_session": previous,
    }


def list_sessions() -> list[dict[str, object]]:
    """List all sessions with their status."""
    _ensure_sessions_dir()

    current_name = ""
    if CURRENT_LINK.is_symlink():
        current_name = CURRENT_LINK.resolve().name

    sessions: list[dict[str, object]] = []
    for d in sorted(SESSIONS_DIR.iterdir()):
        if d.is_dir():
            files = [f.name for f in d.iterdir() if f.is_file()]
            sessions.append({
                "session_id": d.name,
                "active": d.name == current_name,
                "files": files,
            })
    return sessions


def switch_session(session_id: str) -> dict[str, str]:
    """Switch the convenience symlink to an existing session."""
    _ensure_sessions_dir()

    target = SESSIONS_DIR / session_id
    if not target.is_dir():
        return {"error": f"Session not found: {session_id}"}

    _update_symlink(session_id)

    return {
        "session_id": session_id,
        "session_path": str(target),
    }


def get_current_session() -> dict[str, object]:
    """Get the session currently pointed to by the convenience symlink."""
    if not CURRENT_LINK.is_symlink():
        return {"error": "No active session. Use 'new' to create one."}

    resolved = CURRENT_LINK.resolve()
    if not resolved.is_dir():
        return {"error": f"Current symlink points to missing directory: {resolved}"}

    files = [f.name for f in resolved.iterdir() if f.is_file()]
    return {
        "session_id": resolved.name,
        "session_path": str(resolved),
        "files": files,
    }


def migrate_legacy_context() -> dict[str, object]:
    """Migrate flat context/ files into a legacy session."""
    _ensure_sessions_dir()

    legacy_files = [
        f for f in CONTEXT_DIR.iterdir()
        if f.is_file() and f.suffix in (".md", ".jsonl", ".json") and f.name != ".gitkeep"
    ]

    if not legacy_files:
        return {"migrated": 0, "message": "No legacy files to migrate."}

    legacy_id = "legacy-migration"
    legacy_dir = SESSIONS_DIR / legacy_id
    legacy_dir.mkdir(parents=True, exist_ok=True)

    migrated = []
    for f in legacy_files:
        dest = legacy_dir / f.name
        f.rename(dest)
        migrated.append(f.name)

    _update_symlink(legacy_id)

    return {
        "migrated": len(migrated),
        "files": migrated,
        "session_id": legacy_id,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Manage research sessions")
    sub = parser.add_subparsers(dest="command")

    new_p = sub.add_parser("new", help="Create a new session")
    new_p.add_argument("topic", help="Research topic name")

    sub.add_parser("list", help="List all sessions")

    switch_p = sub.add_parser("switch", help="Switch to an existing session")
    switch_p.add_argument("session_id", help="Session ID")

    sub.add_parser("current", help="Show current session")

    ctx_p = sub.add_parser("context-path", help="Get context dir for a session")
    ctx_p.add_argument("session_id", help="Session ID")

    sub.add_parser("migrate", help="Migrate legacy flat context files")

    args = parser.parse_args()

    if args.command == "new":
        result = new_session(args.topic)
    elif args.command == "list":
        result = list_sessions()
    elif args.command == "switch":
        result = switch_session(args.session_id)
    elif args.command == "current":
        result = get_current_session()
    elif args.command == "context-path":
        path = get_context_path(args.session_id)
        result = {"session_id": args.session_id, "context_path": str(path)}
    elif args.command == "migrate":
        result = migrate_legacy_context()
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
