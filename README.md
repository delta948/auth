# Two-step (email) 2FA demo for Windows (Python)

Коротко: это демонстрационный скрипт на Python, который после запуска открывает полноэкранное окно и требует ввести 6-значный код, отправленный на e-mail. Скрипт не интегрируется в встроенную систему аутентификации Windows — он предназначен как дополнительный шаг, запускаемый при входе пользователя (через Task Scheduler).

Файлы:
- `two_factor.py` — основной скрипт.
- `config.example.json` — пример конфигурации SMTP и e-mail.
- `config.json` — ваш файл конфигурации (скопируйте из `config.example.json` и заполните).

Настройка:
1. Скопируйте `config.example.json` в `config.json` и укажите реальные значения SMTP, `smtp_user`, `smtp_password` и `recipient_email`.

2. Установите Python (если ещё не установлен). Рекомендуется Python 3.8+.

3. Запуск вручную для теста:
```powershell
python c:\Users\Delta\Desktop\auth\two_factor.py
```

4. Чтобы запускать скрипт при каждом входе в систему (Task Scheduler):
   - Откройте `Task Scheduler` → `Create Task...`.
   - На вкладке `General` задайте имя (например, `TwoFactorOnLogin`) и выберите `Run only when user is logged on`.
   - На вкладке `Triggers` создайте новый триггер `At log on` для вашего пользователя.
   - На вкладке `Actions` добавьте действие `Start a program` и укажите в `Program/script` путь к `pythonw.exe` (чтобы не показывать консоль), в `Add arguments` укажите полный путь к `two_factor.py`.

Пример команды `schtasks` (запустите от имени администратора или под своей учётной записью — проверьте параметры):
```powershell
schtasks /Create /SC ONLOGON /RU "%USERNAME%" /TN "TwoFactorOnLogin" /TR "\"C:\\Path\\To\\pythonw.exe\" \"C:\\Users\\Delta\\Desktop\\auth\\two_factor.py\"" /F
```

Ограничения и безопасность:
- Этот скрипт — демонстрация. Он не заменяет полноценную интеграцию 2FA в механизм входа Windows.
- Полноэкранное окно можно обойти (Alt+Tab, Ctrl+Alt+Del и т.д.). Для реальной защиты нужно использовать поддерживаемые решения (Windows Hello, корпоративные сервисы MFA, сетевые политики).
- Храните `smtp_password` безопасно и используйте, когда возможно, `app password` (например, для Gmail).

Если хотите, могу:
- Помочь заполнить `config.json` под ваш почтовый провайдер.
- Создать задачу `schtasks` автоматически.
- Улучшить интерфейс (локализация, блокировка клавиш и т.д.) — предупредите о рисках безопасности.

Gmail — быстрые шаги (рекомендуется):

- Включите двухфакторную аутентификацию в вашей Google-учётной записи.
- Создайте `App password` (в разделе Security → App passwords) и скопируйте сгенерированный пароль.
- В `config.json` оставьте `smtp_password` пустым, а `smtp_user` и `smtp_from` укажите ваш e-mail (например, `danisaifudinov@gmail.com`).
- Чтобы не хранить пароль в файле, используйте вспомогательный скрипт, который спросит пароль в терминале и запустит приложение:

```powershell
cd C:\Users\Delta\Desktop\auth
python run_with_password.py
```

Скрипт запросит `SMTP user` (если не указан в `config.json`) и `SMTP password` (app password), затем запустит окно ввода 2FA.

Если хотите запускать без ввода пароля, заполните `smtp_password` в `config.json` (не рекомендуется хранить пароль в открытом виде).

---

SMS (Twilio) — быстрые шаги:

- Если хотите получать коды по SMS, установите в `config.json`:
  - `delivery_method`: `"sms"` или `"both"` (email + sms)
  - `recipient_phone`: номер получателя в международном формате (например, `+996220894773`)
  - `sms_from`: ваш Twilio номер (например, `+1234567890`)

- Настройте переменные окружения с учётными данными Twilio (не храните токены в репозитории):
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_FROM` (опционально, можно задать в `config.json`)

- Пример использования (dry-run если креды не заданы):
```powershell
$Env:TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$Env:TWILIO_AUTH_TOKEN = "your_auth_token"
$Env:TWILIO_FROM = "+1234567890"
python two_factor.py
```

- Примечание: если переменные окружения/параметры отсутствуют, скрипт выполнит dry-run и выведет сообщение в консоль и в `error.log`.

