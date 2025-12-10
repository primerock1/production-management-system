"""
Скрипт для создания профессиональной ER-диаграммы базы данных в формате PDF
"""
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

DB_NAME = 'production_db.sqlite'

# Настройка стиля
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150

try:
    # Подключаемся к БД
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Получаем информацию о таблицах
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Определяем структуру таблиц
    table_info = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        table_info[table] = columns
    
    # Определяем связи (foreign keys)
    relationships = []
    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        fks = cursor.fetchall()
        for fk in fks:
            relationships.append({
                'from_table': table,
                'from_column': fk[3],
                'to_table': fk[2],
                'to_column': fk[4] if fk[4] else 'id'
            })
    
    conn.close()
    
    # Создаем фигуру с большим разрешением
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    
    # Цвета
    header_color = '#2E86AB'
    table_bg = '#F0F8FF'
    border_color = '#1E5A7A'
    pk_color = '#FFD700'
    fk_color = '#FF6B6B'
    text_color = '#000000'
    line_color = '#666666'
    
    # Позиции таблиц (оптимизированы для лучшего расположения)
    table_positions = {
        'material_type': (1.5, 8.5),
        'product_type': (1.5, 6),
        'workshops': (1.5, 3.5),
        'products': (10, 7),
        'product_workshops': (10, 3.5)
    }
    
    # Размеры таблиц
    table_width = 5.5
    header_height = 0.4
    row_height = 0.35
    padding = 0.1
    
    # Рисуем таблицы
    table_boxes = {}
    
    for table_name, (x, y) in table_positions.items():
        if table_name not in table_info:
            continue
        
        columns = table_info[table_name]
        table_height = header_height + len(columns) * row_height
        
        # Сохраняем координаты для связей
        table_boxes[table_name] = {
            'x': x,
            'y': y,
            'width': table_width,
            'height': table_height,
            'center_x': x + table_width / 2,
            'center_y': y + table_height / 2
        }
        
        # Рисуем основную рамку таблицы
        table_box = FancyBboxPatch(
            (x, y), table_width, table_height,
            boxstyle="round,pad=0.02",
            edgecolor=border_color,
            facecolor=table_bg,
            linewidth=2,
            zorder=1
        )
        ax.add_patch(table_box)
        
        # Рисуем заголовок
        header_box = FancyBboxPatch(
            (x, y + table_height - header_height), table_width, header_height,
            boxstyle="round,pad=0.02",
            edgecolor=border_color,
            facecolor=header_color,
            linewidth=2,
            zorder=2
        )
        ax.add_patch(header_box)
        
        # Текст заголовка (с подчеркиванием для разделения слов)
        display_name = table_name.replace('_', ' ').title()
        ax.text(x + table_width/2, y + table_height - header_height/2, 
               display_name, ha='center', va='center', 
               fontsize=11, fontweight='bold', color='white', zorder=3)
        
        # Рисуем колонки
        for i, col in enumerate(columns):
            col_y = y + table_height - header_height - (i + 1) * row_height
            col_name = col[1]
            col_type = col[2]
            
            # Определяем тип колонки
            is_pk = col[5] == 1
            is_fk = any(r['from_table'] == table_name and r['from_column'] == col_name 
                       for r in relationships)
            
            # Цвет фона для PK/FK
            col_bg = 'white'
            if is_pk:
                col_bg = pk_color
            elif is_fk:
                col_bg = fk_color
            
            # Рамка для колонки
            if is_pk or is_fk:
                col_box = FancyBboxPatch(
                    (x + padding, col_y), table_width - 2*padding, row_height,
                    boxstyle="round,pad=0.01",
                    edgecolor=border_color,
                    facecolor=col_bg,
                    linewidth=1,
                    zorder=2,
                    alpha=0.7
                )
                ax.add_patch(col_box)
            
            # Префиксы
            prefix = ""
            if is_pk:
                prefix = "PK: "
            elif is_fk:
                prefix = "FK: "
            
            # Текст колонки
            col_text = f"{prefix}{col_name}"
            type_text = col_type.upper()
            
            # Обрезаем длинные имена типов
            if len(type_text) > 15:
                type_text = type_text[:12] + "..."
            
            ax.text(x + padding + 0.15, col_y + row_height/2, col_text,
                   ha='left', va='center', fontsize=9, 
                   fontweight='bold' if is_pk or is_fk else 'normal',
                   color=text_color, zorder=3)
            
            ax.text(x + table_width - padding - 0.15, col_y + row_height/2, type_text,
                   ha='right', va='center', fontsize=8, style='italic',
                   color='#555555', zorder=3)
            
            # Разделительная линия
            if i < len(columns) - 1:
                ax.plot([x + padding, x + table_width - padding], 
                       [col_y, col_y], 
                       color=line_color, linewidth=0.5, zorder=2, alpha=0.3)
    
    # Рисуем связи между таблицами
    for rel in relationships:
        from_table = rel['from_table']
        to_table = rel['to_table']
        
        if from_table in table_boxes and to_table in table_boxes:
            from_box = table_boxes[from_table]
            to_box = table_boxes[to_table]
            
            # Определяем точки соединения с учетом расположения таблиц
            from_center_x = from_box['center_x']
            from_center_y = from_box['center_y']
            to_center_x = to_box['center_x']
            to_center_y = to_box['center_y']
            
            # Определяем, с какой стороны выходить и входить
            dx = to_center_x - from_center_x
            dy = to_center_y - from_center_y
            
            # Горизонтальное расстояние больше вертикального
            if abs(dx) > abs(dy):
                if dx > 0:  # Целевая таблица справа
                    from_x = from_box['x'] + from_box['width']
                    from_y = from_center_y
                    to_x = to_box['x']
                    to_y = to_center_y
                else:  # Целевая таблица слева
                    from_x = from_box['x']
                    from_y = from_center_y
                    to_x = to_box['x'] + to_box['width']
                    to_y = to_center_y
            else:  # Вертикальное расстояние больше
                if dy > 0:  # Целевая таблица выше
                    from_x = from_center_x
                    from_y = from_box['y'] + from_box['height']
                    to_x = to_center_x
                    to_y = to_box['y']
                else:  # Целевая таблица ниже
                    from_x = from_center_x
                    from_y = from_box['y']
                    to_x = to_center_x
                    to_y = to_box['y'] + to_box['height']
            
            # Рисуем изогнутую стрелку для лучшей читаемости
            arrow = FancyArrowPatch(
                (from_x, from_y), (to_x, to_y),
                arrowstyle='->', mutation_scale=25,
                color=line_color, linewidth=2.5,
                zorder=0, alpha=0.7,
                connectionstyle="arc3,rad=0.2"
            )
            ax.add_patch(arrow)
    
    # Заголовок диаграммы
    ax.text(9, 11, 'ER-диаграмма базы данных производства',
           ha='center', va='center', fontsize=20, fontweight='bold',
           color=text_color)
    
    # Легенда
    legend_elements = [
        mpatches.Patch(color=pk_color, label='Первичный ключ (PK)'),
        mpatches.Patch(color=fk_color, label='Внешний ключ (FK)'),
        mpatches.Patch(color=table_bg, label='Обычное поле')
    ]
    ax.legend(handles=legend_elements, loc='upper right', 
             frameon=True, fancybox=True, shadow=True)
    
    # Сохраняем в PDF с высоким качеством
    pdf_path = 'ER_diagram.pdf'
    plt.tight_layout(pad=1.0)
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight', 
                dpi=300, facecolor='white', edgecolor='none')
    print(f"ER-диаграмма сохранена: {pdf_path}")
    
    plt.close()
    
except Exception as e:
    print(f"Ошибка при создании диаграммы: {e}")
    import traceback
    traceback.print_exc()
