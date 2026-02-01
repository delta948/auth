import json
import random
import smtplib
import threading
import time
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
import os
import traceback
import urllib.parse
import urllib.request
import base64


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_code():
    return "{:06d}".format(random.randint(0, 999999))


def send_code_via_email(cfg, code):
    msg = EmailMessage()
    msg["From"] = cfg.get("smtp_from", cfg.get("smtp_user"))
    msg["To"] = cfg.get("recipient_email")
    msg["Subject"] = cfg.get("email_subject", "Кирүү кодуңуз")
    body = cfg.get("email_body", "Кодуңуз: {code}\nЭгерде сиз кодду сурабасаңыз, бул билдирүүнө көңүл бурбаңыз.").format(code=code)
    msg.set_content(body, charset='utf-8')

    server = None
    try:
        if cfg.get("smtp_tls", True):
            server = smtplib.SMTP(cfg["smtp_server"], cfg.get("smtp_port", 587), timeout=20)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(cfg["smtp_server"], cfg.get("smtp_port", 465), timeout=20)
        server.login(cfg["smtp_user"], cfg["smtp_password"])
        server.send_message(msg)
    finally:
        if server:
            server.quit()


def send_code_via_sms(cfg, code):
    # Prefer environment variables for secrets
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID") or cfg.get("twilio_account_sid")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN") or cfg.get("twilio_auth_token")
    from_number = os.environ.get("TWILIO_FROM") or cfg.get("sms_from")
    to_number = cfg.get("recipient_phone")
    body = cfg.get("sms_body", "Ваш код: {code}").format(code=code)

    if not (account_sid and auth_token and from_number and to_number):
        # Dry-run — логируем, но не падаем
        print("Twilio credentials or phone numbers missing — dry-run SMS:", body)
        return

    data = urllib.parse.urlencode({"To": to_number, "From": from_number, "Body": body}).encode()
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    req = urllib.request.Request(url, data=data)
    auth = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    req.add_header("Authorization", f"Basic {auth}")

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp_text = resp.read().decode(errors="ignore")
            if resp.getcode() >= 400:
                raise Exception(f"Twilio API error: {resp.getcode()} {resp_text}")
    except Exception:
        raise


class TwoFactorApp:
    def __init__(self, cfg):
        self.cfg = cfg
        self.code = None
        self.code_sent_at = 0
        self.resend_cooldown = cfg.get("resend_cooldown_seconds", 60)

        self.root = tk.Tk()
        self.root.title("Two-Factor Authentication")
        self.root.attributes("-topmost", True)
        self.root.attributes("-fullscreen", True)

        self.frame = tk.Frame(self.root, bg="#222")
        self.frame.pack(expand=True, fill="both")

        label = tk.Label(self.frame, text=cfg.get("prompt_text", "Электрондук почтага жөнөтүлгөн 6 орундуу кодду киргизиңиз"),
                         fg="#fff", bg="#222", font=(None, 24))
        label.pack(pady=20)

        self.entry = tk.Entry(self.frame, font=(None, 28), justify="center")
        self.entry.pack(pady=10)

        submit = tk.Button(self.frame, text="Тастыктоо", command=self.check_code, font=(None, 18))
        submit.pack(pady=10)

        self.resend_btn = tk.Button(self.frame, text="Кодду кайра жөнөтүү", command=self.resend_code, font=(None, 14))
        self.resend_btn.pack(pady=6)

        quit_btn = tk.Button(self.frame, text="Чыгуу", command=self.exit_app, font=(None, 12))
        quit_btn.pack(side="bottom", pady=20)

        self.status_label = tk.Label(self.frame, text="", fg="#ddd", bg="#222")
        self.status_label.pack(pady=6)

    def start(self):
        self.send_new_code()
        self.update_resend_button()
        self.root.mainloop()

    def send_new_code(self):
        self.code = generate_code()
        self.code_sent_at = time.time()
        threading.Thread(target=self._deliver_thread, args=(self.code,), daemon=True).start()
        method = self.cfg.get("delivery_method", "email")
        if method == "sms":
            self.status_label.config(text="Код жөнөтүлдү (SMS'ти текшериңиз)")
        elif method == "both":
            self.status_label.config(text="Код жөнөтүлдү (почта жана SMS'ти текшериңиз)")
        else:
            self.status_label.config(text="Код жөнөтүлдү (почтаны текшериңиз)")

    def _deliver_thread(self, code):
        try:
            method = self.cfg.get("delivery_method", "email")
            errors = []
            if method in ("email", "both"):
                try:
                    send_code_via_email(self.cfg, code)
                except Exception as e:
                    errors.append(f"email: {e}")
            if method in ("sms", "both"):
                try:
                    send_code_via_sms(self.cfg, code)
                except Exception as e:
                    errors.append(f"sms: {e}")
            if errors:
                raise Exception("; ".join(errors))
        except Exception as e:
            tb = traceback.format_exc()
            self.status_label.config(text=f"Жөнөтүү катасы: {e}")
            print("Ошибка отправки:\n", tb)
            try:
                base = os.path.dirname(__file__)
                with open(os.path.join(base, "error.log"), "a", encoding="utf-8") as f:
                    f.write(f"{time.ctime()} - Ошибка отправки:\n{tb}\n")
            except Exception:
                pass

    def check_code(self):
        entered = self.entry.get().strip()
        if entered == self.code:
            self.root.destroy()
        else:
            messagebox.showerror("Код туура эмес", "Код туура эмес. Кайра аракет кылыңыз.")

    def resend_code(self):
        now = time.time()
        if now - self.code_sent_at < self.resend_cooldown:
            remaining = int(self.resend_cooldown - (now - self.code_sent_at))
            messagebox.showinfo("Күтүңүз", f"Көп жөнөтүүгө болбойт. {remaining} секунд күтүңүз.")
            return
        self.send_new_code()

    def update_resend_button(self):
        now = time.time()
        remaining = int(max(0, self.resend_cooldown - (now - self.code_sent_at))) if self.code_sent_at else 0
        if remaining > 0:
            self.resend_btn.config(state="disabled", text=f"Кайра жөнөтүү ({remaining}s)")
        else:
            self.resend_btn.config(state="normal", text="Кодду кайра жөнөтүү")
        self.root.after(1000, self.update_resend_button)

    def exit_app(self):
        # Exit without unlocking — user choice. This demo does not kill session.
        self.root.destroy()


def ensure_config_exists(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}. Create config.json from config.example.json and fill values.")


def main():
    base = os.path.dirname(__file__)
    cfg_path = os.path.join(base, "config.json")
    ensure_config_exists(cfg_path)
    cfg = load_config(cfg_path)
    # Allow sensitive password to be provided at runtime via environment variable
    env_pw = os.environ.get("SMTP_PASSWORD")
    if env_pw:
        # remove accidental spaces (Google may display app passwords with spaces)
        cfg["smtp_password"] = env_pw.replace(" ", "")
    env_user = os.environ.get("SMTP_USER")
    if env_user:
        cfg["smtp_user"] = env_user
    env_from = os.environ.get("SMTP_FROM")
    if env_from:
        cfg["smtp_from"] = env_from
    app = TwoFactorApp(cfg)
    app.start()


if __name__ == "__main__":
    main()
