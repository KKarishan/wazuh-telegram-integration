# Phase 2 & 3: Integration Script & Wazuh Configuration

> **Goal:** Deploy the Python script on the Wazuh server and configure the Wazuh Manager to call it automatically when an alert fires.

---

## Phase 2: Deploy the Integration Script

### Step 1: Create the Script File

SSH into your Wazuh Manager server and create the integration script:

```bash
sudo nano /var/ossec/integrations/custom-telegram.py
```

Paste the contents of [`custom-telegram.py`](../scripts/custom-telegram.py) from this repository.

> ⚠️ **Replace the placeholder credentials** at the top of the file:
> ```python
> CHAT_ID = "YOUR_CHAT_ID_HERE"   # ← Your Telegram Chat ID
> TOKEN   = "YOUR_BOT_TOKEN_HERE" # ← Your Bot API Token
> ```

---

### Step 2: Set Correct Permissions

Wazuh runs under the `wazuh` user. The script must be owned by `root:wazuh` and executable — otherwise the integration will **fail silently**.

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-telegram.py
sudo chmod 750 /var/ossec/integrations/custom-telegram.py
```

| Permission | Meaning                                      |
|------------|----------------------------------------------|
| `750`      | Owner (root) can read/write/execute          |
|            | Group (wazuh) can read/execute               |
|            | Others have no access                        |

---

## Phase 3: Configure Wazuh Manager

### Step 3: Edit ossec.conf

Open the main Wazuh configuration file:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Scroll to the **bottom** of the file. Just **above** the closing `</ossec_config>` tag, paste this block:

```xml
<integration>
  <name>custom-telegram.py</name>
  <level>7</level>
  <alert_format>json</alert_format>
</integration>
```

#### Configuration Options Explained

| Tag              | Value              | Description                                                                 |
|------------------|--------------------|-----------------------------------------------------------------------------|
| `<name>`         | `custom-telegram.py` | Must exactly match the filename in `/var/ossec/integrations/`             |
| `<level>`        | `7`                | Minimum alert level to trigger. Level 7 = medium-to-high severity threats  |
| `<alert_format>` | `json`             | Passes the alert to the script as a JSON file                               |

> 💡 **Level Guidance:**
> - Level `3–5` → Very noisy. Thousands of low-level logs will trigger notifications.
> - Level `7` → Recommended. Catches meaningful events (failed logins, sudo usage, etc.).
> - Level `10+` → High-severity only (brute force, privilege escalation, malware).

---

### Step 4: Restart Wazuh Manager

Apply the configuration changes:

```bash
sudo systemctl restart wazuh-manager
```

Verify the service is running:

```bash
sudo systemctl status wazuh-manager
```

---

## Testing the Integration

Since the script expects a **file path** as its argument (`sys.argv[1]`), you can test it manually without waiting for a real alert.

### Create a Test Alert File & Run the Script

```bash
# Extract the most recent alert from the Wazuh alerts log
sudo tail -n 1 /var/ossec/logs/alerts/alerts.json > /tmp/test_alert.json

# Run the script manually against the test file
sudo /var/ossec/integrations/custom-telegram.py /tmp/test_alert.json
```

If configured correctly, you will receive a Telegram message within a few seconds.

---

## Expected Telegram Notification

```
🚨 WAZUH ALERT - Level 10
━━━━━━━━━━━━━━━━━━━━
👤 Victim Agent: Windows-10-Client
📝 Event: Multiple Windows logon failures
━━━━━━━━━━━━━━━━━━━━
💀 ATTACKER DETAILS
🖥️ Machine Name: KALI-LINUX-VM
🌐 Source IP: 192.168.0.22
━━━━━━━━━━━━━━━━━━━━
🎯 MITRE ID: T1110
━━━━━━━━━━━━━━━━━━━━
```

---

➡️ **Back to:** [README](../README.md)
