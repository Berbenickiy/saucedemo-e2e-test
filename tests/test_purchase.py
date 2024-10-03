import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SauceDemoPurchaseTest(unittest.TestCase):
    def setUp(self):
        # Укажите путь к chromedriver, если он не в PATH
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)  # Неявные ожидания

        # Тестовые данные
        self.base_url = "https://www.saucedemo.com/"
        self.username = "standard_user"
        self.password = "secret_sauce"
        self.product_name = "Sauce Labs Backpack"

    def test_purchase_flow(self):
        driver = self.driver
        driver.get(self.base_url)

        # Авторизация
        driver.find_element(By.ID, "user-name").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()

        # Проверка успешной авторизации
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            print("Авторизация прошла успешно.")
        except TimeoutException:
            self.fail("Авторизация не удалась.")

        # Выбор товара
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        product_found = False
        for product in products:
            title = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            if title == self.product_name:
                product.find_element(By.TAG_NAME, "button").click()
                product_found = True
                print(f"Товар '{self.product_name}' добавлен в корзину.")
                break

        if not product_found:
            self.fail(f"Товар '{self.product_name}' не найден.")

        # Переход в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Проверка добавления товара в корзину
        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "inventory_item_name"), self.product_name
                )
            )
            print("Товар успешно добавлен в корзину.")
        except TimeoutException:
            self.fail("Товар не отображается в корзине.")

        # Оформление покупки
        driver.find_element(By.ID, "checkout").click()

        # Заполнение данных покупателя
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        # Проверка на странице обзора заказа
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "summary_info"))
            )
            print("Находится на странице обзора заказа.")
        except TimeoutException:
            self.fail("Не удалось перейти на страницу обзора заказа.")

        # Завершение покупки
        driver.find_element(By.ID, "finish").click()

        # Проверка успешного завершения покупки
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
            )
            success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
            self.assertEqual(success_message, "Thank you for your order!")
            print("Покупка завершена успешно.")
        except TimeoutException:
            self.fail("Покупка не была завершена успешно.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
