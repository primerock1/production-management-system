# Проект учебной практики - Система управления производством

## Описание проекта

Система управления производством включает базу данных SQLite и REST API для работы с данными производства. Проект состоит из скриптов для создания БД, импорта данных из Excel файлов и веб-API для управления данными.

## Выполненные задачи

### 1. База данных SQLite
База данных создана с 5 взаимосвязанными таблицами:
- `material_type` - Типы материалов (4 записи)
- `product_type` - Типы продукции (6 записей)  
- `workshops` - Цеха производства (12 записей)
- `products` - Продукция (20 записей)
- `product_workshops` - Связь продукции и цехов (130 записей)

**Файл БД:** `production_db.sqlite`

### 2. Импорт данных из Excel
Автоматический импорт данных из 5 Excel файлов:
- `Material_type_import.xlsx` → material_type
- `Product_type_import.xlsx` → product_type  
- `Workshops_import.xlsx` → workshops
- `Products_import.xlsx` → products
- `Product_workshops_import.xlsx` → product_workshops

**Всего импортировано:** 172 записи

### 3. ER-диаграмма
Автоматически сгенерированная ER-диаграмма с визуализацией структуры БД и связей между таблицами.

**Файл:** `ER_diagram.pdf`

### 4. REST API (FastAPI)
Веб-API для управления данными производства с полным CRUD функционалом:
- **Material Types API** - управление типами материалов
- **Product Types API** - управление типами продукции
- **Workshops API** - управление цехами
- **Products API** - управление продукцией
- **Product Workshops API** - управление связями продукции и цехов

## Структура проекта

```
УП-1/
├── backend/                      # FastAPI приложение
│   └── app/
│       ├── main.py              # Главный файл приложения
│       ├── config.py            # Конфигурация
│       ├── database.py          # Подключение к БД
│       ├── models/              # SQLAlchemy модели
│       ├── schemas/             # Pydantic схемы
│       └── routers/             # API роутеры
├── production_db.sqlite          # База данных SQLite
├── ER_diagram.pdf               # ER-диаграмма
├── create_database.py           # Скрипт создания БД и импорта данных
├── create_er_diagram.py         # Скрипт создания ER-диаграммы
├── Resources/
│   ├── xlsx/                    # Исходные Excel файлы для импорта
│   └── *.pdf, *.docx           # Документация проекта
├── ПОЯСНЕНИЯ_ПО_БД_СКРИПТАМ.md  # Подробные пояснения по скриптам БД
└── ПОЯСНЕНИЯ_ПО_КОДУ.md         # Подробные пояснения по коду API
```

## Использование

### 1. Работа с базой данных

#### Пересоздание базы данных
```bash
python create_database.py
```

#### Создание ER-диаграммы
```bash
python create_er_diagram.py
```

### 2. Запуск REST API

#### Установка зависимостей
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings
```

#### Запуск сервера разработки
```bash
cd backend
python run.py
```

API будет доступно по адресу: `http://localhost:8000`

#### Документация API
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. API Endpoints

#### Material Types (Типы материалов)
- `GET /api/material-types` - получить все типы материалов
- `GET /api/material-types/{id}` - получить тип материала по ID
- `POST /api/material-types` - создать новый тип материала

#### Product Types (Типы продукции)
- `GET /api/product-types` - получить все типы продукции
- `GET /api/product-types/{id}` - получить тип продукции по ID
- `POST /api/product-types` - создать новый тип продукции

#### Workshops (Цеха)
- `GET /api/workshops` - получить все цеха
- `GET /api/workshops/{id}` - получить цех по ID
- `POST /api/workshops` - создать новый цех

#### Products (Продукция)
- `GET /api/products` - получить всю продукцию
- `GET /api/products/{id}` - получить продукцию по ID
- `POST /api/products` - создать новую продукцию

#### Product Workshops (Связи продукции и цехов)
- `GET /api/product-workshops` - получить все связи
- `GET /api/product-workshops/{id}` - получить связь по ID
- `POST /api/product-workshops` - создать новую связь

## Требования

### Для работы с базой данных
- Python 3.8+
- pandas
- openpyxl  
- Pillow
- reportlab
- matplotlib

```bash
pip install pandas openpyxl pillow reportlab matplotlib
```

### Для REST API
- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings
```

## Статистика данных

| Таблица | Записей | Описание |
|---------|---------|----------|
| material_type | 4 | Типы материалов с процентом потерь |
| product_type | 6 | Типы продукции с коэффициентами |
| workshops | 12 | Цеха с информацией о персонале |
| products | 20 | Продукция с артикулами и ценами |
| product_workshops | 130 | Связи продукции и цехов с временем производства |
| **Всего** | **172** | **Общее количество записей** |

## Особенности реализации

### База данных
- **SQLite** - легковесная БД, не требует установки сервера
- **Внешние ключи** - обеспечивают целостность данных
- **Индексы** - ускоряют поиск по ключевым полям
- **Уникальные ограничения** - предотвращают дубликаты

### API
- **FastAPI** - современный, быстрый веб-фреймворк
- **Автоматическая документация** - Swagger UI и ReDoc
- **Валидация данных** - через Pydantic схемы
- **ORM** - SQLAlchemy для работы с БД
- **Dependency Injection** - для управления сессиями БД

### Импорт данных
- **Автоматическое разрешение связей** - поиск ID по именам
- **Обработка ошибок** - продолжение работы при проблемах с отдельными записями
- **Проверка дубликатов** - предотвращение повторного импорта
- **Валидация типов** - корректное преобразование данных из Excel

## Документация

- **ПОЯСНЕНИЯ_ПО_БД_СКРИПТАМ.md** - подробное описание скриптов создания БД
- **ПОЯСНЕНИЯ_ПО_КОДУ.md** - подробное описание кода FastAPI приложения
- **ER_diagram.pdf** - визуальная схема базы данных

## Примеры использования API

### Создание нового типа материала
```bash
curl -X POST "http://localhost:8000/api/material-types" \
     -H "Content-Type: application/json" \
     -d '{"name": "Металл", "loss_percentage": 3.5}'
```

### Получение всех продуктов
```bash
curl "http://localhost:8000/api/products"
```

### Создание связи продукта и цеха
```bash
curl -X POST "http://localhost:8000/api/product-workshops" \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1, "workshop_id": 2, "production_time_hours": 8.5}'
```

