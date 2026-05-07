import os
import sys


def main() -> None:
    surname = os.environ.get("SURNAME")
    if surname:
        print(f"Знайдено змінну SURNAME: {surname}")
    else:
        print("Помилка: змінну SURNAME не знайдено в системі.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
