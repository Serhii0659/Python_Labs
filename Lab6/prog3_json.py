import json


def main():
    data = {
        "Коваленко": ["Сергій", "Миколайович", 2006],
        "Шевченко": ["Андрій", "Миколайович", 1976],
        "Петренко": ["Олександр", "Іванович", 1995],
        "Сидоренко": ["Марія", "Василівна", 2000],
        "Бондаренко": ["Дмитро", "Леонідович", 1988],
        "Ткаченко": ["Олена", "Вікторівна", 1992],
        "Коваль": ["Іван", "Петрович", 1985],
        "Мороз": ["Тетяна", "Сергіївна", 1999],
        "Лисенко": ["Микола", "Віталійович", 1970],
        "Кравченко": ["Анна", "Олегівна", 2001],
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("[SUCCESS] Словник записано у data.json")

    with open("data.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    print("\n--- Дані з JSON файлу ---")
    for surname, info in loaded_data.items():
        print(f"{surname}: {info[0]} {info[1]}, {info[2]} р.н.")


if __name__ == "__main__":
    main()
