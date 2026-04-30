import asyncio

from googletrans import LANGUAGES, Translator


def _get_lang_code(lang_input: str) -> str:
    """Допоміжна функція для отримання коду мови з назви або коду."""
    lang_input = lang_input.lower()
    if lang_input == "auto" or lang_input in LANGUAGES:
        return lang_input

    # Пошук коду за назвою мови
    for code, name in LANGUAGES.items():
        if name.lower() == lang_input:
            return code

    return lang_input  # Повертаємо як є, якщо не знайдено


async def TransLate(text: str, scr: str, dest: str) -> str:
    """Асинхронний переклад тексту."""
    translator = Translator()
    try:
        src_code = _get_lang_code(scr)
        dest_code = _get_lang_code(dest)

        result = translator.translate(text, src=src_code, dest=dest_code)
        if asyncio.iscoroutine(result):
            result = await result

        return result.text
    except Exception as e:
        return f"Error: {str(e)}"


async def LangDetect(text: str, set_opt: str = "all") -> str:
    """Асинхронне визначення мови"""
    translator = Translator()
    result = ""
    try:
        det = translator.detect(text)
        if asyncio.iscoroutine(det):
            det = await det

        lang_code = det.lang[0] if isinstance(det.lang, list) else det.lang
        conf = det.confidence[0] if isinstance(det.confidence, list) else det.confidence

        if set_opt == "lang":
            result = lang_code
        elif set_opt == "confidence":
            result = str(conf)
        else:
            result = f"Language: {lang_code}, Confidence: {conf}"
    except Exception as e:
        result = f"Error: {str(e)}"

    return result


async def CodeLang(lang: str) -> str:
    """Отримання коду або назви мови за введеним текстом"""
    # Додаємо мікро-await для відповідності async статусу модуля
    await asyncio.sleep(0)

    search_term = lang.lower()
    if search_term in LANGUAGES:
        return LANGUAGES[search_term].capitalize()

    for code, name in LANGUAGES.items():
        if name.lower() == search_term:
            return code

    return "Error: Language not found"


def _save_to_file(filename: str, data: str):
    """Синхронна функція запису для використання в потоці"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


async def LanguageList(out: str = "screen", text: str = "") -> str:
    """Асинхронний вивід таблиці мов"""
    translator = Translator()
    try:
        headers = (
            f"{'N':<4} {'Language':<20} {'ISO-639 code':<15} {'Text' if text else ''}"
        )
        lines = [headers, "-" * 80]

        count = 1
        for code, name in list(LANGUAGES.items())[:20]:
            translated_text = ""
            if text:
                res = translator.translate(text, dest=code)
                if asyncio.iscoroutine(res):
                    res = await res
                translated_text = res.text
            lines.append(
                f"{count:<4} {name.capitalize():<20} {code:<15} {translated_text}"
            )
            count += 1

        output = "\n".join(lines)

        if out == "file":
            # Використовуємо потік для запису файлу, щоб не блокувати Event Loop
            await asyncio.to_thread(_save_to_file, "lang_list_gtrans4.txt", output)
        else:
            print(output)

        return "Ok"
    except Exception as e:
        return f"Error: {str(e)}"
