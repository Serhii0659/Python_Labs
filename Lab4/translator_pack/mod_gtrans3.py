import sys
from googletrans import Translator, LANGUAGES

# Захист від запуску на нових версіях Python (Пункт 5)
if sys.version_info >= (3, 13):
    print("Помилка: Модуль gtrans3.py НЕ ПІДТРИМУЄТЬСЯ в Python 3.13+")
    sys.exit(1)


def _resolve_lang_code(lang_input: str) -> str:
    """Приватна функція для усунення вкладених умов (Виправлення S3358)."""
    lang_input = lang_input.lower()
    if lang_input == "auto" or lang_input in LANGUAGES:
        return lang_input

    # Пошук коду за назвою мови
    for code, name in LANGUAGES.items():
        if name.lower() == lang_input:
            return code

    return lang_input


def TransLate(text: str, scr: str, dest: str) -> str:
    translator = Translator()
    try:
        src_code = _resolve_lang_code(scr)
        dest_code = _resolve_lang_code(dest)

        # type: ignore використовується для коректної роботи в Docker з версією 3.1.0a0
        result = translator.translate(text, src=src_code, dest=dest_code)  # type: ignore
        return result.text  # type: ignore
    except Exception as e:
        return f"Error: {str(e)}"


def LangDetect(text: str, set_opt: str = "all") -> str:
    """Визначення мови (Виправлення S1142)."""
    translator = Translator()
    result = ""
    try:
        det = translator.detect(text)  # type: ignore
        if set_opt == "lang":
            result = det.lang  # type: ignore
        elif set_opt == "confidence":
            result = str(det.confidence)  # type: ignore
        else:
            result = f"Language: {det.lang}, Confidence: {det.confidence}"  # type: ignore
    except Exception as e:
        result = f"Error: {str(e)}"
    return result


def CodeLang(lang: str) -> str:
    lang_lower = lang.lower()
    if lang_lower in LANGUAGES:
        return LANGUAGES[lang_lower].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang_lower:
            return code
    return "Error: Language not found"


def LanguageList(out: str = "screen", text: str = "") -> str:
    translator = Translator()
    try:
        headers = (
            f"{'N':<4} {'Language':<20} {'ISO-639 code':<15} {'Text' if text else ''}"
        )
        lines = [headers, "-" * 80]
        for count, (code, name) in enumerate(list(LANGUAGES.items())[:20], 1):
            translated_text = ""
            if text:
                res = translator.translate(text, dest=code)  # type: ignore
                translated_text = res.text  # type: ignore
            lines.append(
                f"{count:<4} {name.capitalize():<20} {code:<15} {translated_text}"
            )

        output = "\n".join(lines)
        if out == "file":
            with open("lang_list_gtrans3.txt", "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)
        return "Ok"
    except Exception as e:
        return f"Error: {str(e)}"
