"""models.py - Data models for Project 38: Smart Recipe Recommender With Nutrition."""

from datetime import datetime
from typing import Any, Dict, List


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec='seconds') + 'Z'


def create_recommender_config(
    top_recipes: int = 8,
    pantry_weight: float = 0.55,
    nutrition_weight: float = 0.35,
    variety_weight: float = 0.10,
    max_missing_ingredients: int = 3,
    include_shopping_list: bool = True,
    include_weekly_plan: bool = True,
    max_recommendations_in_report: int = 10,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated recommender configuration record."""
    pantry_weight = max(0.0, float(pantry_weight))
    nutrition_weight = max(0.0, float(nutrition_weight))
    variety_weight = max(0.0, float(variety_weight))
    total_weight = pantry_weight + nutrition_weight + variety_weight or 1.0
    return {
        'project_type': 'smart_recipe_recommender_with_nutrition',
        'top_recipes': max(3, int(top_recipes)),
        'pantry_weight': round(pantry_weight / total_weight, 4),
        'nutrition_weight': round(nutrition_weight / total_weight, 4),
        'variety_weight': round(variety_weight / total_weight, 4),
        'max_missing_ingredients': max(0, int(max_missing_ingredients)),
        'include_shopping_list': bool(include_shopping_list),
        'include_weekly_plan': bool(include_weekly_plan),
        'max_recommendations_in_report': max(3, int(max_recommendations_in_report)),
        'random_seed': int(random_seed),
        'created_at': _utc_timestamp(),
    }


def create_recommendation_record(
    recommendation_id: str,
    recipe_id: str,
    recipe_name: str,
    cuisine: str,
    meal_type: str,
    score: float,
    pantry_match: float,
    nutrition_fit: float,
    variety_fit: float,
    calories: int,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    missing_ingredients: List[str],
    suggested_swaps: List[str],
    evidence: List[str],
) -> Dict[str, Any]:
    """Create one computed recommendation record."""
    return {
        'recommendation_id': recommendation_id,
        'recipe_id': recipe_id,
        'recipe_name': recipe_name,
        'cuisine': cuisine,
        'meal_type': meal_type,
        'score': round(float(score), 4),
        'pantry_match': round(float(pantry_match), 4),
        'nutrition_fit': round(float(nutrition_fit), 4),
        'variety_fit': round(float(variety_fit), 4),
        'calories': int(calories),
        'protein_g': round(float(protein_g), 2),
        'carbs_g': round(float(carbs_g), 2),
        'fat_g': round(float(fat_g), 2),
        'missing_ingredients': list(missing_ingredients),
        'suggested_swaps': list(suggested_swaps),
        'evidence': list(evidence),
        'created_at': _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    recipes_loaded: int,
    recipes_evaluated: int,
    recommendations_generated: int,
    unique_cuisines: int,
    elapsed_ms: float,
    artifacts: Dict[str, Any],
    recommendation_previews: List[Dict[str, Any]],
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Create final run summary for reporting and persistence."""
    return {
        'run_id': run_id,
        'recipes_loaded': int(recipes_loaded),
        'recipes_evaluated': int(recipes_evaluated),
        'recommendations_generated': int(recommendations_generated),
        'unique_cuisines': int(unique_cuisines),
        'elapsed_ms': float(elapsed_ms),
        'artifacts': artifacts,
        'recommendation_previews': recommendation_previews,
        'metrics': metrics,
        'finished_at': _utc_timestamp(),
    }


def create_record(**kwargs):
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
