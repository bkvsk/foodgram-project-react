## Foodgram - сервис для публикации рецептов

Проект *Foodgram* позволяет пользователям 
публиковать рецепты, добавлять рецепты в избранное 
и список покупок, подписыватся на других пользователей 
и скачивать список продуктов.

### Проект доступен по адрессу:

178.154.231.48

### Доступ в админку для суперюзера:

login - admin@admin.com
pass - admin321

### Технологии

- Python
- Django
- Docker
- postgresql
- nginx
- gunicorn

### Запуск проекта на сервере

Для работы сервиса на сервере должны быть установлены *Docker* и *docker-compose*

Клонируйте репозиторий командой:

``` git clone https://github.com/bkvsk/foodgram-project-react.git ``` 

Перейдите в каталог командой:

``` cd foodgram-project-react/infra/ ``` 

Выполните команду для запуска контейнера:

``` docker-compose up -d ```

Выполните миграции:

``` docker-compose exec backend python manage.py makemigrations --noinput ```

``` docker-compose exec backend python manage.py migrate --noinput ```

Команда для сбора статики:

``` docker-compose exec backend python manage.py collectstatic --no-input ```

Команда для создания суперпользователя:

``` docker-compose exec backend python manage.py createsuperuser ```

Команда для подгрузки ингредиентов:

``` docker-compose exec backend python manage.py load_ingredients ```
