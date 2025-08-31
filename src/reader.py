import psycopg2
from psycopg2 import sql
from typing import Dict, Any

def create_DB(database: str, params: Dict[str, str]) -> None:
    """
    Создает базу данных и таблицы
    """
    print("Connection parameters:", {k: repr(v) for k, v in params.items()})
    try:
        # Формируем DSN вручную для отладки
        dsn = f"dbname=postgres host={params['host']} user={params['user']} password={params['password']} port={params['port']}"
        print(f"DSN: {repr(dsn)}")
        conn = psycopg2.connect(
            dsn=dsn,
            client_encoding='UTF8'
        )
        print("Successfully connected to postgres database")
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(database)))
        cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(database)))

        cur.close()
        conn.close()

        with psycopg2.connect(
                dbname=database,
                host=params['host'],
                user=params['user'],
                password=params['password'],
                port=params['port'],
                client_encoding='UTF8'
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """CREATE TABLE employers (
                        company_id INTEGER PRIMARY KEY,
                        company_name TEXT NOT NULL);"""
                )

                cur.execute(
                    """CREATE TABLE vacancies (
                            vacancy_id INTEGER PRIMARY KEY,
                            vacancy_name VARCHAR,
                            salary NUMERIC,
                            company_id INTEGER REFERENCES employers(company_id),
                            url VARCHAR);"""
                )
                conn.commit()
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        raise
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise


def save_to_DB(database: str, vacancy: Any, params: Dict[str, str]) -> None:
    """
    A function for adding values to a table
    """
    with psycopg2.connect(
            dbname=database,
            host=params['host'],
            user=params['user'],
            password=params['password'],
            port=params['port'],
            client_encoding='UTF8'
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            # Проверяем, существует ли уже компания
            cur.execute(
                "SELECT company_id FROM employers WHERE company_id = %s;",
                (vacancy.employer_id,)
            )

            if not cur.fetchone():
                # Добавляем компанию, если её нет
                cur.execute(
                    """
                    INSERT INTO employers (company_id, company_name) VALUES (%s, %s);
                """,
                    (vacancy.employer_id, vacancy.employer_name),
                )

            # Добавляем вакансию
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, salary, company_id, url) 
                VALUES (%s, %s, %s, %s, %s);
            """,
                (
                    vacancy.id,
                    vacancy.name,
                    vacancy.salary,
                    vacancy.employer_id,
                    vacancy.url,
                ),
            )