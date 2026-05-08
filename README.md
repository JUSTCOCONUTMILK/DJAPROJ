# NewsHub (Django)

Проект новостного сайта в стиле Habr с ролями, модерацией, рейтингами и избранным.

## Полный запуск с нуля (Windows + VS Code)

1. Откройте VS Code и папку проекта: `C:\Users\LENOVO\Desktop\django`
2. Откройте встроенный терминал (`Terminal -> New Terminal`)
3. Выполните команды:

```bash
cd C:\Users\LENOVO\Desktop\django
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000
Админка: http://127.0.0.1:8000/admin

### Если `python -m venv .venv` зависает или падает

Это обычно связано с этапом `ensurepip` (установка pip внутри venv). Не прерывайте процесс вручную.

Вариант A (рекомендуется): запустить готовый скрипт:

```powershell
cd C:\Users\LENOVO\Desktop\django
powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1
python manage.py createsuperuser
python manage.py runserver
```

Вариант B (вручную):

```powershell
cd C:\Users\LENOVO\Desktop\django
rmdir /s /q .venv
python -m ensurepip --upgrade
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Проверка критериев

### 1) Users / роли
- **Супер админ (1)**:
  - создается через `createsuperuser`
  - может назначать админов
  - может банить
  - в проекте включено ограничение: **только один superuser**
- **Админ**:
  - `is_staff=True`
  - может создавать/редактировать/удалять статьи
  - может банить пользователей
  - может публиковать статьи на модерации
- **Юзер**:
  - регистрируется через `/accounts/register/`
  - может создавать статьи
  - редактирует/удаляет только свои
- **Гость**:
  - видит только опубликованные статьи

### 2) Register and login
- Регистрация: `/accounts/register/`
- Вход: `/accounts/login/`
- Выход: кнопка "Выйти" в шапке

### 3) Статьи
- Поля: заголовок, картинка, текст, категория
- В карточке и деталке есть: автор, время создания, категория
- Оценка статьи: от 1 до 5
- Рейтинг: среднее арифметическое оценок
- Избранное: добавить/удалить
- Создание/изменение для обычного юзера идет через модерацию (`pending`)
- Публикацию подтверждает админ/супер-админ

### 4) Категории
- Backend
- Frontend
- AI
- Cyber security
- Cyber sport
- Game Development

Категории создаются миграцией `articles/migrations/0002_seed_categories.py`.

### 5) Меню
- Статьи (по времени создания)
- Популярное (рейтинг 4+)
- Категории (фильтр по категории)
- Авторы
- Избранное
