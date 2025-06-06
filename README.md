# KTchecker - Kel'Thuzad Realm Status Bot

A simple Discord bot that checks the status of the **Kel'Thuzad-US World of Warcraft realm**.

Features:

- `/ktstatus` slash command
    - TCP connection check to known realm IPs
    - Scrapes Blizzard's official realm status page

---

## Setup

1️⃣ Clone the repo:

```bash
git clone https://github.com/Gatsumo/KTchecker.git
cd KTchecker
2️⃣ Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Create .env file (see below).

4️⃣ Run the bot:

bash
Copy
Edit
python bot.py