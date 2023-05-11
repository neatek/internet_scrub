import json

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.delivery-club.ru/moscow?shippingType=delivery")
driver.implicitly_wait(15)

actions = ActionChains(driver)

for i in range(500):
    articles = driver.find_elements(By.CLASS_NAME, "PlaceListBduItem_placesListItem")
    control_article = articles[-1]

    # Получение наименований заведений и их рейтинг
    for article in articles:
        try:
            place = article.find_element(
                By.XPATH, ".//h3[contains(@class,'NewPlaceItem_title')]"
            ).text
            rating = article.find_element(
                By.XPATH, ".//span[contains(@class,'AppRating_ratingBlock')]"
            ).text
            if len(place) > 0:
                print(place, rating)
        except Exception:
            continue

    actions.move_to_element(control_article)
    actions.perform()
