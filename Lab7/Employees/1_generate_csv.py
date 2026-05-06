import csv
import random
from datetime import date

from faker import Faker

COL_SURNAME = "Прізвище"
COL_NAME = "Ім’я"
COL_PATRONYMIC = "По батькові"
COL_GENDER = "Стать"
COL_BIRTH = "Дата народження"
COL_POSITION = "Посада"
COL_CITY = "Місто проживання"
COL_ADDRESS = "Адреса проживання"
COL_PHONE = "Телефон"
COL_EMAIL = "Email"

def generate_patronymics() -> tuple[list[str], list[str]]:
    male_patronymics = [
        "Миколайович",
        "Олександрович",
        "Іванович",
        "Васильович",
        "Петрович",
        "Вікторович",
        "Михайлович",
        "Сергійович",
        "Анатолійович",
        "Володимирович",
        "Юрійович",
        "Андрійович",
        "Борисович",
        "Григорович",
        "Дмитрович",
        "Євгенович",
        "Леонідович",
        "Максимович",
        "Павлович",
        "Романович",
        "Тарасович",
    ]
    female_patronymics = [
        "Миколаївна",
        "Олександрівна",
        "Іванівна",
        "Василівна",
        "Петрівна",
        "Вікторівна",
        "Михайлівна",
        "Сергіївна",
        "Анатоліївна",
        "Володимирівна",
        "Юріївна",
        "Андріївна",
        "Борисівна",
        "Григорівна",
        "Дмитрівна",
        "Євгенівна",
        "Леонідівна",
        "Максимівна",
        "Павлівна",
        "Романівна",
        "Тарасівна",
    ]
    return male_patronymics, female_patronymics


def generate_employees_data(total_records: int = 500) -> list[dict]:
    fake = Faker(locale="uk_UA")
    male_patr, female_patr = generate_patronymics()
    num_males = int(total_records * 0.6)
    data = []
    start_date = date(1946, 1, 1)
    end_date = date(2011, 12, 31)

    for _ in range(num_males):
        data.append(
            {
                COL_SURNAME: fake.last_name_male(),
                COL_NAME: fake.first_name_male(),
                COL_PATRONYMIC: random.choice(male_patr),
                COL_GENDER: "Чоловіча",
                COL_BIRTH: fake.date_between(
                    start_date=start_date, end_date=end_date
                ).strftime("%Y-%m-%d"),
                COL_POSITION: fake.job(),
                COL_CITY: fake.city(),
                COL_ADDRESS: fake.street_address(),
                COL_PHONE: fake.phone_number(),
                COL_EMAIL: fake.email(),
            }
        )

    for _ in range(total_records - num_males):
        data.append(
            {
                COL_SURNAME: fake.last_name_female(),
                COL_NAME: fake.first_name_female(),
                COL_PATRONYMIC: random.choice(female_patr),
                COL_GENDER: "Жіноча",
                COL_BIRTH: fake.date_between(
                    start_date=start_date, end_date=end_date
                ).strftime("%Y-%m-%d"),
                COL_POSITION: fake.job(),
                COL_CITY: fake.city(),
                COL_ADDRESS: fake.street_address(),
                COL_PHONE: fake.phone_number(),
                COL_EMAIL: fake.email(),
            }
        )

    random.shuffle(data)
    return data


def main():
    filename = "employees.csv"
    fieldnames = [
        COL_SURNAME,
        COL_NAME,
        COL_PATRONYMIC,
        COL_GENDER,
        COL_BIRTH,
        COL_POSITION,
        COL_CITY,
        COL_ADDRESS,
        COL_PHONE,
        COL_EMAIL,
    ]

    employees = generate_employees_data()

    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)

    print(f"Сгенеровано {len(employees)} записів. Файл '{filename}' успішно створено.")


if __name__ == "__main__":
    main()
