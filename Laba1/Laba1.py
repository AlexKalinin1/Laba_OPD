from bs4 import BeautifulSoup
import requests


def parse_omgtu_employees():
    url = 'https://omgtu.ru/ecab/persons/index.php?b=9'

    page = requests.get(url)
    print(f"Статус код: {page.status_code}")

    soup = BeautifulSoup(page.text, "html.parser")

    persons_content = soup.find('div', class_='persons__content')

    employees = persons_content.find_all('div', class_='person__name')

    employees_list = []
    for employee in employees:
        fio = employee.text.strip()
        employees_list.append(fio)

    with open('employees_k.txt', 'w', encoding='utf-8') as file:
        file.write("СОТРУДНИКИ ОмГТУ, ФАМИЛИЯ КОТОРЫХ НАЧИНАЕТСЯ НА БУКВУ К:\n")
        file.write("=" * 70 + "\n\n")

        for i, fio in enumerate(employees_list, 1):
            file.write(f"{i}. {fio}\n")
            print(f"{i}. {fio}")

    print(f"\nВсего найдено сотрудников: {len(employees_list)}")
    print("Результаты сохранены в файл 'employees_k.txt'")


if __name__ == '__main__':
    parse_omgtu_employees()