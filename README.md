# photoshop_tg
A bot for Telegram that lets you create and edit templates right in the app

# full_description
1) A bot for Telegram that lets you draw directly in the app.
2) You can create layers to templates and customize them (font size, font, font color, alignment and coordinates).
3) Implemented admin panel for easy communication with users (sending gifs/videos/text messages/photos/documents, approving user templates) 
4) Implementation of welcome captcha and anti-spam text protection to catch bots
5) Implementation of compulsory channel subscription and its further Middleware audit
6) Ability to add fonts via bot menu
7) The ability to rate other users' templates and add them to favorites
8) Ability to create your own templates and send them for moderation, after approval all interested bot users will be able to use that template.
9) The bot clears all previous posts for a more pleasant interface.
10) Template owners can modify them at any time and at their own discretion

# install
First of all You need to set up your config file -> settings.ini without ' or "

token=BOT_TOKEN
admin_id=ADMIN_ID_1,ADMIN_ID_2...
bot_name=BOT_NAME_WITHOUT_@
channel_id=-100...
channel_url=https://t.me/your_channel_channel
chat_url=https://t.me/your_chat_url
faq_url=https://t.me/your_faq_url
licence_url=https://t.me/your_licence

make sure the bot is added to the channel as an administrator

# run bot
1) You must have Python3.8+ installed
2) You must have the venv virtual environment installed
3) python -m venv venv
4) venv/scripts/activate
5) pip install -r req.txt
6) python main.py
