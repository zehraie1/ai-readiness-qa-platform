"""Developer CLI.

python -m app.cli seed --profile dev|test
python -m app.cli reset-dev --yes        (development/test only: deletes attempts & results)
"""

import argparse
import sys

from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import SessionLocal, get_engine
from app.seed.bank_schema import load_bank
from app.seed.seeder import SeedRefused, seed_content
from app.seed.users import seed_users


def cmd_seed(profile: str) -> int:
    settings = get_settings()
    bank = load_bank()
    with SessionLocal(bind=get_engine()) as db, db.begin():
        seed_content(db, bank, settings.app_env)
        users = seed_users(db, profile, settings)
    print(
        f"Seeded bank '{bank.manifest.version_label}' "
        f"({bank.manifest.content_provenance}) and {len(users)} '{profile}' users."
    )
    return 0


def cmd_reset_dev(confirmed: bool) -> int:
    settings = get_settings()
    if settings.app_env not in ("development", "test"):
        print("reset-dev is only allowed when APP_ENV is development or test.", file=sys.stderr)
        return 2
    if not confirmed:
        print("Pass --yes to confirm deleting all attempts and results.", file=sys.stderr)
        return 2
    with get_engine().begin() as conn:
        conn.execute(
            text(
                "TRUNCATE result_recommendations, competency_scores, score_results, "
                "attempt_answers, attempt_questions, assessment_attempts"
            )
        )
    print("Deleted all attempts and results.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    p_seed = sub.add_parser("seed")
    p_seed.add_argument("--profile", choices=["dev", "test", "demo"], required=True)
    p_reset = sub.add_parser("reset-dev")
    p_reset.add_argument("--yes", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "seed":
            return cmd_seed(args.profile)
        return cmd_reset_dev(args.yes)
    except SeedRefused as exc:
        print(f"Seed refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
