import os
import sys
import winshell
from win32com.client import Dispatch

def create_startup_shortcut():
    try:
        # Путь к папке автозагрузки
        startup_folder = winshell.startup()
        
        # Путь к BAT файлу
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_path = os.path.join(script_dir, "start_auth.bat")
        
        # Создаем ярлык
        shortcut_path = os.path.join(startup_folder, "SystemAuth.lnk")
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = bat_path
        shortcut.WorkingDirectory = script_dir
        shortcut.IconLocation = bat_path
        shortcut.save()
        
        print(f"✅ Ярлык создан: {shortcut_path}")
        print("🔒 Перезагрузите компьютер для проверки")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    create_startup_shortcut()
