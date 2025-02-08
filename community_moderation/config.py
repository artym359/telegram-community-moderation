"""Environment-backed configuration for the public demo."""

from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
except ImportError:  # Loading .env is optional when variables are set by the shell.
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()


def _csv_env(name: str) -> set[str]:
    return {
        value.strip().lstrip("@").lower()
        for value in os.getenv(name, "").split(",")
        if value.strip()
    }


TOKEN = os.getenv("MODERATION_BOT_TOKEN", "").strip()
PERMITTED_USERNAMES = _csv_env("MODERATION_ALLOWED_USERNAMES")
ADMIN_USERNAMES = _csv_env("MODERATION_ADMIN_USERNAMES")
DATABASE_URL = os.getenv(
    "MODERATION_DATABASE_URL",
    "sqlite+aiosqlite:///data/moderation.sqlite3",
).strip()
