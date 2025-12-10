# Инструкция по работе с Git и GitHub

## Пошаговое руководство по загрузке проекта на GitHub

### 1. Подготовка проекта

#### Создание .gitignore файла
Создайте файл `.gitignore` в корне проекта для исключения ненужных файлов:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
```

### 2. Инициализация Git репозитория

#### Откройте терминал в папке проекта и выполните:

```bash
# Инициализация Git репозитория
git init

# Добавление всех файлов в индекс
git add .

# Первый коммит
git commit -m "Initial commit: Production Management System

- Создана база данных SQLite с 5 таблицами
- Реализован импорт данных из Excel файлов  
- Создана ER-диаграмма базы данных
- Разработан REST API на FastAPI
- Добавлена документация проекта"
```

### 3. Создание репозитория на GitHub

#### Вариант 1: Через веб-интерфейс GitHub
1. Зайдите на [github.com](https://github.com)
2. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните форму:
   - **Repository name:** `production-management-system`
   - **Description:** `Система управления производством с базой данных SQLite и REST API`
   - **Visibility:** Public или Private (на ваш выбор)
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license"
4. Нажмите **"Create repository"**

#### Вариант 2: Через GitHub CLI (если установлен)
```bash
gh repo create production-management-system --public --description "Система управления производством с базой данных SQLite и REST API"
```

### 4. Подключение локального репозитория к GitHub

```bash
# Добавление удаленного репозитория
git remote add origin https://github.com/ВАШ_USERNAME/production-management-system.git

# Проверка подключения
git remote -v

# Отправка кода на GitHub
git push -u origin main
```

**Примечание:** Замените `ВАШ_USERNAME` на ваш реальный username на GitHub.

### 5. Дальнейшая работа с проектом

#### Добавление новых изменений
```bash
# Проверка статуса файлов
git status

# Добавление измененных файлов
git add .
# или добавление конкретного файла
git add имя_файла.py

# Создание коммита с описанием изменений
git commit -m "Описание изменений"

# Отправка изменений на GitHub
git push
```

#### Примеры хороших сообщений коммитов
```bash
git commit -m "Add new API endpoint for material statistics"
git commit -m "Fix database connection error handling"
git commit -m "Update README with installation instructions"
git commit -m "Refactor product model validation"
```

### 6. Структура коммитов для вашего проекта

#### Рекомендуемая последовательность коммитов:

```bash
# 1. Базовая структура
git add create_database.py create_er_diagram.py production_db.sqlite
git commit -m "Add database creation and ER diagram scripts"

# 2. Данные и ресурсы
git add Resources/ ER_diagram.pdf
git commit -m "Add Excel data files and generated ER diagram"

# 3. Backend API
git add backend/
git commit -m "Add FastAPI backend with CRUD operations"

# 4. Документация
git add README.md ПОЯСНЕНИЯ_ПО_БД_СКРИПТАМ.md ПОЯСНЕНИЯ_ПО_КОДУ.md
git commit -m "Add comprehensive project documentation"

# 5. Отчеты (если нужно)
git add Отчёты/
git commit -m "Add project reports and documentation"

# Отправка всех коммитов
git push
```

### 7. Полезные Git команды

#### Просмотр истории
```bash
# Просмотр истории коммитов
git log --oneline

# Просмотр изменений в файлах
git diff

# Просмотр статуса репозитория
git status
```

#### Отмена изменений
```bash
# Отмена изменений в файле (до добавления в индекс)
git checkout -- имя_файла.py

# Отмена добавления файла в индекс
git reset HEAD имя_файла.py

# Отмена последнего коммита (сохраняя изменения)
git reset --soft HEAD~1
```

#### Работа с ветками
```bash
# Создание новой ветки
git branch feature/new-functionality

# Переключение на ветку
git checkout feature/new-functionality

# Создание и переключение одной командой
git checkout -b feature/new-functionality

# Слияние ветки с main
git checkout main
git merge feature/new-functionality
```

### 8. Настройка Git (если не настроен)

```bash
# Настройка имени пользователя
git config --global user.name "Ваше Имя"

# Настройка email
git config --global user.email "ваш_email@example.com"

# Проверка настроек
git config --list
```

### 9. Аутентификация на GitHub

#### Вариант 1: Personal Access Token (рекомендуется)
1. Зайдите в GitHub → Settings → Developer settings → Personal access tokens
2. Создайте новый token с правами на репозитории
3. Используйте token вместо пароля при push

#### Вариант 2: SSH ключи
```bash
# Генерация SSH ключа
ssh-keygen -t ed25519 -C "ваш_email@example.com"

# Добавление ключа в ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Копирование публичного ключа
cat ~/.ssh/id_ed25519.pub

# Добавьте этот ключ в GitHub → Settings → SSH and GPG keys
```

### 10. Проверка успешной загрузки

После выполнения `git push` проверьте:
1. Зайдите на страницу вашего репозитория на GitHub
2. Убедитесь, что все файлы загружены
3. Проверьте, что README.md отображается корректно
4. Убедитесь, что структура папок сохранилась

### 11. Дополнительные рекомендации

#### Для учебного проекта добавьте теги:
```bash
# Создание тега для версии
git tag -a v1.0 -m "Версия 1.0: Завершенный проект учебной практики"
git push origin v1.0
```

#### Создание Release на GitHub:
1. Зайдите в репозиторий на GitHub
2. Перейдите в раздел "Releases"
3. Нажмите "Create a new release"
4. Выберите тег v1.0
5. Добавьте описание релиза
6. Опубликуйте релиз

### 12. Возможные проблемы и решения

#### Ошибка "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/ВАШ_USERNAME/production-management-system.git
```

#### Ошибка аутентификации
- Убедитесь, что используете правильный username и token/пароль
- Проверьте настройки Git: `git config --list`

#### Конфликты при push
```bash
# Получение изменений с сервера
git pull origin main

# Разрешение конфликтов и повторный push
git push
```

---

## Быстрый старт (краткая версия)

```bash
# 1. Инициализация
git init
git add .
git commit -m "Initial commit: Production Management System"

# 2. Подключение к GitHub (создайте репозиторий на github.com)
git remote add origin https://github.com/ВАШ_USERNAME/production-management-system.git

# 3. Отправка
git push -u origin main
```

**Готово!** Ваш проект теперь на GitHub и доступен по ссылке:
`https://github.com/ВАШ_USERNAME/production-management-system`