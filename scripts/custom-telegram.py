#!/usr/bin/env python3
# =============================================================================
# custom-telegram.py - v1 (Initial Version)
# Wazuh Custom Integration: Send alerts to Telegram
#
# Description:
#   Basic integration script that reads a Wazuh alert and sends the rule level,
#   description, and agent name to a Telegram bot.
#
# Usage:
#   Called automatically by Wazuh Manager when an alert is triggered.
#   Manual test: sudo /var/ossec/integrations/custom-telegram.py /tmp/test_alert.json
#
# Author: [Your Name]
# =============================================================================

import sys
import json
import requests

# --- CONFIGURATION ---
# Replace these with your actual Telegram Bot credentials
CHAT_ID = "YOUR_CHAT_ID_HERE"
TOKEN = "YOUR_BOT_TOKEN_HERE"
HOOK_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# --- READ ALERT FILE ---
# Wazuh passes the alert file path as the first argument
with open(sys.argv[1]) as f:
    # Read only the first line (one alert per line in Wazuh JSON format)
    first_line = f.readline()
    alert_json = json.loads(first_line)

# --- DATA EXTRACTION ---
level       = alert_json['rule']['level']
description = alert_json['rule']['description']
agent       = alert_json['agent']['name']

# --- MESSAGE FORMATTING ---
message = (
    f"🚨 *Wazuh Alert - Level {level}*\n\n"
    f"👤 *Agent:* {agent}\n"
    f"📝 *Description:* {description}"
)

# --- SEND TO TELEGRAM ---
requests.post(HOOK_URL, json={
    'chat_id':    CHAT_ID,
    'text':       message,
    'parse_mode': 'Markdown'
})
