"""operations.py - Business logic for Project 38: Smart Recipe Recommender With Nutrition."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics
import time
from typing import Any, Dict, List, Tuple

from models import create_recommender_config, create_recommendation_record, create_run_summary
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_recipe_library,
    load_recommendation_catalog,
    load_run_catalog,
    save_recommendation_record,
    save_recipe_library,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S')


def _default_library() -> List[Dict[str, Any]]:
    """Return deterministic starter recipe library used on first run."""
    return [
        {
            'recipe_id': 'rcp_001',
            'name': 'Mediterranean Chickpea Bowl',
            'cuisine': 'Mediterranean',
            'meal_type': 'lunch',
            'ingredients': ['chickpeas', 'cucumber', 'tomato', 'olive oil', 'lemon', 'feta', 'spinach'],
            'prep_minutes': 15,
            'nutrition': {'calories': 520, 'protein_g': 22, 'carbs_g': 54, 'fat_g': 24, 'fiber_g': 13},
        },
        {
            'recipe_id': 'rcp_002',
            'name': 'High Protein Egg Fried Rice',
            'cuisine': 'Asian Fusion',
            'meal_type': 'dinner',
            'ingredients': ['brown rice', 'eggs', 'peas', 'carrot', 'soy sauce', 'sesame oil', 'green onion'],
            'prep_minutes': 20,
            'nutrition': {'calories': 590, 'protein_g': 28, 'carbs_g': 63, 'fat_g': 21, 'fiber_g': 9},
        },
        {
            'recipe_id': 'rcp_003',
            'name': 'Greek Yogurt Berry Parfait',
            'cuisine': 'American',
            'meal_type': 'breakfast',
            'ingredients': ['greek yogurt', 'berries', 'oats', 'chia seeds', 'honey', 'almonds'],
            'prep_minutes': 10,
            'nutrition': {'calories': 430, 'protein_g': 30, 'carbs_g': 42, 'fat_g': 14, 'fiber_g': 10},
        },
        {
            'recipe_id': 'rcp_004',
            'name': 'Turkey Avocado Wrap',
            'cuisine': 'American',
            'meal_type': 'lunch',
            'ingredients': ['whole wheat tortilla', 'turkey breast', 'avocado', 'lettuce', 'tomato', 'mustard'],
            'prep_minutes': 12,
            'nutrition': {'calories': 510, 'protein_g': 35, 'carbs_g': 38, 'fat_g': 23, 'fiber_g': 8},
        },
        {
            'recipe_id': 'rcp_005',
            'name': 'Lentil Tomato Soup',
            'cuisine': 'Comfort',
            'meal_type': 'dinner',
            'ingredients': ['lentils', 'tomato', 'onion', 'garlic', 'carrot', 'celery', 'vegetable broth'],
            'prep_minutes': 35,
            'nutrition': {'calories': 460, 'protein_g': 24, 'carbs_g': 66, 'fat_g': 8, 'fiber_g': 18},
        },
        {
            'recipe_id': 'rcp_006',
            'name': 'Salmon Quinoa Plate',
            'cuisine': 'Nordic',
            'meal_type': 'dinner',
            'ingredients': ['salmon', 'quinoa', 'broccoli', 'olive oil', 'lemon', 'garlic'],
            'prep_minutes': 30,
            'nutrition': {'calories': 640, 'protein_g': 42, 'carbs_g': 45, 'fat_g': 30, 'fiber_g': 8},
        },
        {
            'recipe_id': 'rcp_007',
            'name': 'Tofu Veggie Stir Fry',
            'cuisine': 'Asian Fusion',
            'meal_type': 'dinner',
            'ingredients': ['tofu', 'broccoli', 'bell pepper', 'soy sauce', 'ginger', 'garlic', 'brown rice'],
            'prep_minutes': 25,
            'nutrition': {'calories': 560, 'protein_g': 29, 'carbs_g': 58, 'fat_g': 20, 'fiber_g': 11},
        },
        {
            'recipe_id': 'rcp_008',
            'name': 'Overnight Oats Protein Jar',
            'cuisine': 'American',
            'meal_type': 'breakfast',
            'ingredients': ['oats', 'milk', 'greek yogurt', 'banana', 'chia seeds', 'peanut butter'],
            'prep_minutes': 8,
            'nutrition': {'calories': 520, 'protein_g': 27, 'carbs_g': 55, 'fat_g': 20, 'fiber_g': 10},
        },
        {
            'recipe_id': 'rcp_009',
            'name': 'Bean Burrito Bowl',
            'cuisine': 'Mexican',
            'meal_type': 'lunch',
            'ingredients': ['black beans', 'brown rice', 'corn', 'tomato', 'avocado', 'lime', 'cilantro'],
            'prep_minutes': 18,
            'nutrition': {'calories': 610, 'protein_g': 20, 'carbs_g': 85, 'fat_g': 21, 'fiber_g': 17},
        },
        {
            'recipe_id': 'rcp_010',
            'name': 'Spinach Mushroom Omelet',
            'cuisine': 'French Inspired',
            'meal_type': 'breakfast',
            'ingredients': ['eggs', 'spinach', 'mushroom', 'olive oil', 'onion', 'feta'],
            'prep_minutes': 14,
            'nutrition': {'calories': 410, 'protein_g': 31, 'carbs_g': 11, 'fat_g': 27, 'fiber_g': 4},
        },
        {
            'recipe_id': 'rcp_011',
            'name': 'Chicken Sweet Potato Skillet',
            'cuisine': 'American',
            'meal_type': 'dinner',
            'ingredients': ['chicken breast', 'sweet potato', 'spinach', 'garlic', 'paprika', 'olive oil'],
            'prep_minutes': 28,
            'nutrition': {'calories': 590, 'protein_g': 44, 'carbs_g': 48, 'fat_g': 22, 'fiber_g': 7},
        },
        {
            'recipe_id': 'rcp_012',
            'name': 'Pesto Pasta With Peas',
            'cuisine': 'Italian',
            'meal_type': 'lunch',
            'ingredients': ['whole wheat pasta', 'peas', 'basil pesto', 'parmesan', 'garlic', 'olive oil'],
            'prep_minutes': 22,
            'nutrition': {'calories': 630, 'protein_g': 22, 'carbs_g': 77, 'fat_g': 26, 'fiber_g': 9},
        },
    ]


def _default_user_targets() -> Dict[str, Any]:
    """Return deterministic pantry and nutrition goals for this demo run."""
    return {
        'pantry': {
            'eggs',
            'spinach',
            'tomato',
            'olive oil',
            'garlic',
            'onion',
            'brown rice',
            'chickpeas',
            'greek yogurt',
            'berries',
            'oats',
            'chia seeds',
            'broccoli',
            'tofu',
            'lentils',
            'avocado',
            'lemon',
            'black beans',
            'corn',
        },
        'goals': {
            'target_calories': 550,
            'target_protein_g': 30,
            'target_carbs_g': 55,
            'target_fat_g': 20,
        },
    }


def _normalized_closeness(value: float, target: float) -> float:
    """Return normalized closeness score between 0 and 1 for one nutrition metric."""
    if target <= 0:
        return 0.0
    return max(0.0, 1.0 - abs(value - target) / target)


def _compute_recipe_fits(
    recipe: Dict[str, Any],
    pantry_items: set[str],
    goals: Dict[str, float],
    cuisine_counts: Counter[str],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """Compute fit metrics and weighted final score for one recipe."""
    ingredients = [str(item).strip().lower() for item in recipe.get('ingredients', []) if str(item).strip()]
    pantry = {item.strip().lower() for item in pantry_items if str(item).strip()}
    nutrition = recipe.get('nutrition', {})

    if not ingredients:
        pantry_match = 0.0
        missing_ingredients: List[str] = []
    else:
        missing_ingredients = sorted(item for item in ingredients if item not in pantry)
        pantry_match = (len(ingredients) - len(missing_ingredients)) / len(ingredients)

    calories = float(nutrition.get('calories', 0.0))
    protein_g = float(nutrition.get('protein_g', 0.0))
    carbs_g = float(nutrition.get('carbs_g', 0.0))
    fat_g = float(nutrition.get('fat_g', 0.0))
    fiber_g = float(nutrition.get('fiber_g', 0.0))

    nutrition_fit = statistics.mean(
        [
            _normalized_closeness(calories, float(goals['target_calories'])),
            _normalized_closeness(protein_g, float(goals['target_protein_g'])),
            _normalized_closeness(carbs_g, float(goals['target_carbs_g'])),
            _normalized_closeness(fat_g, float(goals['target_fat_g'])),
        ]
    )

    cuisine = str(recipe.get('cuisine', 'unknown'))
    variety_fit = 1.0 / (1.0 + cuisine_counts[cuisine])

    score = (
        100.0
        * (
            config['pantry_weight'] * pantry_match
            + config['nutrition_weight'] * nutrition_fit
            + config['variety_weight'] * variety_fit
        )
    )

    suggested_swaps: List[str] = []
    if missing_ingredients:
        for item in missing_ingredients[:2]:
            suggested_swaps.append(f'consider substitute for {item}')
    if protein_g < float(goals['target_protein_g']) - 6:
        suggested_swaps.append('add lean protein side to improve protein balance')
    if fiber_g < 8:
        suggested_swaps.append('add leafy greens or legumes for better fiber')

    evidence = [
        f'pantry coverage {pantry_match:.0%} ({len(ingredients) - len(missing_ingredients)}/{len(ingredients)} ingredients)',
        (
            'nutrition fit '
            f"{nutrition_fit:.0%} (kcal={int(calories)}, protein={int(protein_g)}g, carbs={int(carbs_g)}g, fat={int(fat_g)}g)"
        ),
        f'cuisine variety boost {variety_fit:.2f}',
    ]

    return {
        'score': score,
        'pantry_match': pantry_match,
        'nutrition_fit': nutrition_fit,
        'variety_fit': variety_fit,
        'missing_ingredients': missing_ingredients,
        'suggested_swaps': suggested_swaps,
        'evidence': evidence,
        'calories': int(calories),
        'protein_g': protein_g,
        'carbs_g': carbs_g,
        'fat_g': fat_g,
        'fiber_g': fiber_g,
    }


def _build_weekly_plan(recommendations: List[Dict[str, Any]]) -> str:
    """Create a simple seven-day meal suggestion plan from ranked recommendations."""
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if not recommendations:
        return 'No recommendations available for weekly plan.'

    lines = ['SMART RECIPE WEEKLY PLAN', '========================', '']
    for index, day in enumerate(day_names):
        pick = recommendations[index % len(recommendations)]
        lines.append(
            f"- {day}: {pick['recipe_name']} [{pick['meal_type']}] "
            f"score={pick['score']:.1f} pantry={pick['pantry_match']:.0%}"
        )
    return '\n'.join(lines)


def _build_shopping_list(recommendations: List[Dict[str, Any]]) -> List[str]:
    """Create deduplicated shopping list from missing ingredients."""
    items = {
        item
        for recommendation in recommendations
        for item in recommendation.get('missing_ingredients', [])
    }
    return sorted(items)


def load_recommender_profile() -> Dict[str, Any]:
    """Return startup profile built from previously saved catalogs."""
    runs = load_run_catalog()
    recommendations = load_recommendation_catalog()
    library = load_recipe_library()
    recent_recommendations = [
        f"{item.get('recommendation_id', '')}:{item.get('recipe_name', '')}:{item.get('score', 0.0):.1f}"
        for item in recommendations[-8:]
    ]
    return {
        'catalog_file': 'data/runs.json',
        'recommendation_catalog_file': 'data/recommendations.json',
        'library_file': 'data/library.json',
        'runs_stored': len(runs),
        'recommendation_records_stored': len(recommendations),
        'library_available': len(library),
        'recent_recommendations': recent_recommendations,
    }


def run_core_flow() -> Dict[str, Any]:
    """Run one complete recommendation session."""
    ensure_data_dirs()
    config = create_recommender_config()
    run_id = _run_id()
    started = time.perf_counter()

    library = load_recipe_library()
    if not library:
        library = _default_library()
        save_recipe_library(library)

    user_targets = _default_user_targets()
    pantry_items = user_targets['pantry']
    goals = user_targets['goals']

    cuisine_counts = Counter(str(recipe.get('cuisine', 'unknown')) for recipe in library)
    evaluations: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []

    for recipe in library:
        computed = _compute_recipe_fits(
            recipe=recipe,
            pantry_items=pantry_items,
            goals=goals,
            cuisine_counts=cuisine_counts,
            config=config,
        )
        if len(computed['missing_ingredients']) > config['max_missing_ingredients']:
            continue
        evaluations.append((recipe, computed))

    evaluations.sort(
        key=lambda item: (
            -item[1]['score'],
            len(item[1]['missing_ingredients']),
            int(item[0].get('prep_minutes', 999)),
        )
    )
    selected = evaluations[: config['top_recipes']]

    recommendation_records: List[Dict[str, Any]] = []
    metadata_files: List[str] = []
    for index, (recipe, computed) in enumerate(selected, start=1):
        recommendation_id = f'rec_{index:03d}'
        record = create_recommendation_record(
            recommendation_id=recommendation_id,
            recipe_id=str(recipe.get('recipe_id', 'unknown')),
            recipe_name=str(recipe.get('name', 'Unnamed Recipe')),
            cuisine=str(recipe.get('cuisine', 'unknown')),
            meal_type=str(recipe.get('meal_type', 'unknown')),
            score=computed['score'],
            pantry_match=computed['pantry_match'],
            nutrition_fit=computed['nutrition_fit'],
            variety_fit=computed['variety_fit'],
            calories=computed['calories'],
            protein_g=computed['protein_g'],
            carbs_g=computed['carbs_g'],
            fat_g=computed['fat_g'],
            missing_ingredients=computed['missing_ingredients'],
            suggested_swaps=computed['suggested_swaps'],
            evidence=computed['evidence'],
        )
        recommendation_records.append(record)
        metadata_files.append(save_recommendation_record(record, run_id))

    ranked_file = OUTPUTS_DIR / f'ranked_{run_id}.json'
    ranked_file.write_text(json.dumps(recommendation_records, indent=2), encoding='utf-8')

    recommendations_file = OUTPUTS_DIR / f'recommendations_{run_id}.json'
    recommendations_file.write_text(
        json.dumps(
            {
                'run_id': run_id,
                'pantry_size': len(pantry_items),
                'nutrition_goals': goals,
                'recommendations': recommendation_records,
            },
            indent=2,
        ),
        encoding='utf-8',
    )

    shopping_items = _build_shopping_list(recommendation_records)
    shopping_file = OUTPUTS_DIR / f'shopping_list_{run_id}.txt'
    shopping_file.write_text(
        'SHOPPING LIST\n=============\n\n'
        + ('\n'.join(f'- {item}' for item in shopping_items) if shopping_items else 'No missing ingredients.'),
        encoding='utf-8',
    )

    weekly_plan_file = OUTPUTS_DIR / f'weekly_plan_{run_id}.txt'
    weekly_plan_file.write_text(_build_weekly_plan(recommendation_records), encoding='utf-8')

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    scores = [item['score'] for item in recommendation_records]
    pantry_matches = [item['pantry_match'] for item in recommendation_records]
    nutrition_fits = [item['nutrition_fit'] for item in recommendation_records]
    meal_type_counts = Counter(item['meal_type'] for item in recommendation_records)

    metrics: Dict[str, Any] = {
        'mean_score': round(statistics.mean(scores), 4) if scores else 0.0,
        'max_score': round(max(scores), 4) if scores else 0.0,
        'mean_pantry_match': round(statistics.mean(pantry_matches), 4) if pantry_matches else 0.0,
        'mean_nutrition_fit': round(statistics.mean(nutrition_fits), 4) if nutrition_fits else 0.0,
        'avg_calories': round(
            statistics.mean(item['calories'] for item in recommendation_records), 2
        )
        if recommendation_records
        else 0.0,
        'breakfast_share': round(meal_type_counts.get('breakfast', 0) / len(recommendation_records), 4)
        if recommendation_records
        else 0.0,
    }

    artifacts: Dict[str, Any] = {
        'run_file': str(OUTPUTS_DIR / f'run_{run_id}.json'),
        'ranked_file': str(ranked_file),
        'recommendations_file': str(recommendations_file),
        'shopping_file': str(shopping_file),
        'weekly_plan_file': str(weekly_plan_file),
        'metadata_files': metadata_files,
    }

    summary = create_run_summary(
        run_id=run_id,
        recipes_loaded=len(library),
        recipes_evaluated=len(evaluations),
        recommendations_generated=len(recommendation_records),
        unique_cuisines=len(set(item.get('cuisine', 'unknown') for item in library)),
        elapsed_ms=elapsed_ms,
        artifacts=artifacts,
        recommendation_previews=recommendation_records[: config['max_recommendations_in_report']],
        metrics=metrics,
    )

    save_run_record(summary)
    return summary
