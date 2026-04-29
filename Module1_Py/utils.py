from typing import Dict, Tuple

from colorama import Fore, init

init(autoreset=True)


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}".replace(".", ",")


def convert_and_compare_speeds(v1_kmh: float, v2_ms: float) -> Tuple[float, float, str]:
    v1_ms = v1_kmh * 1000 / 3600
    v2_kmh = v2_ms * 3600 / 1000

    if abs(v1_ms - v2_ms) < 1e-9:
        comparison = "equal"
    elif v1_ms < v2_ms:
        comparison = "less"
    else:
        comparison = "greater"

    return v1_ms, v2_kmh, comparison


def apply_color(text: str, color: str) -> str:
    return f"{color}{text}{Fore.RESET}"


def translate(key: str, lang: str = "uk") -> str:
    translations: Dict[str, Dict[str, str]] = {
        "uk": {
            "lang_name": "Українська",
            "lang_label": "Мова: ",
            "v1_label": "Швидкість v1 (км/год): ",
            "v2_label": "Швидкість v2 (м/с): ",
            "conv_1": "Швидкість {} км/год = {} м/с",
            "conv_2": "Швидкість {} м/с = {} км/год",
            "less": "Швидкість v1={} менша ніж швидкість v2={}",
            "greater": "Швидкість v1={} більша ніж швидкість v2={}",
            "equal": "Швидкість v1={} дорівнює швидкості v2={}",
            "unit_kmh": "км/год",
            "unit_ms": "м/с",
        },
        "en": {
            "lang_name": "English",
            "lang_label": "Language: ",
            "v1_label": "Speed v1 (km/h): ",
            "v2_label": "Speed v2 (m/s): ",
            "conv_1": "Speed {} km/h = {} m/s",
            "conv_2": "Speed {} m/s = {} km/h",
            "less": "Speed v1={} is less than speed v2={}",
            "greater": "Speed v1={} is greater than speed v2={}",
            "equal": "Speed v1={} is equal to speed v2={}",
            "unit_kmh": "km/h",
            "unit_ms": "m/s",
        },
    }

    if lang not in translations:
        lang = "uk"

    return translations[lang].get(key, translations["uk"].get(key, key))
