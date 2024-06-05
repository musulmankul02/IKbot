1) команда
        ```python -m venv venv```

2) Активация venv
        ```venv\Scripts\activate```

3) установление биб
        ```pip install -r requirement.txt```

4) прогоняем миграцию
        ```python manage.py makemigrations```
        ```python manage.py migrate```

5) запуск проекта
        ```python manage.py runserver ``` для того чтобы запустить Django проект
        ```python manage.py runbot ``` для того чтобы запустить телеграм бот