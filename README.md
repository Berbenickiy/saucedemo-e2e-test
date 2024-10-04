Сначала необходимо склонировать репозиторий с GitHub на ваш локальный компьютер.

Откройте терминал или командную строку.

Перейдите в директорию, куда хотите клонировать проект.

cd путь/до/вашей/папки
git clone https://github.com/ваш_пользователь/saucedemo-e2e-test.git
Замените "ваш_пользователь" на ваше имя пользователя на GitHub

Перейдите в директорию проекта:
cd saucedemo-e2e-test



Создайте и Активируйте Виртуальное Окружение
Windows PowerShell
python -m venv venv
venv\Scripts\activate

Установите Зависимости
pip install -r requirements.txt

Запустите Тест
python tests/test_purchase.py
