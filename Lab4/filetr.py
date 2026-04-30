import json
import os
import re
from importlib import import_module


def main():
    config_file = "config.json"

    if not os.path.exists(config_file):
        print(f"Помилка: Конфігураційний файл {config_file} не знайдено.")
        return

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    file_name = config.get("text_file")
    target_lang = config.get("target_lang")
    mod_name = config.get("module_name")
    output_method = config.get("output")
    max_sent = config.get("max_sentences")

    if not os.path.exists(file_name):
        print(f"Помилка: Файл {file_name} не знайдено.")
        return

    # Динамічний імпорт вибраного модуля
    try:
        translator_mod = import_module(f"translator_pack.{mod_name}")
    except ModuleNotFoundError:
        print(f"Помилка: Модуль {mod_name} не знайдено в пакеті.")
        return

    with open(file_name, "r", encoding="utf-8") as f:
        full_text = f.read()

    # I. Вивід статистики
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", full_text) if s.strip()]
    file_size = os.path.getsize(file_name)
    char_count = len(full_text)

    # Визначаємо мову в залежності від того, який модуль вибрано (асинхр чи синхр)
    import asyncio

    if mod_name == "mod_gtrans4":
        lang_info = asyncio.run(translator_mod.LangDetect(full_text, "lang"))
    else:
        lang_info = translator_mod.LangDetect(full_text, "lang")

    print("--- АНАЛІЗ ФАЙЛУ ---")
    print(f"Файл: {file_name} ({file_size} байт)")
    print(f"Символів: {char_count}")
    print(f"Речень у файлі: {len(sentences)}")
    print(f"Мова оригіналу: {lang_info}")
    print("-" * 40)

    # II. Обмеження речень
    sentences_to_translate = sentences[:max_sent]
    text_to_translate = " ".join(sentences_to_translate)

    # III. Переклад
    if mod_name == "mod_gtrans4":
        translated_text = asyncio.run(
            translator_mod.TransLate(text_to_translate, "auto", target_lang)
        )
    else:
        translated_text = translator_mod.TransLate(
            text_to_translate, "auto", target_lang
        )

    # IV & V. Вивід
    if output_method == "screen":
        print(f"Мова перекладу: {target_lang}")
        print(f"Використаний модуль: {mod_name}")
        print(f"Переклад:\n{translated_text}")
    elif output_method == "file":
        name, ext = os.path.splitext(file_name)
        new_file_name = f"{name}_{target_lang}{ext}"
        try:
            with open(new_file_name, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print("Ok")
        except Exception as e:
            print(f"Помилка запису файлу: {e}")
    else:
        print("Помилка: Невідомий метод виводу в конфігурації.")


if __name__ == "__main__":
    main()
