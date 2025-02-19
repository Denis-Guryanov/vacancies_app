from src.api import HH
from src.json_saver import JSONFileSaver, get_top_n_vacancies


def interact_with_user():
    """Взаимодействует с пользователем через консоль."""
    file_saver = JSONFileSaver(r'./data/vacancies.json')


    while True:
        print("1. Ввести поисковый запрос.\n"
        "2. Получить топ N вакансий по зарплате.\n"
        "3. Найти вакансии с ключевым словом в описании.\n"
        "4. Выйти.\n")

        choice = input("Выберите опцию: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = HH().load_vacancies(query)
            vacancies_dict = [vacancy.to_dict() for vacancy in vacancies]
            file_saver.save(vacancies_dict)
            print(f"Найдено {len(vacancies)} вакансий по запросу '{query}'.")
            for vacancy in vacancies:
                print(f"{vacancy.name} - {vacancy.get_salary()} ({vacancy.url})")

        elif choice == "2":
            n = int(input("Введите количество вакансий, которые хотите получить: "))
            top_vacancies = get_top_n_vacancies(file_saver, n)
            print(f"Топ {n} вакансий по зарплате:")
            for vacancy in top_vacancies:
                print(f"{vacancy['name']} - {vacancy['salary']} ({vacancy['url']}, {vacancy['company']})")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ")
            vacancies = HH().load_vacancies(keyword)
            filtered_vacancies = [vac for vac in vacancies if keyword.lower() in vac.name.lower()]
            print(f"Найдено {len(filtered_vacancies)} вакансий с ключевым словом '{keyword}':")
            for vacancy in filtered_vacancies:
                print(f"{vacancy.name} - {vacancy.get_salary()} ({vacancy.url})")

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

interact_with_user()