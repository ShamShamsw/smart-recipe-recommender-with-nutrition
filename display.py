"""display.py - Presentation helpers for Project 38: Smart Recipe Recommender With Nutrition."""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return '=' * 70 + '\n' + '   SMART RECIPE RECOMMENDER WITH NUTRITION\n' + '=' * 70


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and historical profile."""
    recent = ', '.join(profile.get('recent_recommendations', [])) or 'None yet'
    lines = [
        '',
        'Configuration:',
        f"   Project type:         {config['project_type']}",
        '   Recommendation engine: pantry + nutrition + variety (stdlib only)',
        f"   Top recipes:          {config['top_recipes']}",
        f"   Pantry weight:        {config['pantry_weight']}",
        f"   Nutrition weight:     {config['nutrition_weight']}",
        f"   Variety weight:       {config['variety_weight']}",
        f"   Max missing items:    {config['max_missing_ingredients']}",
        f"   Include shopping list: {config['include_shopping_list']}",
        f"   Include weekly plan:  {config['include_weekly_plan']}",
        f"   Max recs in report:   {config['max_recommendations_in_report']}",
        f"   Random seed:          {config['random_seed']}",
        '',
        'Startup:',
        '   Data directory:       data/',
        '   Outputs directory:    data/outputs/',
        (
            f"   Recipe library:       {profile['library_file']} "
            f"(loaded {profile['library_available']} recipes)"
        ),
        (
            f"   Run catalog:          {profile['catalog_file']} "
            f"(loaded {profile['runs_stored']} runs)"
        ),
        (
            f"   Recommendation cat.:  {profile['recommendation_catalog_file']} "
            f"(loaded {profile['recommendation_records_stored']} records)"
        ),
        f"   Recent recommendations: {recent}",
        '',
        '---',
    ]
    return '\n'.join(lines)


def format_recommendation_table(previews: List[Dict[str, Any]]) -> str:
    """Format recommendation preview table."""
    if not previews:
        return 'No recommendations generated.'
    lines = [
        'Recommendation previews:',
        '   ID      | Recipe                       | Meal      | Score | Pantry | Nutrition | Missing',
        '   --------+------------------------------+-----------+-------+--------+-----------+----------------',
    ]
    for recommendation in previews:
        missing_count = len(recommendation.get('missing_ingredients', []))
        lines.append(
            '   '
            f"{recommendation['recommendation_id'][:7]:<7} | "
            f"{recommendation.get('recipe_name', '')[:28]:<28} | "
            f"{recommendation.get('meal_type', '')[:9]:<9} | "
            f"{recommendation.get('score', 0.0):>5.1f} | "
            f"{recommendation.get('pantry_match', 0.0):>6.0%} | "
            f"{recommendation.get('nutrition_fit', 0.0):>9.0%} | "
            f"{missing_count}"
        )
    return '\n'.join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    artifacts = summary.get('artifacts', {})
    metrics = summary.get('metrics', {})
    metadata_files = artifacts.get('metadata_files', [])
    lines = [
        '',
        'Run complete:',
        f"   Run ID:               {summary['run_id']}",
        f"   Recipes loaded:       {summary['recipes_loaded']}",
        f"   Recipes evaluated:    {summary['recipes_evaluated']}",
        f"   Recommendations:      {summary['recommendations_generated']}",
        f"   Unique cuisines:      {summary['unique_cuisines']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        '',
        (
            f"Dataset metrics: mean_score={metrics.get('mean_score', 0.0):.1f} | "
            f"mean_pantry_match={metrics.get('mean_pantry_match', 0.0):.1%} | "
            f"mean_nutrition_fit={metrics.get('mean_nutrition_fit', 0.0):.1%} | "
            f"avg_calories={metrics.get('avg_calories', 0.0):.0f} | "
            f"max_score={metrics.get('max_score', 0.0):.1f}"
        ),
        '',
        format_recommendation_table(summary.get('recommendation_previews', [])),
        '',
        'Artifacts saved:',
        f"   Run record:           {artifacts.get('run_file', 'N/A')}",
        f"   Ranked export:        {artifacts.get('ranked_file', 'N/A')}",
        f"   Recs export:          {artifacts.get('recommendations_file', 'N/A')}",
        f"   Shopping list:        {artifacts.get('shopping_file', 'N/A')}",
        f"   Weekly plan:          {artifacts.get('weekly_plan_file', 'N/A')}",
        f"   Metadata exports:     {len(metadata_files)}",
    ]
    return '\n'.join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 38] {message}'
