from unittest.mock import MagicMock, patch

import pytest

from src.api import HH  # Предположим, что ваш класс HH находится в файле hh.py
from src.vacancy import Vacancy  # Предположим, что класс Vacancy импортируется из vacancy.py


@patch("requests.get")
def test_load_vacancies(mock_get, hh_parser):

    mock_response = {
        "items": [
            {
                "name": "Вакансия Python Developer",
                "salary": {"from": 80000, "to": 120000},
                "alternate_url": "https://hh.ru/vacancy/1",
                "employer": {"name": "Компания A"},
            },
            {
                "name": "Вакансия Java Developer",
                "salary": {"from": 50000, "to": 100000},
                "alternate_url": "https://hh.ru/vacancy/2",
                "employer": {"name": "Компания B"},
            },
        ]
    }

    mock_get.return_value = MagicMock()
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = MagicMock()

    keywords = "Python"
    vacancies = hh_parser.load_vacancies(keywords)

    assert len(vacancies) == 1
    assert vacancies[0].name == "Вакансия Python Developer"
    assert vacancies[0].salary == mock_response["items"][0]["salary"]
    assert vacancies[0].url == mock_response["items"][0]["alternate_url"]
    assert vacancies[0].company == mock_response["items"][0]["employer"]["name"]


@patch("requests.get")
def test_no_matching_vacancies(mock_get, hh_parser):

    mock_response = {"items": []}

    mock_get.return_value = MagicMock()
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = MagicMock()

    keywords = "Data Scientist"
    vacancies = hh_parser.load_vacancies(keywords)

    assert len(vacancies) == 0


@patch("requests.get")
def test_partial_vacancies(mock_get, hh_parser):

    mock_response = {
        "items": [
            {
                "name": "Вакансия Python Developer",
                "salary": {"from": 80000, "to": 120000},
                "alternate_url": "https://hh.ru/vacancy/1",
                "employer": {"name": "Компания A"},
            },
            {
                "name": "Вакансия C# Developer",
                "salary": {"from": 60000, "to": 90000},
                "alternate_url": "https://hh.ru/vacancy/2",
                "employer": {"name": "Компания B"},
            },
        ]
    }

    mock_get.return_value = MagicMock()
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = MagicMock()

    keywords = "Python C#"
    vacancies = hh_parser.load_vacancies(keywords)

    assert len(vacancies) == 2
    assert vacancies[0].name == "Вакансия Python Developer"
    assert vacancies[1].name == "Вакансия C# Developer"
