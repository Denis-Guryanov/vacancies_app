import pytest

from src.vacancy import Vacancy


def test_get_salary(vacancy):
    """Тестируем метод get_salary."""
    salary = vacancy.get_salary()
    assert salary == 80000


def test_get_salary_no_salary():
    """Тестируем get_salary, когда salary не предоставлено."""
    vacancy_no_salary = Vacancy(
        name="Вакансия без зарплаты", salary=None, url="https://hh.ru/vacancy/2", company="Компания B"
    )
    salary = vacancy_no_salary.get_salary()
    assert salary == 0


def test_to_dict(vacancy):
    """Тестируем метод to_dict."""
    dict_representation = vacancy.to_dict()

    expected_dict = {
        "name": "Вакансия Python Developer",
        "salary": {"from": 80000, "to": 120000},
        "url": "https://hh.ru/vacancy/1",
        "company": "Компания A",
    }
    assert dict_representation == expected_dict


def test_validate_salary_valid():
    """Тестируем validate_salary с корректными данными."""
    valid_salary = {"from": 50000, "to": 100000}
    assert Vacancy.validate_salary(valid_salary) is True


def test_validate_salary_invalid():
    """Тестируем validate_salary с некорректными данными."""
    invalid_salary = {"amount": 50000}
    assert Vacancy.validate_salary(invalid_salary) is False


def test_validate_salary_not_a_dict():
    """Тестируем validate_salary с не сущностями словаря."""
    assert Vacancy.validate_salary(50000) is False
    assert Vacancy.validate_salary("salary") is False
    assert Vacancy.validate_salary(None) is False
