import re
import requests
from bs4 import BeautifulSoup


def extract_phone_numbers(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все текстовые узлы на странице
        text_nodes = soup.find_all()
        # Используем регулярное выражение для поиска номеров телефонов в нужном формате
        phone_pattern = re.compile(r'8\s?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}')

        phone_numbers = set()

        for node in text_nodes:
            # print(node.get_text())
            text = node.get_text()
            if "+7" in text:
                # На случай если есть номера телефонов вида +7 (решил сделать на всякий случай)
                text = text.replace("+7", "8")
            # Подставляю регулярное выражение для поиска номеров
            matches = phone_pattern.findall(text)
            phone_numbers.update(matches)

        return phone_numbers

    # Обработка ошибок
    except Exception as e:
        print(f"Произошла ошибка при работе с ссылкой {url}: Ошибка: {e}")
        return set()


if __name__ == "__main__":
    # Пример использования
    # Можно сюда добавить еще сайты, либо реализовать чтение их из файла
    urls = [
        "https://hands.ru/company/about",
        "https://repetitors.info"
    ]

    for url in urls:
        numbers = extract_phone_numbers(url)
        if numbers:
            print(f"Найдены номера телефонов по ссылке {url}: {numbers}")
        else:
            print(f"Номера телефонов не найдены по ссылке {url}")
