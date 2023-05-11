import json
import requests
from bs4 import BeautifulSoup as bs

vacancy = input("Введите профессию: ").lower()

data_list = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

"""
Парсим hh.ru
"""
for number in range(1, 3):
    url = f"https://spb.hh.ru/search/vacancy?text={vacancy}&area={number}"
    response = requests.get(url, headers=headers)
    soup = bs(response.text, "html.parser")

    vac_item_list_hh = list(
        soup.find_all("div", {"class": "vacancy-serp-item-body__main-info"})
    )

    for item in vac_item_list_hh:
        temp_dict = {}

        temp_dict["title"] = item.find("a", {"class": "serp-item__title"}).text
        temp_dict["link"] = item.find("a", {"class": "serp-item__title"})["href"]
        temp_dict["recruiter"] = item.find(
            "a", {"class": "bloko-link bloko-link_kind-tertiary"}
        ).text.replace("\xa0", " ")
        temp_dict["location"] = item.find(
            "div", {"data-qa": "vacancy-serp__vacancy-address"}
        ).text.replace("\xa0", " ")

        try:
            salary = item.find("span", {"class": "bloko-header-section-3"}).text

            salary = salary.split()

            if salary[0] == "до":
                temp_dict["salary_min"] = None
                temp_dict["salary_max"] = int(f"{salary[1]}{salary[2]}")
                temp_dict["salary_currency"] = salary[3]
            elif salary[0] == "от":
                temp_dict["salary_min"] = int(f"{salary[1]}{salary[2]}")
                temp_dict["salary_max"] = None
                temp_dict["salary_currency"] = salary[3]
            else:
                temp_dict["salary_min"] = int(f"{salary[0]}{salary[1]}")
                temp_dict["salary_max"] = int(f"{salary[3]}{salary[4]}")
                temp_dict["salary_currency"] = salary[5]

            if temp_dict["salary_currency"] == "руб.":
                temp_dict["salary_currency"] = "RUB"
        except AttributeError:
            temp_dict["salary_min"] = None
            temp_dict["salary_max"] = None
            temp_dict["salary_currency"] = None

        temp_dict["source"] = "hh.ru"

        data_list.append(temp_dict)


objs = {"data": data_list}

# записываем полученные данные в json формате
with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(objs, f, indent=4, ensure_ascii=False)
