import asyncio
import time
import re
import sys
from googletrans import Translator, LANGUAGES
from colorama import init, Fore, Style

# Ініціалізація colorama для підтримки кольорів у Windows/Linux
init(autoreset=True)

# Кольорові константи
INFO = Fore.CYAN + "[INFO] " + Style.RESET_ALL
SUCCESS = Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL
WARN = Fore.YELLOW + "[WARNING] " + Style.RESET_ALL
ERR = Fore.RED + "[ERROR] " + Style.RESET_ALL
HEADER = Fore.MAGENTA + Style.BRIGHT


def TransLate(text: str, lang: str) -> str:
    """Синхронний переклад одного речення."""
    translator = Translator()
    try:
        target_lang = lang.lower()
        if target_lang not in LANGUAGES:
            for code, name in LANGUAGES.items():
                if name.lower() == target_lang:
                    target_lang = code
                    break

        result = translator.translate(text, dest=target_lang)
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)

        return result.text
    except Exception as e:
        return f"Error: {str(e)}"


def LangDetect(txt: str) -> str:
    """Визначення мови."""
    translator = Translator()
    try:
        det = translator.detect(txt)
        if asyncio.iscoroutine(det):
            det = asyncio.run(det)

        lang_code = det.lang[0] if isinstance(det.lang, list) else det.lang
        lang_name = LANGUAGES.get(lang_code, "Unknown")
        return f"{Fore.YELLOW}{lang_name}{Style.RESET_ALL} (Code: {lang_code}, Confidence: {det.confidence})"
    except Exception as e:
        return f"Error: {str(e)}"


def CodeLang(lang: str) -> str:
    """Пошук мови за кодом."""
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang].capitalize()
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Error"


async def process_async_all(text: str, sentences: list, dest_lang: str):
    """Асинхронний диспетчер задач."""
    tasks = [asyncio.to_thread(LangDetect, text)]

    for s in sentences:
        tasks.append(asyncio.to_thread(TransLate, s, dest_lang))

    # Чекаємо виконання всіх задач одночасно
    return await asyncio.gather(*tasks)


def run_lab():
    file_name = "text.txt"
    target_lang = "it"

    print(f"\n{HEADER}=== ЛАБОРАТОРНА РОБОТА: АНАЛІЗ ТА ПЕРЕКЛАД ===\n")

    # 1. Читання файлу
    print(f"{INFO}Спроба читання файлу '{file_name}'...")
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            full_text = f.read()
        print(f"{SUCCESS}Файл успішно прочитано!")
    except Exception as e:
        print(f"{ERR}Помилка читання файлу: {e}")
        return

    # 2. Парсинг
    txt_list = [s.strip() for s in re.split(r"(?<=[.!?])\s+", full_text) if s.strip()]

    print(f"\n{HEADER}--- СТАТИСТИКА ФАЙЛУ ---")
    print(f"Кількість символів: {Fore.CYAN}{len(full_text)}{Style.RESET_ALL}")
    print(f"Кількість речень: {Fore.CYAN}{len(txt_list)}{Style.RESET_ALL}\n")

    # --- 3.4.1 СИНХРОННИЙ РЕЖИМ ---
    print(f"{HEADER}--- СИНХРОННИЙ РЕЖИМ (Обробка по черзі) ---")
    start_sync = time.perf_counter()

    print(f"{INFO}Визначаю мову оригіналу...")
    sync_detect = LangDetect(full_text)

    sync_translated_sentences = []
    for i, sentence in enumerate(txt_list):
        # Імітація статус-бару
        sys.stdout.write(f"\r{INFO}Переклад речення [{i+1}/{len(txt_list)}]...")
        sys.stdout.flush()
        sync_translated_sentences.append(TransLate(sentence, target_lang))

    end_sync = time.perf_counter()
    sync_time = end_sync - start_sync
    print(f"\n{SUCCESS}Синхронний переклад завершено!\n")

    # --- 3.4.2 АСИНХРОННИЙ РЕЖИМ ---
    print(f"{HEADER}--- АСИНХРОННИЙ РЕЖИМ (Паралельна обробка) ---")
    start_async = time.perf_counter()

    print(f"{INFO}Відправляю всі {len(txt_list)} речень та запит детекції одночасно...")

    async_results = asyncio.run(process_async_all(full_text, txt_list, target_lang))

    async_detect = async_results[0]
    async_translated_sentences = async_results[1:]

    end_async = time.perf_counter()
    async_time = end_async - start_async
    print(f"{SUCCESS}Асинхронний переклад завершено!\n")

    translated_text = " ".join(async_translated_sentences)

    # --- 3.5 ВИВІД РЕЗУЛЬТАТІВ ---
    print(f"{HEADER}=== ФІНАЛЬНИЙ ЗВІТ ===\n")

    print(f"{Fore.BLUE}ОРИГІНАЛ:{Style.RESET_ALL}")
    print(f"Визначення (Асинхронно): {async_detect}")
    print(
        f"{Fore.LIGHTBLACK_EX}{full_text[:150]}...{Style.RESET_ALL}\n"
    )

    print(f"{Fore.BLUE}ПЕРЕКЛАД НА {CodeLang(target_lang).upper()}:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{translated_text[:150]}...{Style.RESET_ALL}\n")

    # --- ПРОДУКТИВНІСТЬ ---
    print(f"{HEADER}--- ПРОДУКТИВНІСТЬ (ЧАС) ---")

    # Визначаємо кольори: переможець - зелений, інший - червоний
    if async_time < sync_time:
        color_async = Fore.GREEN
        color_sync = Fore.RED
        winner_info = f"{INFO}Асинхронний режим швидший у {Fore.YELLOW}{sync_time / async_time:.1f}x{Style.RESET_ALL} разів!"
    else:
        color_async = Fore.RED
        color_sync = Fore.GREEN
        winner_info = f"{WARN}Синхронний режим виявився швидшим (можливо, через мережеву затримку)!"

    print(f"Синхронно (3.4.1):  {color_sync}{sync_time:.4f} сек{Style.RESET_ALL}")
    print(f"Асинхронно (3.4.2): {color_async}{async_time:.4f} сек{Style.RESET_ALL}")

    print(winner_info)
    print("\n")


if __name__ == "__main__":
    run_lab()
