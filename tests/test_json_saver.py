import json
import os

import pytest

from src.json_saver import JSONFileSaver, get_top_n_vacancies


def test_save_and_load(json_file_saver):
    """Тестируем сохранение и загрузку данных."""
    data = [
        {"name": "Вакансия 1", "salary": {"from": 60000}},
        {"name": "Вакансия 2", "salary": {"from": 80000}},
    ]
    json_file_saver.save(data)

    loaded_data = json_file_saver.load()

    assert loaded_data == data


def test_load_non_existent_file():
    """Тестируем загрузку из несуществующего файла."""
    file_path = "non_existent_file.json"
    file_saver = JSONFileSaver(file_path)
    loaded_data = file_saver.load()
    assert loaded_data == []


def test_load_invalid_json(json_file_saver):
    """Тестируем загрузку из файла с некорректным JSON."""
    with open(json_file_saver.file_path, "w", encoding="utf-8") as f:
        f.write("Некорректные данные")

    loaded_data = json_file_saver.load()
    assert loaded_data == []


def test_get_top_n_vacancies(json_file_saver):
    """Тестируем получение топ вакансий."""
    data = [
        {"name": "Вакансия 1", "salary": {"from": 60000}},
        {"name": "Вакансия 2", "salary": {"from": 80000}},
        {"name": "Вакансия 3", "salary": {"from": 70000}},
    ]
    json_file_saver.save(data)

    top_vacancies = get_top_n_vacancies(json_file_saver, 2)

    expected_top_vacancies = [
        {"name": "Вакансия 2", "salary": {"from": 80000}},
        {"name": "Вакансия 3", "salary": {"from": 70000}},
    ]
    assert top_vacancies == expected_top_vacancies


def test_get_top_n_vacancies_empty_file(json_file_saver):
    """Тестируем получение топ вакансий из пустого файла."""
    top_vacancies = get_top_n_vacancies(json_file_saver, 2)
    assert top_vacancies == []
