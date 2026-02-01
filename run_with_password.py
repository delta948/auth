import os
import getpass

print("Запуск 2FA с вводом SMTP-пароля (не сохраняется на диск).")
user = os.environ.get("SMTP_USER")
if not user:
    # read smtp_user from config.json if present
    try:
        import json
        base = os.path.dirname(__file__)
        with open(os.path.join(base, "config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)
            user = cfg.get("smtp_user")
    except Exception:
        user = None

if user:
    print(f"SMTP user: {user}")
else:
    user = input("SMTP user (email): ").strip()

pw = getpass.getpass("SMTP password (app password): ")
# set env for child module
os.environ["SMTP_PASSWORD"] = pw
os.environ["SMTP_USER"] = user

# run the app
import two_factor
two_factor.main()
