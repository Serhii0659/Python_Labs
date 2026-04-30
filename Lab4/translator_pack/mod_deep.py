from deep_translator import GoogleTranslator
from langdetect import detect_langs, DetectorFactory
from typing import Dict

# Стабілізація результатів langdetect
DetectorFactory.seed = 0


def get_langs() -> Dict[str, str]:
    """Отримання підтримуваних мов як словника."""
    # Явно повертаємо результат як словник для Pylance
    return dict(GoogleTranslator().get_supported_languages(as_dict=True))


def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        src_code = "auto" if scr == "auto" else scr
        translator = GoogleTranslator(source=src_code, target=dest)
        return translator.translate(text)
    except Exception as e:
        return f"Error: {str(e)}"


def LangDetect(text: str, set_opt: str = "all") -> str:
    """Визначення мови з однією точкою виходу (Виправлення S1142)."""
    result = ""
    try:
        res = detect_langs(text)[0]
        if set_opt == "lang":
            result = res.lang
        elif set_opt == "confidence":
            result = str(res.prob)
        else:
            result = f"Language: {res.lang}, Confidence: {res.prob}"
    except Exception as e:
        result = f"Error: {str(e)}"
    return result


def CodeLang(lang: str) -> str:
    """Пошук коду або назви (Виправлення Pylance items)."""
    langs = get_langs()
    search_term = lang.lower()
    result = "Error: Not found"

    # Використовуємо .items() для словника
    for name, code in langs.items():
        if code == search_term:
            result = name.capitalize()
            break
        if name.lower() == search_term:
            result = code
            break
    return result


def LanguageList(out: str = "screen", text: str = "") -> str:
    """Вивід таблиці мов (Виправлення Pylance items)."""
    try:
        langs = get_langs()
        headers = (
            f"{'N':<4} {'Language':<20} {'ISO-639 code':<15} {'Text' if text else ''}"
        )
        lines = [headers, "-" * 80]

        for count, (name, code) in enumerate(list(langs.items())[:20], 1):
            translated = ""
            if text:
                translated = GoogleTranslator(source="auto", target=code).translate(
                    text
                )
            lines.append(f"{count:<4} {name.capitalize():<20} {code:<15} {translated}")

        output = "\n".join(lines)
        if out == "file":
            with open("lang_list_deep.txt", "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)
        return "Ok"
    except Exception as e:
        return f"Error: {str(e)}"
