# NewsHub (Django)

Новостной сайт в стиле Habr с системой ролей, модерацией, рейтингами и избранным.

## 🚀 Быстрый запуск

### 1. Клонирование и установка
```bash
git clone https://github.com/JUSTCOCONUTMILK/DJAPROJ.git
cd DJAPROJ
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
python manage.py migrate
python manage.py init_admin
python manage.py runserver
```

### 3. Доступ к проекту
- **Сайт:** http://127.0.0.1:8000
- **Админ-панель:** http://127.0.0.1:8000/admin
- **Логин:** `admin`
- **Пароль:** `admin123`

## 👥 Система ролей

- **Супер-админ:** полный контроль над системой
- **Админ:** модерация статей, управление пользователями
- **Пользователь:** создание и редактирование своих статей
- **Гость:** просмотр опубликованных материалов

## 📝 Функционал

### Статьи
- Создание, редактирование, удаление
- Система модерации
- Рейтинги (1-5 звезд)
- Избранное
- Фильтрация по категориям

### Категории
- Backend
- Frontend  
- Machine Learning
- Cyber Security
- Cyber Sport
- Game Development

### Пользователи
- Регистрация и авторизация
- Профили пользователей
- Блокировка
- Статистика публикаций

## 🛠 Технологии

- **Backend:** Django 6.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **Styling:** Custom CSS с темной темой

## 📁 Структура проекта

```
DJAPROJ/
├── articles/          # Приложение статей
├── users/             # Приложение пользователей
├── config/            # Настройки Django
├── templates/         # HTML шаблоны
├── static/            # CSS и статические файлы
├── manage.py          # Управление проектом
└── requirements.txt   # Зависимости
```

## 🔧 Дополнительные команды

```bash
# Создание суперпользователя
python manage.py createsuperuser

# Инициализация категорий
python manage.py init_categories

# Сброс базы данных
python manage.py flush
```

## 📝 Лицензия

MIT License - свободное использование и модификация.
