import json
from pathlib import Path
from typing import Dict

_translations_cache: Dict[str, Dict[str, str]] = {}

def load_translations(lang: str) -> Dict[str, str]:
    if lang in _translations_cache:
        return _translations_cache[lang]
    
    locales_dir = Path(__file__).parent / "locale"
    file_path = locales_dir / f"{lang}.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translations_cache[lang] = translations
            return translations
    except FileNotFoundError:
        return {}

def t(key: str, lang: str = "en") -> str:
    translations = load_translations(lang)
    return translations.get(key, key)