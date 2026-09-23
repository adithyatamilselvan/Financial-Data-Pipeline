from src.pipeline import run
from src.logging_utils import configure_logging
from config.settings import settings
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the synthetic financial transaction pipeline")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run through validation without MySQL")
    parser.add_argument("--no-generate", action="store_true",
                        help="Use existing raw source files")
    args = parser.parse_args()
    logger = configure_logging(settings.log_file)
    try:
        summary = run(dry_run=args.dry_run,
                      generate=not args.no_generate, logger=logger)
    except Exception as error:
        logger.exception("Pipeline failed: %s", error)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
