import tkinter as tk
from tkinter import Canvas, PhotoImage
import os

def draw_flag(canvas, x, y, width=60, height=40):
    """Рисует флаг Кыргызстана"""
    # Красный фон флага
    canvas.create_rectangle(x, y, x + width, y + height, 
                           fill='#e00025', outline='#e00025')
    
    # Желтый круг в центре
    center_x = x + width // 2
    center_y = y + height // 2
    radius = min(width, height) // 4
    
    canvas.create_oval(center_x - radius, center_y - radius,
                      center_x + radius, center_y + radius,
                      fill='#ffcc00', outline='#ffcc00')
    
    # Солнечные лучи (упрощенная версия)
    import math
    num_rays = 40
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        
        # Внутренний и внешний радиусы лучей
        inner_r = radius * 0.6
        outer_r = radius * 1.3
        
        x1 = center_x + inner_r * math.cos(angle)
        y1 = center_y + inner_r * math.sin(angle)
        x2 = center_x + outer_r * math.cos(angle)
        y2 = center_y + outer_r * math.sin(angle)
        
        canvas.create_line(x1, y1, x2, y2, fill='#ffcc00', width=2)
    
    # Центральный элемент (тундук)
    canvas.create_rectangle(center_x - 3, center_y - 8,
                           center_x + 3, center_y + 8,
                           fill='#e00025', outline='#e00025')

def draw_emblem(canvas, x, y, size=50):
    """Рисует упрощенный герб Кыргызстана"""
    # Синий круг фона
    canvas.create_oval(x - size//2, y - size//2,
                      x + size//2, y + size//2,
                      fill='#0066cc', outline='#0066cc')
    
    # Белые горы (Ала-Тоо)
    mountain_points = [
        x - size//3, y + size//4,
        x - size//6, y - size//6,
        x, y - size//3,
        x + size//6, y - size//6,
        x + size//3, y + size//4
    ]
    canvas.create_polygon(mountain_points, fill='white', outline='white')
    
    # Солнце над горами
    sun_radius = size // 8
    canvas.create_oval(x - sun_radius, y - size//2 - sun_radius,
                      x + sun_radius, y - size//2 + sun_radius,
                      fill='#ffcc00', outline='#ffcc00')
    
    # Орнамент по краям (упрощенный)
    import math
    for i in range(8):
        angle = (2 * math.pi * i) / 8
        ornament_x = x + (size//2 - 5) * math.cos(angle)
        ornament_y = y + (size//2 - 5) * math.sin(angle)
        canvas.create_oval(ornament_x - 2, ornament_y - 2,
                          ornament_x + 2, ornament_y + 2,
                          fill='white', outline='white')

def draw_real_emblem(canvas, x, y, size=80):
    """Рисует реальное изображение герба Кыргызстана"""
    try:
        # Путь к файлу герба
        script_dir = os.path.dirname(os.path.dirname(__file__))
        emblem_path = os.path.join(script_dir, 'Emblem_of_Kyrgyzstan.svg.png')
        
        if os.path.exists(emblem_path):
            # Загружаем изображение
            emblem_img = PhotoImage(file=emblem_path)
            
            # Изменяем размер изображения
            emblem_img = emblem_img.subsample(max(1, emblem_img.width() // size), 
                                            max(1, emblem_img.height() // size))
            
            # Отображаем изображение
            canvas.create_image(x, y, image=emblem_img, anchor='center')
            
            # Сохраняем ссылку на изображение
            canvas.emblem_img = emblem_img
            return True
        else:
            # Если файл не найден, рисуем упрощенную версию
            draw_emblem(canvas, x, y, size//2)
            return False
    except Exception as e:
        # В случае ошибки рисуем упрощенную версию
        draw_emblem(canvas, x, y, size//2)
        return False

def create_symbols_frame(parent):
    """Создает фрейм с символами Кыргызстана"""
    symbols_frame = tk.Frame(parent, bg='#0a0e27')
    
    # Флаг
    flag_canvas = Canvas(symbols_frame, width=60, height=40, 
                        bg='#0a0e27', highlightthickness=0)
    flag_canvas.pack(side='left', padx=5)
    draw_flag(flag_canvas, 0, 0)
    
    # Герб (реальное изображение)
    emblem_canvas = Canvas(symbols_frame, width=80, height=80,
                          bg='#0a0e27', highlightthickness=0)
    emblem_canvas.pack(side='left', padx=5)
    draw_real_emblem(emblem_canvas, 40, 40, 60)
    
    # Флаг (еще один для симметрии)
    flag_canvas2 = Canvas(symbols_frame, width=60, height=40,
                         bg='#0a0e27', highlightthickness=0)
    flag_canvas2.pack(side='left', padx=5)
    draw_flag(flag_canvas2, 0, 0)
    
    return symbols_frame

def create_big_emblem_frame(parent):
    """Создает фрейм с большим гербом"""
    emblem_frame = tk.Frame(parent, bg='#0a0e27')
    
    # Большой герб (реальное изображение)
    big_emblem_canvas = Canvas(emblem_frame, width=150, height=150,
                             bg='#0a0e27', highlightthickness=0)
    big_emblem_canvas.pack()
    draw_real_emblem(big_emblem_canvas, 75, 75, 120)
    
    return emblem_frame
