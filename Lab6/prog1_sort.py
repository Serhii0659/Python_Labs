import re


def custom_sort_key(word):
    ua_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    en_alphabet = "abcdefghijklmnopqrstuvwxyz"

    clean_word = word.lower()
    result_key = []

    for char in clean_word:
        if char in ua_alphabet:
            result_key.append((0, ua_alphabet.index(char)))
        elif char in en_alphabet:
            result_key.append((1, en_alphabet.index(char)))
        else:
            result_key.append((2, ord(char)))
    return result_key


def main():
    try:
        with open("text.txt", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Помилка: Файл text.txt не знайдено.")
        return

    print("--- Початковий текст ---")
    print(content)

    words = re.findall(r"[a-zA-Zа-яА-ЯіїєґІЇЄҐ]+", content)

    sorted_words = sorted(list(set(words)), key=custom_sort_key)

    print("\n--- Відсортований список слів ---")
    print(sorted_words)


if __name__ == "__main__":
    main()
