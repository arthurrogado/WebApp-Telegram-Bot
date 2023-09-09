# Example of a two-way communication between bot and webapp
# Exemplo de uma comunicação de dois lados entre bot e webapp

### This example uses @pyTelegramBotAPI to create a bot that sends messages to a webapp
### And vanila javascript to implement a Telegram webapp

## Functionality:

1. Bot gets data from user
2. Bot creates and sends a keyboard button with webapp initialisation link (with data via GET)
3. User clicks the button and opens the webapp
4. Webapp uses the data from the link to populate the page form
5. User fills the form and 'submits' it
6. Webapp sends the data to the bot by webapp.SendData() method
7. Bot receives the data with a message_handler filtering by content_types=['web_app_data']
8. Bot sends a message with the data back to the user, but can do anything else with it

## How to use:

1. Create a bot with @BotFather
2. Fill api_token.py with your bot token
3. Deploy the webapp folder to a server (must be https) and fill WEBAPP_URL in bot.py
3.1. If you don't have a server, you can use ngrok to create a tunnel to your localhost
3.2. A free option of a server, and is what I used, is squarecloud.app (https://squarecloud.app/)
4. Run bot.py

## Working example:
https://t.me/webappcomunicationbot

## Contact me:
https://arthurrogado.t.me