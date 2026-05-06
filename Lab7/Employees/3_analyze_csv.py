import sys
import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

COL_GENDER = "Стать"
COL_BIRTH = "Дата народження"
COL_AGE = "Вік"
COL_CATEGORY = "Категорія"
LABEL_COUNT = "Кількість"

CAT_YOUNGER_18 = "younger_18"
CAT_18_45 = "18-45"
CAT_45_70 = "45-70"
CAT_OLDER_70 = "older_70"
AGE_ORDER = [CAT_YOUNGER_18, CAT_18_45, CAT_45_70, CAT_OLDER_70]


def calculate_exact_age(birthdate_series: pd.Series) -> pd.Series:
    current_date = datetime(2026, 5, 7)
    birthdates = pd.to_datetime(birthdate_series)

    years = current_date.year - birthdates.dt.year
    is_before_birthday = (current_date.month < birthdates.dt.month) | (
        (current_date.month == birthdates.dt.month)
        & (current_date.day < birthdates.dt.day)
    )

    return years - is_before_birthday.astype(int)


def categorize_age(age: int) -> str:
    category = CAT_OLDER_70
    if age < 18:
        category = CAT_YOUNGER_18
    elif 18 <= age <= 45:
        category = CAT_18_45
    elif 46 <= age <= 70:
        category = CAT_45_70
    return category


def run_analytics(df: pd.DataFrame):
    gender_counts = df[COL_GENDER].value_counts()
    print("\n--- Кількість співробітників за статтю ---")
    print(gender_counts.to_string())

    plt.figure(figsize=(8, 5))
    gender_counts.plot(kind="bar", color=["#3498db", "#e74c3c"])
    plt.title("Розподіл за статтю")
    plt.ylabel(LABEL_COUNT)
    plt.tight_layout()
    plt.savefig("plot_gender.png")
    plt.close()

    age_counts = df[COL_CATEGORY].value_counts().reindex(AGE_ORDER).fillna(0)
    print("\n--- Кількість співробітників за віковими категоріями ---")
    print(age_counts.to_string())

    plt.figure(figsize=(8, 5))
    age_counts.plot(kind="bar", color="#2ecc71")
    plt.title("Розподіл за віковими категоріями")
    plt.ylabel(LABEL_COUNT)
    plt.tight_layout()
    plt.savefig("plot_age_categories.png")
    plt.close()

    gender_age_cross = (
        pd.crosstab(df[COL_CATEGORY], df[COL_GENDER]).reindex(AGE_ORDER).fillna(0)
    )
    print("\n--- Розподіл статі всередині вікових категорій ---")
    print(gender_age_cross.to_string())

    gender_age_cross.plot(kind="bar", figsize=(10, 6), color=["#e74c3c", "#3498db"])
    plt.title("Стать у розрізі вікових категорій")
    plt.ylabel(LABEL_COUNT)
    plt.tight_layout()
    plt.savefig("plot_gender_by_age.png")
    plt.close()


def main():
    csv_file = "employees.csv"

    try:
        if not os.path.exists(csv_file):
            print(f"Повідомлення: Відсутній файл CSV за шляхом {csv_file}")
            sys.exit(1)

        df = pd.read_csv(csv_file)
        print("Ok")
    except Exception as e:
        print(f"Повідомлення: Проблеми при відкритті файлу CSV. Деталі: {e}")
        sys.exit(1)

    df.loc[:, COL_AGE] = calculate_exact_age(df[COL_BIRTH])
    df.loc[:, COL_CATEGORY] = df[COL_AGE].apply(categorize_age)

    run_analytics(df)

    print("\n[Успіх] Аналіз завершено.")
    print(
        "Згенеровані діаграми: plot_gender.png, plot_age_categories.png, plot_gender_by_age.png"
    )


if __name__ == "__main__":
    main()
