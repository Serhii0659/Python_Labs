import json
import sys
from typing import Any, TypedDict

from colorama import Fore

from utils import (apply_color, convert_and_compare_speeds, format_number,
                   translate)

DATA_FILE = "MyData.json"

# Тип даних для збереження в файлі для відповідності strict type checking
class AppData(TypedDict):
    v1: float
    v2: float
    lang: str

def read_data() -> AppData:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)

        v1 = float(data["v1"])
        v2 = float(data["v2"])
        lang = str(data.get("lang", "uk")).strip().lower()

        return {"v1": v1, "v2": v2, "lang": lang}
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        raise ValueError(f"Помилка або відсутні дані: {e}")


def prompt_and_save_data() -> None:
    print("Програма намагається прочитати дані із файлу MyData...")
    print("Виявлено відсутність файлу або некоректні дані.")
    try:
        v1_input = input("Введіть швидкість v1 (км/год): ")
        v2_input = input("Введіть швидкість v2 (м/с): ")
        lang_input = input("Введіть мову інтерфейсу: ")

        data_to_save: AppData = {
            "v1": float(v1_input),
            "v2": float(v2_input),
            "lang": lang_input.strip().lower(),
        }

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        print(f"Дані збережено в файл {DATA_FILE}")

    except ValueError:
        print("Помилка: Введено некоректні числові дані.")
        sys.exit(1)


def process_data(data: AppData) -> None:
    v1 = data["v1"]
    v2 = data["v2"]
    lang = data["lang"]

    if lang not in ["uk", "en"]:
        lang = "uk"

    v1_ms, v2_kmh, comparison_result = convert_and_compare_speeds(v1, v2)

    f_v1 = format_number(v1)
    f_v2 = format_number(v2)
    f_v1_ms = format_number(v1_ms)
    f_v2_kmh = format_number(v2_kmh)

    c_v1_red = apply_color(f_v1, Fore.RED)
    c_v2_red = apply_color(f_v2, Fore.RED)
    c_v1_ms_red = apply_color(f_v1_ms, Fore.RED)
    c_v2_kmh_red = apply_color(f_v2_kmh, Fore.RED)

    unit_kmh = translate("unit_kmh", lang)
    unit_ms = translate("unit_ms", lang)

    comp_v1_blue = apply_color(f"{f_v1} {unit_kmh}", Fore.BLUE)
    comp_v2_blue = apply_color(f"{f_v2} {unit_ms}", Fore.BLUE)

    lang_name_colored = apply_color(translate("lang_name", lang), Fore.BLUE)

    output = (
        f"{translate('lang_label', lang)}{lang_name_colored}\n"
        f"{translate('v1_label', lang)}{f_v1}\n"
        f"{translate('v2_label', lang)}{f_v2}\n\n"
        f"{translate('conv_1', lang).format(c_v1_red, c_v1_ms_red)}\n"
        f"{translate('conv_2', lang).format(c_v2_red, c_v2_kmh_red)}\n\n"
        f"{translate(comparison_result, lang).format(comp_v1_blue, comp_v2_blue)}"
    )

    print(output)


def main() -> None:
    try:
        data = read_data()
        process_data(data)
    except ValueError:
        prompt_and_save_data()


if __name__ == "__main__":
    main()
