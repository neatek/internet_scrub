import requests
from pprint import pprint
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
job_name = input("Write job name: ")
result = requests.get("https://hh.ru/search/vacancy?text=" + job_name, headers=headers)
print("https://hh.ru/search/vacancy?text=" + job_name)
root = html.fromstring(result.content)
main = root.xpath("//main/div")[0]

all_data = []

for job in main:
    title = job.xpath(".//a/text()")
    link = job.xpath(".//a/@href")
    if title:
        salary = job.xpath(".//span/text()")

        # Можно улучшить парсинг данных и добавить много чего на самом деле 😊
        # но в рамках домашней пусть так будет
        for index, rub in enumerate(salary):
            if rub == "руб." or rub == "KZT":
                salary = salary[index - 1] + salary[index]

        obj = {"link": link[0], "title": str(title[0]), "salary": salary}
        all_data.append(obj)

pprint(all_data)

# Write job name: Петя
# https://hh.ru/search/vacancy?text=Петя
# [{'link': 'https://protvino.hh.ru/vacancy/78634508?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ' руб.',
#   'title': 'Сотрудник склада (п. Петро - Славянка)'},
#  {'link': 'https://protvino.hh.ru/vacancy/78634502?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ' руб.',
#   'title': 'Сборщик заказов (п. Петро - Славянка)'},
#  {'link': 'https://protvino.hh.ru/vacancy/79683534?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ' KZT',
#   'title': 'Главный инженер нефтебазы'},
#  {'link': 'https://protvino.hh.ru/vacancy/76463386?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ['Откликнуться'],
#   'title': 'Машинист каротажной станции'},
#  {'link': 'https://protvino.hh.ru/vacancy/79449325?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '90\u202f000 – 110\u202f000 руб.',
#   'title': 'Водитель категории Е'},
#  {'link': 'https://protvino.hh.ru/vacancy/79496435?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ['от ', '25\u202f000', ' ', 'KGS', 'Откликнуться'],
#   'title': 'Лаборант микробиолог'},
#  {'link': 'https://protvino.hh.ru/vacancy/79093871?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '150\u202f000 – 270\u202f000 руб.',
#   'title': 'Помощник специалиста в концертно-театральное агентство'},
#  {'link': 'https://protvino.hh.ru/vacancy/69046757?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '53\u202f000 – 75\u202f000 руб.',
#   'title': 'Менеджер(без поиска р-н Петра Метальникова )'},
#  {'link': 'https://protvino.hh.ru/vacancy/79593913?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '50\u202f000 – 250\u202f000 руб.',
#   'title': 'Менеджер по продажам каркасных деревянных изделий'},
#  {'link': 'https://protvino.hh.ru/vacancy/78053614?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '60\u202f000 – 80\u202f000 руб.',
#   'title': 'Менеджер по работе с клиентами HoReCa для компании "Алтима" '
#            '(алкогольная продукция)'},
#  {'link': 'https://protvino.hh.ru/vacancy/79688155?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '55\u202f000 – 100\u202f000 руб.',
#   'title': 'Менеджер по работе с клиентами'},
#  {'link': 'https://protvino.hh.ru/vacancy/78776153?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '70\u202f000 – 90\u202f000 руб.',
#   'title': 'Менеджер по проектам'},
#  {'link': 'https://protvino.hh.ru/vacancy/52343753?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '50\u202f000 – 75\u202f000 руб.',
#   'title': 'Менеджер по работе с клиентами (БЕЗ ПОИСКА ул. Петра '
#            'Метальникова)'},
#  {'link': 'https://protvino.hh.ru/vacancy/78798593?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '120\u202f000 – 250\u202f000 руб.',
#   'title': 'Менеджер по продажам каркасных деревянных изделий'},
#  {'link': 'https://protvino.hh.ru/vacancy/79681319?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '38\u202f000 – 75\u202f000 руб.',
#   'title': 'Помощник в отдел кадров'},
#  {'link': 'https://protvino.hh.ru/vacancy/73137950?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '45\u202f000 – 60\u202f000 руб.',
#   'title': 'Менеджер по продажам (Петра Метальникова р-он)'},
#  {'link': 'https://protvino.hh.ru/vacancy/79669023?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '80\u202f000 – 110\u202f000 руб.',
#   'title': 'Мастер цеха на производство'},
#  {'link': 'https://protvino.hh.ru/vacancy/78686865?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ' руб.',
#   'title': 'Менеджер по продажам'},
#  {'link': 'https://protvino.hh.ru/vacancy/79447359?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': ' руб.',
#   'title': 'Менеджер по оптовым продажам'},
#  {'link': 'https://protvino.hh.ru/vacancy/78881761?from=vacancy_search_list&query=%D0%9F%D0%B5%D1%82%D1%8F',
#   'salary': '50\u202f000 – 110\u202f000 руб.',
#   'title': 'Менеджер по продажам'}]
