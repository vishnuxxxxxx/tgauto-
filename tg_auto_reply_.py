from telethon import TelegramClient, events
import asyncio
import time
import random
from quart import Quart, render_template_string

# Set your API_ID and API_HASH
api_id = 26124454  # Replace with your API ID
api_hash = '60fb2a214a81e55c8a48c5236f7afe33'  # Replace with your API hash

client = TelegramClient('session_name55', api_id, api_hash)
app = Quart(__name__)

last_reply_time = {}
WAIT_TIME = 120  
bot_ping = 0.0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ml">
<head>
    <meta charset="UTF-8">
    <title>DemonXRD Status</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding-top: 50px; }
        .container { background-color: #1e1e1e; padding: 20px; border-radius: 10px; display: inline-block; width: 300px; }
        h1 { color: #00bcd4; }
        .status { color: #4caf50; font-weight: bold; }
        .ping { color: #ffeb3b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>DemonXRD</h1>
        <p>Status: <span class="status">Bot is still running</span></p>
        <p>Ping: <span class="ping">{{ ping }} ms</span></p>
    </div>
</body>
</html>
"""

@app.route('/')
async def status_page():
    return await render_template_string(HTML_TEMPLATE, ping=bot_ping)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private:
        return
        
    user_id = event.sender_id
    current_time = time.time()
    
    await asyncio.sleep(random.uniform(1.0, 3.0))

    if user_id not in last_reply_time:
        await event.reply(
            "Hello 👋, thank you for contacting Demon Services 🛡️. We are currently busy, but we will get back to you shortly ⏳. Thank you for your patience! 😊"
        )
        last_reply_time[user_id] = current_time
        
    elif current_time - last_reply_time[user_id] >= WAIT_TIME:
        await event.reply(
            "Still busy! 🕰️ We haven't forgotten about you and will contact you back as soon as possible. 🌟 Thanks for understanding! 😊"
        )
        last_reply_time[user_id] = current_time

async def ping_task():
    global bot_ping
    while True:
        start_time = time.time()
        await client.get_me()
        bot_ping = round((time.time() - start_time) * 1000, 2)
        await asyncio.sleep(30)

async def main():
    await client.start()
    print("Telegram auto-reply bot and web server are running successfully...")
    
    # ടെലിഗ്രാം പിംഗ് കണക്കാക്കുന്ന ടാസ്ക് പശ്ചാത്തലത്തിൽ തുടങ്ങുന്നു
    asyncio.create_task(ping_task())
    
    # ക്വാർട്ട് വെബ് സെർവർ സ്റ്റാർട്ട് ചെയ്യുന്നു
    await app.run_task(host='0.0.0.0', port=5000)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped manually.")
        