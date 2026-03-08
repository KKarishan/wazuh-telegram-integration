# Phase 1: Create Your Telegram Bot

> **Goal:** Set up a Telegram Bot that will receive Wazuh security alerts on your phone.

---

## Step 1: Create the Bot via BotFather

1. Open **Telegram** and search for **[@BotFather](https://t.me/botfather)**.
2. Start a chat and type `/newbot`.
3. Follow the prompts:
   - **Bot display name** — e.g., `My Wazuh Alert Bot`
   - **Bot username** — must end in `bot`, e.g., `MyWazuhAlertBot`
4. BotFather will reply with your **API Token** — it looks like:
   ```
   123456789:ABC-defGHIjklMNO-pqrSTUvwxYZ
   ```
   > ⚠️ **Save this token securely.** Treat it like a password — anyone with this token can control your bot.

---

## Step 2: Start the Bot

Search for your newly created bot by its username in Telegram and click **Start**.

> This step is required. The bot cannot send you messages until you have initiated the conversation.

---

## Step 3: Get Your Chat ID

1. Search for **[@myidbot](https://t.me/myidbot)** in Telegram.
2. Type `/getid`.
3. It will return your **Chat ID** — a number like `123456789`.

> 💡 **Note:** If you are adding the bot to a **group**, the Chat ID will be a **negative number** (e.g., `-987654321`).

---

## Summary

You should now have two values saved:

| Value      | Example                                    | Where Used                        |
|------------|--------------------------------------------|-----------------------------------|
| `TOKEN`    | `123456789:ABC-defGHIjklMNO-pqrSTUvwxYZ`  | `custom-telegram.py` script       |
| `CHAT_ID`  | `123456789`                                | `custom-telegram.py` script       |

---

➡️ **Next:** [Phase 2 — Create the Integration Script](integration-wazuh-config.md)
