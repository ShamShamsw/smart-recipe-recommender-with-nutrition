"""storage.py - Persistence layer for Project 38: Smart Recipe Recommender With Nutrition."""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
RUN_CATALOG_FILE = DATA_DIR / 'runs.json'
RECOMMENDATION_CATALOG_FILE = DATA_DIR / 'recommendations.json'
LIBRARY_FILE = DATA_DIR / 'library.json'


def ensure_data_dirs() -> None:
    """Create local data/output directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_data_dir() -> None:
    """Backwards-compatible alias for older scaffold code."""
    ensure_data_dirs()


def _load_list_file(path: Path) -> List[Dict[str, Any]]:
    """Safely load a list-based JSON file."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _save_list_file(path: Path, data: List[Dict[str, Any]]) -> None:
    """Persist list-based JSON with indentation."""
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')


def load_run_catalog() -> List[Dict[str, Any]]:
    """Load run catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(RUN_CATALOG_FILE)


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog to disk."""
    ensure_data_dirs()
    _save_list_file(RUN_CATALOG_FILE, catalog)


def load_recommendation_catalog() -> List[Dict[str, Any]]:
    """Load recommendation catalog entries from disk."""
    ensure_data_dirs()
    return _load_list_file(RECOMMENDATION_CATALOG_FILE)


def save_recommendation_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist recommendation catalog to disk."""
    ensure_data_dirs()
    _save_list_file(RECOMMENDATION_CATALOG_FILE, catalog)


def load_recipe_library() -> List[Dict[str, Any]]:
    """Load recipe library from disk."""
    ensure_data_dirs()
    return _load_list_file(LIBRARY_FILE)


def save_recipe_library(library: List[Dict[str, Any]]) -> str:
    """Persist recipe library to disk."""
    ensure_data_dirs()
    _save_list_file(LIBRARY_FILE, library)
    return str(LIBRARY_FILE)


def save_run_record(run_record: Dict[str, Any]) -> str:
    """Persist one run record and update run catalog."""
    ensure_data_dirs()
    run_id = run_record['run_id']
    file_path = OUTPUTS_DIR / f'run_{run_id}.json'
    file_path.write_text(json.dumps(run_record, indent=2), encoding='utf-8')

    catalog = load_run_catalog()
    catalog.append(
        {
            'run_id': run_id,
            'recipes_loaded': run_record.get('recipes_loaded', 0),
            'recipes_evaluated': run_record.get('recipes_evaluated', 0),
            'recommendations_generated': run_record.get('recommendations_generated', 0),
            'unique_cuisines': run_record.get('unique_cuisines', 0),
            'elapsed_ms': run_record.get('elapsed_ms', 0.0),
            'finished_at': run_record.get('finished_at', ''),
            'run_file': str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_recommendation_record(recommendation_record: Dict[str, Any], run_id: str) -> str:
    """Persist one recommendation record and update recommendation catalog."""
    ensure_data_dirs()
    recommendation_id = recommendation_record['recommendation_id']
    file_path = OUTPUTS_DIR / f'recommendation_{recommendation_id}_{run_id}.json'
    file_path.write_text(json.dumps(recommendation_record, indent=2), encoding='utf-8')

    catalog = load_recommendation_catalog()
    catalog.append(
        {
            'recommendation_id': recommendation_id,
            'run_id': run_id,
            'recipe_id': recommendation_record.get('recipe_id', ''),
            'recipe_name': recommendation_record.get('recipe_name', ''),
            'score': recommendation_record.get('score', 0.0),
            'cuisine': recommendation_record.get('cuisine', ''),
            'meal_type': recommendation_record.get('meal_type', ''),
            'metadata_file': str(file_path),
        }
    )
    save_recommendation_catalog(catalog)
    return str(file_path)


def load_json(filename: str):
    """Load JSON data from the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []


def save_json(filename: str, data) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
