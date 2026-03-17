# Beginner Project 38: Smart Recipe Recommender With Nutrition

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Pantry-aware recipe ranking, nutrition-fit scoring, and persistent recommendation analytics

---

## Why This Project?

Home meal planning is often a tradeoff between what ingredients are already available and what nutrition targets should be met. This project demonstrates how to convert a static recipe collection into actionable meal recommendations using deterministic scoring and transparent rule-based evidence.

This project teaches end-to-end recommendation workflow concepts where you can:

- load or auto-generate a reusable local recipe library,
- evaluate pantry coverage per recipe and identify missing ingredients,
- compute nutrition-fit scores against calorie and macro targets,
- combine pantry match, nutrition fit, and cuisine variety into a weighted recommendation score,
- generate ranked recipe suggestions with explainable evidence strings,
- export recommendation payloads to JSON for downstream tooling,
- produce shopping list and weekly plan text artifacts,
- persist run summaries and per-recommendation metadata to JSON,
- track recent recommendations and historical run catalogs,
- and print a readable terminal report with preview rows and export paths.

---

## More Projects

You can access this project and more in this separate repository:

[student-interview-prep](https://github.com/ShamShamsw/student-interview-prep.git)

---

## What You Will Build

You will build a smart recipe recommender with nutrition analytics that:

1. Loads a recipe library from `data/library.json` (or seeds a starter set).
2. Uses a deterministic pantry profile and nutrition target profile for scoring.
3. Computes pantry coverage and missing-ingredient counts for each recipe.
4. Computes nutrition-fit scores from calorie, protein, carbs, and fat closeness.
5. Adds cuisine-variety adjustments to avoid one-category recommendation bias.
6. Produces weighted final scores and ranked recipe recommendations.
7. Exports ranked recommendations to JSON for downstream usage.
8. Exports recommendation payloads with score components and evidence.
9. Produces a plain-text shopping list from missing ingredients.
10. Produces a plain-text weekly meal plan from top-ranked recipes.
11. Persists per-recommendation metadata and run summaries for history and auditing.

---

## Requirements

- Python 3.11+
- No external dependencies - the recommendation engine uses stdlib only.

---

## Example Session

```text
======================================================================
   SMART RECIPE RECOMMENDER WITH NUTRITION
======================================================================

Configuration:
   Project type:         smart_recipe_recommender_with_nutrition
   Recommendation engine: pantry + nutrition + variety (stdlib only)
   Top recipes:          8
   Pantry weight:        0.55
   Nutrition weight:     0.35
   Variety weight:       0.1
   Max missing items:    3
   Include shopping list: True
   Include weekly plan:  True
   Max recs in report:   10
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Recipe library:       data/library.json (loaded 12 recipes)
   Run catalog:          data/runs.json (loaded 0 runs)
   Recommendation cat.:  data/recommendations.json (loaded 0 records)
   Recent recommendations: None yet

---

Run complete:
   Run ID:               20260317_191530
   Recipes loaded:       12
   Recipes evaluated:    10
   Recommendations:      8
   Unique cuisines:      7
   Elapsed time:         7.91 ms

Dataset metrics: mean_score=74.1 | mean_pantry_match=73.2% | mean_nutrition_fit=84.6% | avg_calories=534 | max_score=86.8

Recommendation previews:
   ID      | Recipe                       | Meal      | Score | Pantry | Nutrition | Missing
   --------+------------------------------+-----------+-------+--------+-----------+----------------
   rec_001 | Spinach Mushroom Omelet      | breakfast |  86.8 |   83%  |      88%  | 1
   rec_002 | Mediterranean Chickpea Bowl  | lunch     |  84.6 |   86%  |      83%  | 1
   rec_003 | Lentil Tomato Soup           | dinner    |  82.9 |   86%  |      80%  | 1

Artifacts saved:
   Run record:           data/outputs/run_20260317_191530.json
   Ranked export:        data/outputs/ranked_20260317_191530.json
   Recs export:          data/outputs/recommendations_20260317_191530.json
   Shopping list:        data/outputs/shopping_list_20260317_191530.txt
   Weekly plan:          data/outputs/weekly_plan_20260317_191530.txt
   Metadata exports:     8
```

---

## Run

```bash
python main.py
```
