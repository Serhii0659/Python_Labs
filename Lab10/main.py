import os
import logging
import time
from typing import List, Tuple, Any
import psycopg2
from psycopg2.extensions import connection as PgConnection
from tabulate import tabulate
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ClinicDatabaseManager:
    """Robust CLI tool for managing the private clinic database."""

    def __init__(self) -> None:
        load_dotenv()
        self.host = "localhost"
        self.port = "5432"
        self.database = os.getenv("POSTGRES_DB", "clinic_db")
        self.user = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD", "supersecret")
        self.conn: PgConnection | None = None

    def connect(self, retries: int = 5, delay: int = 2) -> None:
        """Establishes connection to the PostgreSQL database with retries."""
        for attempt in range(retries):
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.database,
                    user=self.user,
                    password=self.password,
                )
                logger.info("Successfully connected to the database.")
                return
            except psycopg2.OperationalError as e:
                logger.warning(
                    f"Connection attempt {attempt + 1} failed. Retrying in {delay} seconds..."
                )
                time.sleep(delay)

        logger.error("Failed to connect to the database after multiple attempts.")
        raise ConnectionError("Database connection failed.")

    def close(self) -> None:
        """Graceful shutdown of database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def execute_query(
        self, query: str, fetch: bool = False
    ) -> List[Tuple[Any, ...]] | None:
        """Executes a SQL query securely."""
        if not self.conn:
            raise ConnectionError("No active database connection.")

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query)
                if fetch:
                    columns = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    return [columns] + results
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                logger.error(f"Error executing query: {e}")
                raise

    def init_schema(self) -> None:
        """Creates tables with constraints, masks, and foreign keys."""
        logger.info("Initializing database schema...")

        # Додано префікс r перед усім рядком """
        schema_sql = r"""
        DROP TABLE IF EXISTS hospital_stays CASCADE;
        DROP TABLE IF EXISTS patients CASCADE;
        DROP TABLE IF EXISTS doctors CASCADE;

        CREATE TABLE doctors (
            doctor_id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(100),
            specialization VARCHAR(50) NOT NULL CHECK (specialization IN ('лор', 'терапевт', 'хірург')),
            experience_years INT CHECK (experience_years >= 0)
        );

        CREATE TABLE patients (
            patient_id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(100),
            address TEXT,
            phone VARCHAR(20) CHECK (phone ~ '^\+38\(\d{3}\)\d{3}-\d{2}-\d{2}$'),
            birth_year INT CHECK (birth_year > 1900 AND birth_year <= EXTRACT(YEAR FROM CURRENT_DATE)),
            category VARCHAR(20) NOT NULL CHECK (category IN ('дитяча', 'доросла'))
        );

        CREATE TABLE hospital_stays (
            stay_id SERIAL PRIMARY KEY,
            patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
            admission_date DATE NOT NULL,
            days_spent INT NOT NULL CHECK (days_spent > 0),
            daily_cost NUMERIC(10, 2) NOT NULL CHECK (daily_cost >= 0),
            discount_percent NUMERIC(5, 2) DEFAULT 0 CHECK (discount_percent >= 0 AND discount_percent <= 100),
            doctor_id INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE RESTRICT
        );
        """
        self.execute_query(schema_sql)
        logger.info("Schema initialized successfully.")

    def seed_data(self) -> None:
        """Populates tables with initial data (4 doctors, 9 patients, 17 stays)."""
        logger.info("Seeding database with initial data...")

        seed_sql = """
        INSERT INTO doctors (last_name, first_name, middle_name, specialization, experience_years) VALUES
        ('Іванов', 'Петро', 'Олексійович', 'хірург', 15),
        ('Смирнова', 'Олена', 'Іванівна', 'терапевт', 8),
        ('Коваленко', 'Ігор', 'Васильович', 'лор', 12),
        ('Шевченко', 'Анна', 'Сергіївна', 'терапевт', 5);

        INSERT INTO patients (last_name, first_name, middle_name, address, phone, birth_year, category) VALUES
        ('Мельник', 'Олександр', 'Юрійович', 'Київ, вул. Хрещатик 1', '+38(050)123-45-67', 1985, 'доросла'),
        ('Ткаченко', 'Марія', 'Вікторівна', 'Київ, вул. Франка 5', '+38(067)234-56-78', 2010, 'дитяча'),
        ('Бойко', 'Дмитро', 'Анатолійович', 'Львів, вул. Зелена 10', '+38(093)345-67-89', 2005, 'дитяча'),
        ('Лисенко', 'Тетяна', 'Ігорівна', 'Одеса, вул. Дерибасівська 2', '+38(050)456-78-90', 1999, 'доросла'),
        ('Гриценко', 'Микола', 'Степанович', 'Київ, вул. Перемоги 12', '+38(067)567-89-01', 1970, 'доросла'),
        ('Романенко', 'Олег', 'Павлович', 'Дніпро, вул. Робоча 8', '+38(093)678-90-12', 2015, 'дитяча'),
        ('Кравчук', 'Вікторія', 'Олександрівна', 'Харків, вул. Сумська 3', '+38(050)789-01-23', 1995, 'доросла'),
        ('Олійник', 'Андрій', 'Васильович', 'Запоріжжя, пр. Соборний 4', '+38(067)890-12-34', 2002, 'доросла'),
        ('Мороз', 'Софія', 'Миколаївна', 'Київ, вул. Садова 6', '+38(093)901-23-45', 2012, 'дитяча');

        INSERT INTO hospital_stays (patient_id, admission_date, days_spent, daily_cost, discount_percent, doctor_id) VALUES
        (1, '2023-01-10', 5, 1500.00, 0, 1),
        (2, '2023-02-15', 3, 1200.00, 10, 3),
        (3, '2023-03-20', 7, 1000.00, 5, 2),
        (4, '2023-04-05', 2, 800.00, 0, 4),
        (5, '2023-05-12', 10, 2000.00, 15, 1),
        (6, '2023-06-18', 4, 1100.00, 10, 3),
        (7, '2023-07-22', 6, 1300.00, 0, 2),
        (8, '2023-08-30', 5, 1400.00, 5, 4),
        (9, '2023-09-14', 3, 900.00, 20, 3),
        (1, '2023-10-01', 2, 1500.00, 0, 2),
        (2, '2023-10-15', 4, 1200.00, 10, 1),
        (3, '2023-11-05', 6, 1000.00, 5, 4),
        (4, '2023-11-20', 3, 800.00, 0, 3),
        (5, '2023-12-01', 8, 2000.00, 15, 2),
        (6, '2023-12-10', 5, 1100.00, 10, 1),
        (7, '2024-01-15', 4, 1300.00, 0, 4),
        (8, '2024-02-20', 7, 1400.00, 5, 3);
        """
        self.execute_query(seed_sql)
        logger.info("Data seeded successfully.")

    def display_results(self, title: str, query: str) -> None:
        """Executes a query and pretty-prints the results using tabulate."""
        print(f"\n{'='*80}\n{title}\n{'='*80}")
        data = self.execute_query(query, fetch=True)
        if data and len(data) > 1:
            headers = data[0]
            rows = data[1:]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No data found.")

    def run_lab_queries(self) -> None:
        """Executes the specific queries required by Lab 9 Variant 10."""

        # 1. Відобразити всіх пацієнтів, які народилися після 1998 року. Відсортувати по прізвищу пацієнта
        q1 = """
        SELECT patient_id, last_name, first_name, birth_year 
        FROM patients 
        WHERE birth_year > 1998 
        ORDER BY last_name;
        """
        self.display_results("1. Пацієнти, які народилися після 1998 року", q1)

        # 2. Порахувати кількість пацієнтів дитячої категорії, та кількість пацієнтів дорослої категорії
        q2 = """
        SELECT category, COUNT(*) as patient_count 
        FROM patients 
        GROUP BY category;
        """
        self.display_results("2. Кількість пацієнтів за категоріями", q2)

        # 3. Порахувати суму лікування, та суму лікування з урахуванням пільги для кожного пацієнта (обчислювальне поле)
        q3 = """
        SELECT 
            p.last_name, 
            p.first_name,
            SUM(hs.days_spent * hs.daily_cost) AS total_cost,
            SUM((hs.days_spent * hs.daily_cost) * (1 - hs.discount_percent / 100)) AS cost_with_discount
        FROM patients p
        JOIN hospital_stays hs ON p.patient_id = hs.patient_id
        GROUP BY p.patient_id, p.last_name, p.first_name;
        """
        self.display_results("3. Вартість лікування (звичайна та зі знижкою)", q3)

        # 4. Відобразити всі звернення до лікаря заданої спеціалізації (запит з параметром)
        target_specialization = "лор"
        q4 = f"""
        SELECT hs.stay_id, p.last_name AS patient, d.last_name AS doctor, hs.admission_date
        FROM hospital_stays hs
        JOIN patients p ON hs.patient_id = p.patient_id
        JOIN doctors d ON hs.doctor_id = d.doctor_id
        WHERE d.specialization = '{target_specialization}';
        """
        self.display_results(
            f"4. Звернення до лікаря спеціалізації: {target_specialization}", q4
        )

        # 5. Порахувати кількість звернень пацієнтів до кожного лікаря (підсумковий запит)
        q5 = """
        SELECT d.last_name, d.first_name, d.specialization, COUNT(hs.stay_id) AS visits_count
        FROM doctors d
        LEFT JOIN hospital_stays hs ON d.doctor_id = hs.doctor_id
        GROUP BY d.doctor_id, d.last_name, d.first_name, d.specialization;
        """
        self.display_results("5. Кількість звернень до кожного лікаря", q5)

        # 6. Перехресний запит: кількість пацієнтів кожної категорії, які лікувалися у лора, терапевта, хірурга
        # В PostgreSQL для цього використовується агрегація з FILTER
        q6 = """
        SELECT 
            p.category,
            COUNT(hs.stay_id) FILTER (WHERE d.specialization = 'лор') AS lor_visits,
            COUNT(hs.stay_id) FILTER (WHERE d.specialization = 'терапевт') AS therapist_visits,
            COUNT(hs.stay_id) FILTER (WHERE d.specialization = 'хірург') AS surgeon_visits
        FROM patients p
        JOIN hospital_stays hs ON p.patient_id = hs.patient_id
        JOIN doctors d ON hs.doctor_id = d.doctor_id
        GROUP BY p.category;
        """
        self.display_results(
            "6. Перехресний запит: звернення за категорією та спеціалізацією", q6
        )


def main() -> None:
    db_manager = ClinicDatabaseManager()
    try:
        db_manager.connect()
        db_manager.init_schema()
        db_manager.seed_data()
        db_manager.run_lab_queries()
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
