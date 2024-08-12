# Time tracker - console app
Позволяет выставлять цель на определённый промежуток времени и отслеживать активности, как в процентах, так и в временном количестве. 
Отлично подходит для отслеживания своего времени и анализа затраченного времени одной активности, относительно другой.

![prev](https://github.com/MaximGit1/Activity-tracker/blob/main/other-files/readme-config/example.jpg)

## Первичные настройки
При первом запуске нужно зайти в бд и создать активности:
Название - любое название
Цвет - из таблицы цветов
![colors](https://github.com/MaximGit1/Activity-tracker/blob/main/other-files/readme-config/%D1%86%D0%B2%D0%B5%D1%82%D0%B0.png)

В файле ```config.py``` можно настроить некоторые критерии:

    ```goal: int = 2 * (3600 * 6)  # 12 hours a week
    min_time: int = (5 * 60)  # minimum time for plotting (5 minute)
    save_path = BASE_DIR / 'fig'  # path of preservation graphics
    min_percentage: int = 1  # the minimum percentage for calculations and plotting
    max_activities: int = 13  # maximum number of activities. Recommended value 13-15
    max_title_len: int = 12 
    table_name: str = 'activities'  # db name``` 
Наиболее интересные параметры:
1. goal - цель на промежуток времени
2. save_path - путь, где будет находится папка "fig", где будут хранится результаты (Название результатов, можно будет изменить в следующем обновлении)
   
Остальные настройки и недостоющие функции будут доступны при обновлении.

## Запуск
1. git clone link
2. Запустить нужный файл: py/py3 .\Activity-tracker\main.py
3. Закрыть консоль и сделать первичную настройку
4. Пользоваться трекером (Осторожно, нет проверок на вводимые типы в консоль)
5. Можно создать активатор скрипта, например, start.bat -- файл будет хранить команду для запуска скрипта (2 пункт) (для windows)

