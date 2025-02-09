from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests

from src.vacancy import Vacancy


class Parser(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def load_vacancies(self, keyword: str) -> List[Vacancy]:
        """Загружает вакансии по ключевому слову"""
        pass


class HH(Parser):
    """Класс для взаимодействия с API HeadHunter"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"page": 0, "per_page": 100}

    def load_vacancies(self, keywords: str) -> List[Vacancy]:
        """Загружает вакансии, фильтруя по ключевым словам."""
        keywords_list = keywords.lower().split(" ")
        vacancies = []

        while self.params["page"] < 20:
            vacancies_data = self._fetch_data_from_api()
            for vacancy_data in vacancies_data:
                if any(keyword in vacancy_data.get("name", "").lower() for keyword in keywords_list):
                    vacancy = Vacancy(
                        name=vacancy_data.get("name", ""),
                        salary=vacancy_data.get("salary"),
                        url=vacancy_data.get("alternate_url", ""),
                        company=vacancy_data.get("employer", {}).get("name", ""),
                    )
                    vacancies.append(vacancy)

            # Проверяем, если меньше 100 вакансий было возвращено, значит, больше запрашивать не нужно
            if len(vacancies_data) < 100:
                break

            self.params["page"] += 1

        return vacancies

    def _fetch_data_from_api(self) -> List[Dict[str, Any]]:
        """Запрашивает данные из API и проверяет статус ответа"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json().get("items", [])
