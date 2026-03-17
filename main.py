"""main.py - Entry point for Project 38: Smart Recipe Recommender With Nutrition."""

from display import format_header, format_run_report, format_startup_guide
from models import create_recommender_config
from operations import load_recommender_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete recommendation session."""
    ensure_data_dirs()
    print(format_header())

    config = create_recommender_config()
    profile = load_recommender_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
