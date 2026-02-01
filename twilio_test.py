import json
import os
import traceback

# Simple test script to exercise Twilio SMS sending via two_factor.send_code_via_sms
# Usage:
# 1) Set environment variables (recommended):
#    $Env:TWILIO_ACCOUNT_SID = 'ACxxxx'
#    $Env:TWILIO_AUTH_TOKEN = 'your_auth_token'
#    $Env:TWILIO_FROM = '+1234567890'
# 2) python twilio_test.py

from two_factor import load_config, send_code_via_sms, generate_code


def main():
    base = os.path.dirname(__file__)
    cfg_path = os.path.join(base, "config.json")
    cfg = load_config(cfg_path)

    print("Delivery method:", cfg.get("delivery_method"))
    print("Recipient phone:", cfg.get("recipient_phone"))

    code = generate_code()
    print("Sending test SMS with code:", code)
    try:
        send_code_via_sms(cfg, code)
        print("send_code_via_sms returned (check console / Twilio dashboard / recipient phone).")
    except Exception:
        print("Exception during SMS send:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
