import os
import sys
import subprocess
import time

def main():
    # Логирование для отладки
    log_file = os.path.join(os.path.dirname(__file__), "startup.log")
    
    try:
        with open(log_file, 'a') as f:
            f.write(f"\n=== Startup at {time.ctime()} ===\n")
            f.write(f"Python: {sys.executable}\n")
            f.write(f"Working dir: {os.getcwd()}\n")
        
        # Ждем загрузки системы
        time.sleep(5)
        
        # Запускаем блокировщик экрана
        script_dir = os.path.dirname(os.path.abspath(__file__))
        locker_path = os.path.join(script_dir, "screen_locker.py")
        
        with open(log_file, 'a') as f:
            f.write(f"Starting locker: {locker_path}\n")
        
        result = subprocess.run([sys.executable, locker_path], check=True, 
                               capture_output=True, text=True)
        
        with open(log_file, 'a') as f:
            f.write(f"Locker completed successfully\n")
            f.write(f"Return code: {result.returncode}\n")
        
    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"ERROR: {e}\n")
            f.write(f"Stdout: {getattr(result, 'stdout', 'N/A')}\n")
            f.write(f"Stderr: {getattr(result, 'stderr', 'N/A')}\n")
        
        # При ошибке блокируем систему
        subprocess.run([sys.executable, os.path.join(script_dir, "lock_system.py")])

if __name__ == "__main__":
    main()
