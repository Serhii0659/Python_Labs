import asyncio
import time
import re
import sys
from googletrans import Translator, LANGUAGES


def TransLate(text: str, lang: str) -> str:
    translator = Translator()
    try:
        target_lang = lang.lower()
        if target_lang not in LANGUAGES:
            for code, name in LANGUAGES.items():
                if name.lower() == target_lang:
                    target_lang = code
                    break
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"Error: {str(e)}"


def LangDetect(txt: str) -> str:
    translator = Translator()
    try:
        det = translator.detect(txt)
        # Обробка випадку, коли lang повертається як список
        lang_code = det.lang[0] if isinstance(det.lang, list) else det.lang
        return f"Detected(lang={lang_code}, confidence={det.confidence})"
    except Exception as e:
        return f"Error: {str(e)}"


def CodeLang(lang: str) -> str:
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Error: Language not found"


async def translate_async_list(sentences, dest_lang):
    translator = Translator()
    tasks = [
        asyncio.to_thread(translator.translate, s, dest=dest_lang) for s in sentences
    ]
    return await asyncio.gather(*tasks)


def run_lab():
    file_name = "text.txt"
    target_lang = "uk"

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            full_text = f.read()
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return

    # Розбиття на речення (Пункт 3.4.1)
    txt_list = [s.strip() for s in re.split(r"(?<=[.!?])\s+", full_text) if s.strip()]

    print(f"Файл: {file_name}")
    print(f"Кількість символів: {len(full_text)}")
    print(f"Кількість речень: {len(txt_list)}")

    det_info = LangDetect(full_text)
    orig_code = det_info.split("=")[1].split(",")[0]
    print(f"Оригінал: {det_info} | Мова: {CodeLang(orig_code)}")
    print("-" * 50)

    # --- 3.4.1 СИНХРОННИЙ РЕЖИМ ---
    start_sync = time.perf_counter()
    sync_results = []
    for sentence in txt_list:
        sync_results.append(TransLate(sentence, target_lang))
    end_sync = time.perf_counter()

    # --- 3.4.2 АСИНХРОННИЙ РЕЖИМ ---
    start_async = time.perf_counter()
    # Тепер це спрацює без помилок
    async_results = asyncio.run(translate_async_list(txt_list, target_lang))
    end_async = time.perf_counter()

    # Вивід результатів (Пункт 3.5)
    print(f"Переклад на: {CodeLang(target_lang)} ({target_lang})")
    for res in async_results:
        print(f"-> {res.text}")

    print("-" * 50)
    print(f"Час синхронно (3.4.1): {end_sync - start_sync:.4f} сек")
    print(f"Час асинхронно (3.4.2): {end_async - start_async:.4f} сек")
