#!/usr/bin/env python3
# =============================================================================
# custom-telegram.py - v2 (Enhanced Version)
# Wazuh Custom Integration: Send enriched alerts to Telegram
#
# Description:
#   Enhanced integration script that extracts detailed attacker information
#   from Windows security events (e.g., Event ID 4625 - failed logon).
#   Includes Attacker IP, Attacker Machine Name, and MITRE ATT&CK IDs.
#
# Improvements over v1:
#   - Added attacker IP and machine name extraction
#   - Added MITRE ATT&CK ID parsing
#   - Improved message formatting with visual separators
#   - Used .get() for safe key access (prevents KeyError crashes)
#   - Reads full alert JSON instead of first line only
#
# Usage:
#   Called automatically by Wazuh Manager when an alert is triggered.
#   Manual test: sudo /var/ossec/integrations/custom-telegram.py /tmp/test_alert.json
#
# Author: Karishan
# =============================================================================

import sys
import json
import requests

# --- CONFIGURATION ---
# Replace these with your actual Telegram Bot credentials
CHAT_ID = "YOUR_CHAT_ID_HERE"
TOKEN   = "YOUR_BOT_TOKEN_HERE"
HOOK_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# --- READ ALERT FILE ---
# Wazuh passes the alert file path as the first argument
with open(sys.argv[1]) as f:
    alert_json = json.loads(f.read())

# --- DATA EXTRACTION ---
rule  = alert_json.get('rule',  {})
agent = alert_json.get('agent', {})
data  = alert_json.get('data',  {})
win   = data.get('win', {}).get('eventdata', {})

# Basic alert info
level       = rule.get('level')
description = rule.get('description')
agent_name  = agent.get('name')

# Attacker machine name
# Windows Event ID 4625 stores the source workstation in multiple possible fields
attacker_machine = (
    win.get('workstationName') or
    data.get('srcuser') or
    "Unknown Name"
)

# Attacker IP address
# Checks standard Wazuh field first, then Windows-specific fields
attacker_ip = (
    data.get('srcip') or
    win.get('ipAddress') or
    "Unknown IP"
)

# MITRE ATT&CK technique IDs
mitre_ids     = rule.get('mitre', {}).get('id', [])
mitre_ids_str = ", ".join(mitre_ids) if mitre_ids else "N/A"

# --- MESSAGE FORMATTING ---
message = (
    f"🚨 *WAZUH ALERT - Level {level}*\n"
    f"━━━━━━━━━━━━━━━━━━━━\n"
    f"👤 *Victim Agent:* {agent_name}\n"
    f"📝 *Event:* {description}\n"
    f"━━━━━━━━━━━━━━━━━━━━\n"
    f"💀 *ATTACKER DETAILS*\n"
    f"🖥️ *Machine Name:* `{attacker_machine}`\n"
    f"🌐 *Source IP:* `{attacker_ip}`\n"
    f"━━━━━━━━━━━━━━━━━━━━\n"
    f"🎯 *MITRE ID:* `{mitre_ids_str}`\n"
    f"━━━━━━━━━━━━━━━━━━━━"
)

# --- SEND TO TELEGRAM ---
requests.post(HOOK_URL, json={
    'chat_id':    CHAT_ID,
    'text':       message,
    'parse_mode': 'Markdown'
})
