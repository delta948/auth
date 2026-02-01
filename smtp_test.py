import json
import smtplib
from email.message import EmailMessage
import os


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_send(cfg):
    # Diagnostic: print non-sensitive config info
    print("SMTP server:", cfg.get("smtp_server"))
    print("SMTP port:", cfg.get("smtp_port"))
    print("SMTP user:", cfg.get("smtp_user"))
    # Fallback to environment variable if config has no password
    pw = cfg.get("smtp_password")
    if not pw:
        pw = os.environ.get("SMTP_PASSWORD")
        if pw:
            # remove accidental spaces in pasted app-password
            pw = pw.replace(" ", "")
            print("Using SMTP password from environment (fallback).")
            cfg["smtp_password"] = pw
    print("SMTP password present:", bool(pw), "length:", len(pw) if pw else 0)

    msg = EmailMessage()
    msg["From"] = cfg.get("smtp_from", cfg.get("smtp_user"))
    msg["To"] = cfg.get("recipient_email")
    msg["Subject"] = "SMTP test"
    msg.set_content("This is a test message from smtp_test.py")

    server = None
    try:
        if cfg.get("smtp_tls", True):
            server = smtplib.SMTP(cfg["smtp_server"], cfg.get("smtp_port", 587), timeout=20)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(cfg["smtp_server"], cfg.get("smtp_port", 465), timeout=20)
        server.login(cfg["smtp_user"], cfg["smtp_password"])
        server.send_message(msg)
        print("Письмо успешно отправлено.")
    except Exception as e:
        import traceback

        print("Ошибка при отправке:\n", traceback.format_exc())
    finally:
        if server:
            server.quit()


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    cfg_path = os.path.join(base, "config.json")
    if not os.path.exists(cfg_path):
        print("config.json не найден. Создайте его на основе config.example.json и заполните.")
    else:
        cfg = load_config(cfg_path)
        test_send(cfg)
