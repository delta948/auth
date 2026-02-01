import os
import ctypes
import sys

def lock_system():
    """Блокирует рабочую станцию Windows"""
    try:
        # Используем Windows API для блокировки
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception as e:
        print(f"Ошибка блокировки: {e}")
        # Альтернативный метод
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return False

if __name__ == "__main__":
    lock_system()
