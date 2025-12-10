"""
Скрипт для создания базы данных и импорта данных из Excel файлов
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path

# Создаем базу данных
DB_NAME = 'production_db.sqlite'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("Создание базы данных...")

# Создаем таблицы на основе структуры Excel файлов
# Сначала читаем файлы, чтобы понять структуру
excel_dir = Path('Resources/xlsx')

# 1. Material_type (Типы материалов)
cursor.execute('''
CREATE TABLE IF NOT EXISTS material_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    loss_percentage REAL
)
''')

# 2. Product_type (Типы продуктов)
cursor.execute('''
CREATE TABLE IF NOT EXISTS product_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    coefficient REAL
)
''')

# 3. Workshops (Цеха)
cursor.execute('''
CREATE TABLE IF NOT EXISTS workshops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    workshop_type TEXT,
    staff_count INTEGER
)
''')

# 4. Products (Продукты)
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product_type_id INTEGER,
    article TEXT,
    min_price REAL,
    main_material TEXT,
    FOREIGN KEY (product_type_id) REFERENCES product_type(id)
)
''')

# 5. Product_workshops (Связь продуктов и цехов)
cursor.execute('''
CREATE TABLE IF NOT EXISTS product_workshops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    workshop_id INTEGER NOT NULL,
    production_time_hours REAL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (workshop_id) REFERENCES workshops(id),
    UNIQUE(product_id, workshop_id)
)
''')

print("Таблицы созданы успешно!")

# Импортируем данные из Excel
print("\nИмпорт данных из Excel файлов...")

try:
    # Импорт Material_type
    if os.path.exists(excel_dir / 'Material_type_import.xlsx'):
        df = pd.read_excel(excel_dir / 'Material_type_import.xlsx')
        print(f"\nMaterial_type: {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO material_type (name, loss_percentage)
                    VALUES (?, ?)
                ''', (str(row['Тип материала']) if pd.notna(row['Тип материала']) else None,
                      float(row['Процент потерь сырья']) if pd.notna(row['Процент потерь сырья']) else None))
            except Exception as e:
                print(f"Ошибка при импорте Material_type: {e}")
    
    # Импорт Product_type
    if os.path.exists(excel_dir / 'Product_type_import.xlsx'):
        df = pd.read_excel(excel_dir / 'Product_type_import.xlsx')
        print(f"\nProduct_type: {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO product_type (name, coefficient)
                    VALUES (?, ?)
                ''', (str(row['Тип продукции']) if pd.notna(row['Тип продукции']) else None,
                      float(row['Коэффициент типа продукции']) if pd.notna(row['Коэффициент типа продукции']) else None))
            except Exception as e:
                print(f"Ошибка при импорте Product_type: {e}")
    
    # Импорт Workshops
    if os.path.exists(excel_dir / 'Workshops_import.xlsx'):
        df = pd.read_excel(excel_dir / 'Workshops_import.xlsx')
        print(f"\nWorkshops: {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO workshops (name, workshop_type, staff_count)
                    VALUES (?, ?, ?)
                ''', (str(row['Название цеха']) if pd.notna(row['Название цеха']) else None,
                      str(row['Тип цеха']) if pd.notna(row['Тип цеха']) else None,
                      int(row['Количество человек для производства ']) if pd.notna(row['Количество человек для производства ']) else None))
            except Exception as e:
                print(f"Ошибка при импорте Workshops: {e}")
    
    # Импорт Products
    if os.path.exists(excel_dir / 'Products_import.xlsx'):
        df = pd.read_excel(excel_dir / 'Products_import.xlsx')
        print(f"\nProducts: {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        for _, row in df.iterrows():
            try:
                # Находим product_type_id по имени
                product_type_name = str(row['Тип продукции']) if pd.notna(row['Тип продукции']) else None
                product_type_id = None
                if product_type_name:
                    cursor.execute('SELECT id FROM product_type WHERE name = ?', (product_type_name,))
                    result = cursor.fetchone()
                    product_type_id = result[0] if result else None
                
                cursor.execute('''
                    INSERT OR IGNORE INTO products (name, product_type_id, article, min_price, main_material)
                    VALUES (?, ?, ?, ?, ?)
                ''', (str(row['Наименование продукции']) if pd.notna(row['Наименование продукции']) else None,
                      product_type_id,
                      str(row['Артикул']) if pd.notna(row['Артикул']) else None,
                      float(row['Минимальная стоимость для партнера']) if pd.notna(row['Минимальная стоимость для партнера']) else None,
                      str(row['Основной материал']) if pd.notna(row['Основной материал']) else None))
            except Exception as e:
                print(f"Ошибка при импорте Products: {e}")
    
    # Импорт Product_workshops
    if os.path.exists(excel_dir / 'Product_workshops_import.xlsx'):
        df = pd.read_excel(excel_dir / 'Product_workshops_import.xlsx')
        print(f"\nProduct_workshops: {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        imported_count = 0
        for _, row in df.iterrows():
            try:
                # Находим product_id и workshop_id по именам
                product_name = str(row['Наименование продукции']) if pd.notna(row['Наименование продукции']) else None
                workshop_name = str(row['Название цеха']) if pd.notna(row['Название цеха']) else None
                
                product_id = None
                workshop_id = None
                
                if product_name:
                    cursor.execute('SELECT id FROM products WHERE name = ?', (product_name,))
                    result = cursor.fetchone()
                    product_id = result[0] if result else None
                
                if workshop_name:
                    cursor.execute('SELECT id FROM workshops WHERE name = ?', (workshop_name,))
                    result = cursor.fetchone()
                    workshop_id = result[0] if result else None
                
                if product_id and workshop_id:
                    cursor.execute('''
                        INSERT OR IGNORE INTO product_workshops (product_id, workshop_id, production_time_hours)
                        VALUES (?, ?, ?)
                    ''', (product_id, workshop_id,
                          float(row['Время изготовления, ч']) if pd.notna(row['Время изготовления, ч']) else None))
                    imported_count += 1
                else:
                    if not product_id:
                        print(f"  Предупреждение: продукт '{product_name}' не найден")
                    if not workshop_id:
                        print(f"  Предупреждение: цех '{workshop_name}' не найден")
            except Exception as e:
                print(f"Ошибка при импорте Product_workshops: {e}")
        print(f"  Импортировано записей: {imported_count}")
    
    conn.commit()
    print("\nДанные успешно импортированы!")
    
    # Выводим статистику
    print("\n" + "="*60)
    print("Статистика базы данных:")
    print("="*60)
    for table in ['material_type', 'product_type', 'workshops', 'products', 'product_workshops']:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"{table}: {count} записей")
    
except Exception as e:
    print(f"Ошибка при импорте: {e}")
    import traceback
    traceback.print_exc()

finally:
    conn.close()
    print(f"\nБаза данных сохранена в файл: {DB_NAME}")

