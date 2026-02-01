import os
import sys
import subprocess
import time

def main():
    # Логирование
    log_file = os.path.join(os.path.dirname(__file__), "startup.log")
    
    try:
        with open(log_file, 'a') as f:
            f.write(f"\n=== TEST Startup at {time.ctime()} ===\n")
            f.write(f"Python: {sys.executable}\n")
            f.write(f"Working dir: {os.getcwd()}\n")
            f.write(f"Script dir: {os.path.dirname(__file__)}\n")
        
        # Проверяем существование файлов
        script_dir = os.path.dirname(__file__)
        locker_path = os.path.join(script_dir, "screen_locker.py")
        
        with open(log_file, 'a') as f:
            f.write(f"Locker exists: {os.path.exists(locker_path)}\n")
            f.write(f"Locker path: {locker_path}\n")
        
        # Запускаем блокировщик
        with open(log_file, 'a') as f:
            f.write("Starting screen locker...\n")
        
        result = subprocess.run([sys.executable, locker_path], 
                               capture_output=True, text=True)
        
        with open(log_file, 'a') as f:
            f.write(f"Return code: {result.returncode}\n")
            f.write(f"Stdout: {result.stdout}\n")
            f.write(f"Stderr: {result.stderr}\n")
        
    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"ERROR: {e}\n")
            import traceback
            f.write(f"Traceback: {traceback.format_exc()}\n")

if __name__ == "__main__":
    main()
