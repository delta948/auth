import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import sys
import json
import ctypes
import subprocess
from tkinter import Canvas
from kyrgyzstan_symbols import create_symbols_frame, create_big_emblem_frame

class ScreenLocker:
    def __init__(self):
        self.cfg = self.load_config()
        self.code = None
        self.code_generated_at = None
        self.code_validity_seconds = 30
        self.authenticated = False
        
        # Создаем полноэкранное окно с красивым фоном
        self.root = tk.Tk()
        self.root.title("Системалык аутентификация керек")
        
        # Полноэкранный режим поверх всех окон
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#0a0e27')
        
        # Блокируем Alt+Tab, Ctrl+Alt+Delete
        self.root.bind('<Alt-Tab>', lambda e: None)
        self.root.bind('<Control-Alt-Delete>', lambda e: None)
        
        # Создаем градиентный фон
        self.create_gradient_background()
        
        self.setup_ui()
        
        # Отключаем менеджер задач
        self.disable_task_manager()
        
    def create_gradient_background(self):
        """Создает красивый градиентный фон"""
        self.canvas = Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Получаем размеры экрана
        self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Создаем градиент от темно-синего к черному
        for i in range(height):
            # Градиент от #0a0e27 до #000000
            ratio = i / height
            r = int(10 * (1 - ratio))
            g = int(14 * (1 - ratio))
            b = int(39 * (1 - ratio))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, width=1)
        
        # Добавляем декоративные элементы
        self.add_decorative_elements()
    
    def add_decorative_elements(self):
        """Добавляет декоративные элементы на фон"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Добавляем кружки с анимацией
        self.circles = []
        for _ in range(20):
            x = width // 2 + (hash(_) % 400 - 200)
            y = height // 2 + (hash(_ * 2) % 300 - 150)
            size = 2 + (hash(_ * 3) % 4)
            circle = self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill='#ffffff', outline='', stipple='gray50'
            )
            self.circles.append(circle)
        
        # Анимация кружков
        self.animate_circles()
    
    def animate_circles(self):
        """Анимирует декоративные кружки"""
        if hasattr(self, 'canvas'):
            import random
            for circle in self.circles:
                # Случайное перемещение
                coords = self.canvas.coords(circle)
                if coords:
                    new_x = coords[0] + random.randint(-1, 1)
                    new_y = coords[1] + random.randint(-1, 1)
                    size = (coords[2] - coords[0]) / 2
                    self.canvas.coords(circle, new_x, new_y, new_x + size*2, new_y + size*2)
            
            self.root.after(100, self.animate_circles)
    
    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def disable_task_manager(self):
        try:
            # Блокируем диспетчер задач через реестр
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except:
            pass
    
    def enable_task_manager(self):
        try:
            # Включаем обратно диспетчер задач
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 
                               0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "DisableTaskMgr")
            winreg.CloseKey(key)
        except:
            pass
    
    def setup_ui(self):
        # Создаем главный контейнер
        main_frame = tk.Frame(self.root, bg='#0a0e27')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Логотип иконка замка
        self.create_lock_icon(main_frame)
        
        # Заголовок с эффектом свечения
        title = tk.Label(main_frame, text="🔒 СИСТЕМА БЛОКТОЛДУ", 
                        fg='#00ffcc', bg='#0a0e27', 
                        font=('Arial Bold', 36))
        title.pack(pady=(20, 10))
        
        # Подзаголовок
        subtitle = tk.Label(main_frame, 
                           text="Кыргыз Республикасы", 
                           fg='#666699', bg='#0a0e27', 
                           font=('Arial Bold', 14))
        subtitle.pack(pady=(0, 30))
        
        # Инструкция в красивой рамке
        instruction_frame = tk.Frame(main_frame, bg='#1a1e3a', relief='ridge', bd=2)
        instruction_frame.pack(pady=20, padx=20, fill='x')
        
        instruction = tk.Label(instruction_frame, 
                             text="Системаны бошотуу үчүн электрондук почтаңызга\nжөнөтүлгөн 6 орундуу кодду киргизиңиз", 
                             fg='#ffffff', bg='#1a1e3a', 
                             font=('Arial', 16), justify='center')
        instruction.pack(pady=20, padx=30)
        
        # Поле для ввода кода с красивым стилем
        self.code_entry = tk.Entry(main_frame, font=('Arial', 28), 
                                 justify='center', width=12,
                                 bg='#2a2e4a', fg='#00ffcc',
                                 insertbackground='#00ffcc',
                                 relief='flat', bd=0)
        self.code_entry.pack(pady=20)
        
        # Добавляем рамку вокруг поля ввода
        entry_frame = tk.Frame(main_frame, bg='#00ffcc', relief='flat', bd=2)
        entry_frame.place(relx=0.5, rely=0.58, anchor='center', width=320, height=60)
        entry_frame.tkraise()
        self.code_entry.tkraise()
        
        self.code_entry.focus()
        
        # Кнопки в красивом стиле
        button_frame = tk.Frame(main_frame, bg='#0a0e27')
        button_frame.pack(pady=20)
        
        send_btn = tk.Button(button_frame, text="📧 Кодду почтага жөнөтүү", 
                           command=self.send_code,
                           font=('Arial', 14, 'bold'), 
                           bg='#0066cc', fg='white',
                           activebackground='#0088ff',
                           activeforeground='white',
                           relief='flat', bd=0,
                           padx=30, pady=15,
                           cursor='hand2')
        send_btn.pack(side='left', padx=10)
        
        unlock_btn = tk.Button(button_frame, text="🔓 Бошотуу", 
                             command=self.verify_code,
                             font=('Arial', 16, 'bold'), 
                             bg='#00cc66', fg='white',
                             activebackground='#00ff88',
                             activeforeground='white',
                             relief='flat', bd=0,
                             padx=30, pady=15,
                             cursor='hand2')
        unlock_btn.pack(side='left', padx=10)
        
        # Статус с анимацией
        self.status_label = tk.Label(main_frame, 
                                    text="📧 Кодду алуу үчүн 'Кодду почтага жөнөтүү' басыңыз", 
                                    fg='#ffcc00', bg='#0a0e27', 
                                    font=('Arial', 14))
        self.status_label.pack(pady=20)
        
        # Информация о почте
        info_frame = tk.Frame(main_frame, bg='#1a1e3a', relief='flat', bd=1)
        info_frame.pack(pady=10, padx=20, fill='x')
        
        info = tk.Label(info_frame, 
                       text=f"📩 Электрондук почта: {self.cfg.get('recipient_email', 'Конфигурацияланган эмес')}", 
                       fg='#8888cc', bg='#1a1e3a', 
                       font=('Arial', 11))
        info.pack(pady=10)
        
        # Время
        self.time_label = tk.Label(main_frame, 
                                  text="", 
                                  fg='#666699', bg='#0a0e27', 
                                  font=('Arial', 10))
        self.time_label.pack(pady=5)
        self.update_time()
        
        # Большие символы Кыргызстана внизу (только герб по центру)
        bottom_symbols_frame = tk.Frame(main_frame, bg='#0a0e27')
        bottom_symbols_frame.pack(pady=20)
        
        # Только большой герб (реальное изображение) в центре
        big_emblem_frame = create_big_emblem_frame(bottom_symbols_frame)
        big_emblem_frame.pack()
        
        # Bind Enter key
        self.code_entry.bind('<Return>', lambda e: self.verify_code())
        # Bind Escape key
        self.root.bind('<Escape>', lambda e: None)
    
    def create_lock_icon(self, parent):
        """Создает красивую иконку замка"""
        icon_canvas = Canvas(parent, width=80, height=80, bg='#0a0e27', highlightthickness=0)
        icon_canvas.pack(pady=10)
        
        # Рисуем замок
        # Корпус замка
        icon_canvas.create_rectangle(20, 40, 60, 70, fill='#00ffcc', outline='#00ffcc', width=2)
        # Дужка замка
        icon_canvas.create_arc(20, 25, 60, 55, start=0, extent=180, 
                              style='arc', outline='#00ffcc', width=3)
        # Ключевое отверстие
        icon_canvas.create_oval(38, 50, 42, 54, fill='#0a0e27', outline='#0a0e27')
        icon_canvas.create_rectangle(38, 54, 42, 62, fill='#0a0e27', outline='#0a0e27')
    
    def update_time(self):
        """Обновляет время"""
        if hasattr(self, 'time_label'):
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%d.%m.%Y")
            self.time_label.config(text=f"🕐 {current_time} | 📅 {current_date}")
            self.root.after(1000, self.update_time)
    
    def send_code(self):
        self.status_label.config(text="Код жөнөтүлүүдө...", fg='#ffff00')
        
        # Импортируем функции из two_factor.py
        sys.path.append(os.path.dirname(__file__))
        from two_factor import generate_code, send_code_via_email
        
        self.code = generate_code()
        self.code_generated_at = time.time()
        
        def send_thread():
            try:
                send_code_via_email(self.cfg, self.code)
                self.status_label.config(text="Код жөнөтүлдү! Почтаңызды текшериңиз", fg='#00ff00')
                # Запускаем таймер обратного отсчета
                self.start_countdown()
            except Exception as e:
                self.status_label.config(text=f"Ката: {e}", fg='#ff0000')
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def start_countdown(self):
        """Запускает обратный отсчет времени действия кода"""
        def update_countdown():
            if self.code_generated_at is None:
                return
            
            elapsed = time.time() - self.code_generated_at
            remaining = max(0, self.code_validity_seconds - int(elapsed))
            
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                if minutes > 0:
                    time_text = f"⏰ Коддуңуз жашайт: {minutes}м {seconds}с"
                else:
                    time_text = f"⏰ Коддуңуз жашайт: {seconds} секунд"
                
                self.status_label.config(text=time_text, fg='#00ff00')
                self.root.after(1000, update_countdown)
            else:
                # Время истекло
                self.code = None
                self.code_generated_at = None
                self.status_label.config(text="⏰ Коддуңуз мөөнөтү өттү! Кайра жөнөтүңүз.", fg='#ff0000')
                self.code_entry.delete(0, tk.END)
        
        update_countdown()
    
    def verify_code(self):
        entered_code = self.code_entry.get().strip()
        
        if not self.code:
            messagebox.showerror("Ката", "Алгач кодду жөнөтүңүз!")
            return
        
        # Проверяем, не истекло ли время действия кода
        if self.code_generated_at is not None:
            elapsed = time.time() - self.code_generated_at
            if elapsed > self.code_validity_seconds:
                messagebox.showerror("Код мөөнөтү өттү", "Коддуңуз мөөнөтү өттү! Кайра жөнөтүңүз.")
                self.code = None
                self.code_generated_at = None
                self.code_entry.delete(0, tk.END)
                self.status_label.config(text="⏰ Коддуңуз мөөнөтү өттү! Кайра жөнөтүңүз.", fg='#ff0000')
                return
        
        if entered_code == self.code:
            self.authenticated = True
            self.status_label.config(text="Аутентификация ийгиликтүү! Бошотуу...", fg='#00ff00')
            self.enable_task_manager()
            time.sleep(2)
            self.root.destroy()
        else:
            self.status_label.config(text="Код туура эмес! Кайра аракет кылыңыз", fg='#ff0000')
            self.code_entry.delete(0, tk.END)
            messagebox.showerror("Кирүүгө тыюу салынды", "Аутентификация коду туура эмес!")
    
    def run(self):
        # Центрируем окно
        self.root.mainloop()
        return self.authenticated

if __name__ == "__main__":
    locker = ScreenLocker()
    success = locker.run()
    
    if not success:
        # Если аутентификация не пройдена, блокируем снова
        ctypes.windll.user32.LockWorkStation()
