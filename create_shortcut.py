import os
import sys
from pathlib import Path

def create_startup_shortcut():
    try:
        # Путь к папке автозагрузки
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        
        # Путь к BAT файлу
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_path = os.path.join(script_dir, "start_auth.bat")
        
        # Создаем VBS скрипт для создания ярлыка
        vbs_content = f'''
Set oShell = CreateObject("WScript.Shell")
sDesktop = oShell.SpecialFolders("Startup")
Set oLink = oShell.CreateShortcut(sDesktop & "\\SystemAuth.lnk")
oLink.TargetPath = "{bat_path}"
oLink.WorkingDirectory = "{script_dir}"
oLink.Save
'''
        
        vbs_path = os.path.join(script_dir, "create_shortcut.vbs")
        with open(vbs_path, 'w') as f:
            f.write(vbs_content)
        
        # Запускаем VBS скрипт
        os.system(f'cscript //nologo "{vbs_path}"')
        
        # Удаляем временный VBS файл
        os.remove(vbs_path)
        
        print(f"✅ Ярлык создан в папке автозагрузки")
        print(f"📁 Папка автозагрузки: {startup_folder}")
        print("🔒 Перезагрузите компьютер для проверки")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    create_startup_shortcut()
