import sys
from datetime import datetime

import pandas as pd


def calculate_exact_age(birthdate_series: pd.Series) -> pd.Series:
    current_date = datetime(2026, 5, 7)

    birthdates = pd.to_datetime(birthdate_series)

    ages = (
        current_date.year
        - birthdates.dt.year
        - (
            (current_date.month <= birthdates.dt.month)
            & (current_date.day < birthdates.dt.day)
        )
    )
    return ages


def format_sheet_data(df: pd.DataFrame) -> pd.DataFrame:
    formatted_df = df.copy()

    cols = ["Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"]
    result_df = formatted_df[cols].copy()

    result_df.insert(0, "№", range(1, len(result_df) + 1))
    return result_df


def main():
    csv_file = "employees.csv"
    xlsx_file = "employees_age_groups.xlsx"

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("Повідомлення: Відсутній файл CSV. Запустіть спочатку 1_generate_csv.py.")
        sys.exit(1)
    except Exception as e:
        print(f"Повідомлення: Проблеми при відкритті файлу CSV. Деталі: {e}")
        sys.exit(1)

    try:
        df.loc[:, "Вік"] = calculate_exact_age(df["Дата народження"])

        df_all = df.copy()
        df_younger_18 = df[df["Вік"] < 18]
        df_18_45 = df[(df["Вік"] >= 18) & (df["Вік"] <= 45)]
        df_46_70 = df[(df["Вік"] >= 46) & (df["Вік"] <= 70)]
        df_older_70 = df[df["Вік"] > 70]

        with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
            df_all.to_excel(writer, sheet_name="all", index=False)

            format_sheet_data(df_younger_18).to_excel(
                writer, sheet_name="younger_18", index=False
            )
            format_sheet_data(df_18_45).to_excel(
                writer, sheet_name="18-45", index=False
            )
            format_sheet_data(df_46_70).to_excel(
                writer, sheet_name="45-70", index=False
            )
            format_sheet_data(df_older_70).to_excel(
                writer, sheet_name="older_70", index=False
            )

        print("Ok")

    except Exception as e:
        print(f"Повідомлення: Неможливість створення XLSX файлу. Деталі: {e}")


if __name__ == "__main__":
    main()
