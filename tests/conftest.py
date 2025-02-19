import pytest

from src.api import HH
from src.json_saver import JSONFileSaver
from src.vacancy import Vacancy


@pytest.fixture
def hh_parser():
    """Фикстура для инициализации класса HH."""
    parser = HH()
    return parser


@pytest.fixture
def vacancy():
    """Фикстура для создания экземпляра класса Vacancy."""
    return Vacancy(
        name="Вакансия Python Developer",
        salary={"from": 80000, "to": 120000},
        url="https://hh.ru/vacancy/1",
        company="Компания A",
    )


@pytest.fixture
def json_file_saver(tmp_path):
    """Фикстура для JSONFileSaver с временным файлом."""
    file_path = tmp_path / "test_vacancies.json"
    file_saver = JSONFileSaver(file_path)
    return file_saver
