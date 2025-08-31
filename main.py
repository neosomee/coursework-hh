import sys
import os
from src.config import config
from src.dbManager import DBManager
from src.hh import HeadHunterAPI
from src.vacancies import Vacancy
from src.reader import create_DB, save_to_DB

# Настройка кодировки консоли
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Удаление переменных окружения PostgreSQL
os.environ.pop('PGPASSWORD', None)
os.environ.pop('PGCLIENTENCODING', None)

def main():
    company_ids = [
        "3489751",
        "8723019",
        "5621893",
        "4310975",
        "10598372",
        "7643120",
        "2398750",
        "9876543",
        "6758493",
        "3147852",
    ]

    params = config()
    vacancies = HeadHunterAPI(company_ids)

    if vacancies.get_vacancies() != [[]]:
        user_input = input("Введите ключевое слово для поиска вакансий: ")

        create_DB("HHApi", params)

        for vacancy in vacancies.get_vacancies()[0]:
            vac = Vacancy(vacancy)
            save_to_DB("HHApi", vac, params)

        dbmanager = DBManager("HHApi", params)
        companies_and_vacancies_count = dbmanager.get_companies_and_vacancies_count()
        all_vacancies = dbmanager.get_all_vacancies()
        avg_salary = dbmanager.get_avg_salary()
        vacancies_with_higher_salary = dbmanager.get_vacancies_with_higher_salary()
        vacancies_with_keyword = dbmanager.get_vacancies_with_keyword(user_input)

        print(
            f"""
            Компании и их количество вакансий: {companies_and_vacancies_count}
            Все вакансии: {all_vacancies}
            Средняя зарплата по вакансиям: {avg_salary}
            Вакансии с зарплатой выше среднего: {vacancies_with_higher_salary}
            Вакансии с ключевым словом в названии {vacancies_with_keyword}"""
        )

if __name__ == "__main__":
    main()