from typing import Any, Dict, List, Optional


class Vacancy:
    """Класс для предоставления вакансий"""

    __slots__ = ("name", "salary", "url", "company")

    def __init__(self, name: str, salary: Optional[Dict[str, Any]], url: str, company: str):
        self.name = name
        self.salary = salary
        self.url = url
        self.company = company

    def get_salary(self) -> int:
        """Возвращает зарплату в виде целого числа"""
        return self.salary["from"] if isinstance(self.salary, dict) and "from" in self.salary else 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "salary": self.salary,
            "url": self.url,
            "company": self.company,
        }

    @staticmethod
    def validate_salary(salary: int) -> bool:
        """Приватный метод для валидации зарплаты."""
        return isinstance(salary, dict) and "from" in salary
