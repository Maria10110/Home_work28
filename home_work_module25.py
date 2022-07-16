from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pytest

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C://Users/hp/Documents/driverChrome/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('maria.valenbahova@yandex.ru')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('1234567')
   time.sleep(10)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   time.sleep(10)
   pytest.driver.find_element_by_css_selector('div#navbarNav > ul > li > a').click()
   time.sleep(10)


   yield

   pytest.driver.quit()


# проверяем наличие всех питомцев
def test_quantity_of_my_pets():
   pytest.driver.implicitly_wait(10)
   # получаем массив всех моих питомцев
   info_of_my_pets = pytest.driver.find_elements_by_css_selector('div td')
   # получаем имена питомцев
   names = info_of_my_pets[::4]
   # получаем текст с логином, количеством питомцев, друзей и сообщений
   quantity_of_pets_full = WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))).text
   # получаем индекс символа буквы П слова "Питомцев"
   index_pets = quantity_of_pets_full.find('Питомцев')
   # получаем индекс символа буквы Д слова "Друзей"
   index_friends = quantity_of_pets_full.find('Друзей')
   # получаем срез строки от пробела после слова "Питомцев" до начала слова "Друзей"
   quantity_of_pets = quantity_of_pets_full[index_pets + 10:index_friends].replace(' ', '')
   # проверяем, соответствует ли количество питомцев по профилю реальному количеству имен питомцев
   assert int(quantity_of_pets) == len(names)


# проверяем, что фото есть хотя бы у половины питомцев
def test_half_of_the_pets_have_photos():
   # получаем фото питомцев
   images = WebDriverWait(pytest.driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div th > img')))
   count = 0
   # считаем количество фотографи
   for i in range(len(images)):
      if images[i].get_attribute('src'):
         count += 1
   # ставим условие по количеству в зависимости от того, четное или нечетное число фотографий
   if (len(images) % 2) == 0:
      assert count >= (len(images) / 2), 'Фото есть меньше чем у половины питомцев'
   else:
      assert count >= (len(images) / 2 + 1), 'Фото есть меньше чем у половины питомцев'


# проверяем, что у всех питомцев есть имя, вид и возраст.
def test_all_pets_have_name_age_and_type():
   info_of_my_pets = WebDriverWait(pytest.driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
   # получаем имена, виды и возрасты питомцев
   names = info_of_my_pets[::4]
   types = info_of_my_pets[1::4]
   ages = info_of_my_pets[2::4]
   assert '' not in names, 'Не у всех питомцев есть имя'
   # проверяем, что у всех питомцев есть порода
   assert '' not in types, 'Не у всех питомцев есть вид'
   # проверяем, что у всех питомцев есть возраст
   count_noage = 0
   assert '' not in ages, 'Не у всех питомцев есть возраст'


def test_different_names():
   info_of_my_pets = pytest.driver.find_elements_by_css_selector('div td')
   # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
   names = info_of_my_pets[::4]
   types = info_of_my_pets[1::4]
   ages = info_of_my_pets[2::4]
   # проверяем, что у всех питомцев разные имена
   assert len(names) == len(list(set(names))), 'В списке есть питомцы с разными именами'


def test_different_pets():
   info_of_my_pets = pytest.driver.find_elements_by_css_selector('div td')
   # info_of_my_pets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div td')))
   # удаляем из списка лишние элементы
   del info_of_my_pets[::4]
   # группируем каждые три элемента списка питомцев в кортеж (имя,порода,возраст)
   info_of_my_pets_tuple = [tuple(info_of_my_pets[i:i + 3]) for i in range(0, len(info_of_my_pets), 3)]
   # проверяем, есть ли в списке кортежей одинаковые элементы
   assert len(info_of_my_pets_tuple) == len(list(set(info_of_my_pets_tuple))), 'В списке есть повторяющиеся питомцы'






