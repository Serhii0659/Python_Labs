import urllib.parse

import pyperclip


def main():
    # Формат (II) з буфера або вводу
    encoded_url = "https://uk.wikipedia.org/wiki/%D0%A8%D1%82%D1%83%D1%87%D0%BD%D0%B8%D0%B9_%D1%96%D0%BD%D1%82%D0%B5%D0%BB%D0%B5%D0%BA%D1%82"

    # Перетворення до формату (I)
    decoded_url = urllib.parse.unquote(encoded_url)

    print(f"Вхідне посилання: {encoded_url}")
    print(f"Результат: {decoded_url}")

    # Копіювання в буфер обміну
    pyperclip.copy(decoded_url)
    print("\n[INFO] Декодоване посилання скопійовано в буфер обміну.")


if __name__ == "__main__":
    main()
