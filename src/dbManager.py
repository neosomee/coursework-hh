import psycopg2


class DBManager:
    """Класс для подключения к базе данных"""

    def __init__(self, database, params):
        self.database = database
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database, **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute(
            """SELECT e.company_name, COUNT(v.vacancy_name) FROM employers e
                        JOIN vacancies v USING(company_id) GROUP BY company_name;"""
        )

        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(
            """SELECT e.company_name, v.vacancy_name, v.salary, v.url FROM employers e
                        JOIN vacancies v USING(company_id);"""
        )

        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(salary) FROM vacancies;")
        return float(self.cur.fetchall()[0][0])

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT * FROM vacancies WHERE salary > %s;", (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%';")
        return self.cur.fetchall()
