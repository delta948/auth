import os
import sys
import winreg

def add_to_startup():
    try:
        # Получаем путь к текущему скрипту
        script_path = os.path.abspath(__file__)
        startup_script = os.path.join(os.path.dirname(script_path), "startup.py")
        
        # Добавляем в автозагрузку через реестр
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_SET_VALUE)
        
        winreg.SetValueEx(key, "SystemAuth", 0, winreg.REG_SZ, 
                         f'"{sys.executable}" "{startup_script}"')
        winreg.CloseKey(key)
        
        print("✅ Добавлено в автозагрузку Windows")
        print("🔒 Система будет запрашивать код при каждом включении")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def remove_from_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_SET_VALUE)
        
        winreg.DeleteValue(key, "SystemAuth")
        winreg.CloseKey(key)
        
        print("✅ Удалено из автозагрузки")
        
    except FileNotFoundError:
        print("ℹ️ Запись в автозагрузке не найдена")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_from_startup()
    else:
        add_to_startup()
