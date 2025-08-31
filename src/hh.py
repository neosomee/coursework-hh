from abc import ABC, abstractmethod

import requests


class BaseHeadHunterAPI(ABC):
    """
    Абстрактный класс для HeadHunterAPI.
    """

    @abstractmethod
    def get_vacancies(self, companies) -> None:
        pass

    @abstractmethod
    def get_api(self) -> None:
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    """
    Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
    """

    def __init__(self, companies):
        self.companies = companies
        self.base_url = "https://api.hh.ru/vacancies"
        self.params = {"employer_id": companies}
        self.vacancies = []

    def get_api(self):
        return requests.get(self.base_url, params=self.params)

    def get_vacancies(self, params=None):
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return []