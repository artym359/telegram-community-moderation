# Telegram Community Moderation Bot

Public-safe rework of a Telegram moderation prototype. The bot watches configured group chats, detects profiles/messages that require review, queues candidates for an administrator and supports a review decision through inline buttons.

## What it demonstrates

- asynchronous Telegram bot architecture with `aiogram`;
- separate admin and scraper entry points;
- URL/profile heuristics and a review queue;
- SQLite persistence through SQLAlchemy async sessions;
- moderation actions isolated behind explicit administrator decisions.

## Safety boundary

This repository contains code only. It does not contain bot tokens, databases, user/chat exports, logs, browser sessions or production configuration. The bot can delete messages and ban users, so run it only in a test group where you have explicit administrator permission. Review the platform rules and privacy requirements before using any automated moderation rule.

The original local project name was intentionally replaced with this neutral name for public presentation. The public version also removes personal usernames and offensive copy from the application messages.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill `.env` with a test bot token and comma-separated usernames. The token must stay local and must never be committed. Run the two roles in separate terminals:

```powershell
python -m community_moderation.main_admin
python -m community_moderation.main_scraper
```

The SQLite database is created under `data/`, which is ignored by Git. Use a disposable test database while evaluating the project.

## Repository layout

```text
community_moderation/
  app/checker/       administrator review flow
  app/scraper/       group message/profile checks
  database/          SQLAlchemy models and requests
  main_admin.py      admin bot entry point
  main_scraper.py    scraper bot entry point
```

## Known limitations

The prototype uses a simple URL/profile heuristic and has no production-grade audit log, rate-limit strategy or policy engine. It is a portfolio demonstration of async integration and persistence, not a drop-in moderation service.

## License

MIT. See [LICENSE](LICENSE).
