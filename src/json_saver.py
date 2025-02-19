import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class FileOperations(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def save(self, data: List[Dict[str, Any]]):
        """Сохраняет данные в файл"""
        pass

    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        """Загружает данные из файла"""
        pass


class JSONFileSaver(FileOperations):
    """Класс для работы с JSON-файлами."""

    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data: List[Dict[str, Any]]):
        """Добавляет данные в файл."""
        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def load(self) -> List[Dict[str, Any]]:
        """Загружает данные из файла, если файл существует, иначе возвращает пустой список"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Файл не найден. Убедитесь, что вы сначала сохранили вакансии.")
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Убедитесь, что файл содержит корректный JSON.")
            return []


def get_top_n_vacancies(file_saver, n):
    """Функция сортирующая топ вакансий"""
    vacancies = file_saver.load()

    def get_salary(vacancy):
        try:
            salary = vacancy.get("salary").get("from")
        except Exception:
            return 0
        if isinstance(salary, (int, float)):
            return salary
        return 0

    top_vacancies = sorted(vacancies, key=get_salary, reverse=True)[:n]
    return top_vacancies
