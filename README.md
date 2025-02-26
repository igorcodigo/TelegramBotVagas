# Telegram Job Bot - IT Job Listings

This is a Telegram bot developed in Python that collects messages from IT job listing groups and stores them in a MongoDB database. The bot allows users to display the latest numbered messages from each job group via Telegram commands.

## Features

- Collects messages from IT job listing groups and stores them in MongoDB.
- Displays the most recent numbered messages (from newest to oldest).
- Commands to restart message collection and display stored messages.

## Requirements

- **Python 3.10+**
- Telegram account to create a bot (using [BotFather](https://core.telegram.org/bots#botfather))
- Telegram API (ID and Hash)
- MongoDB to store the messages
- Configured environment variables

## Installation

1. Clone the repository to your local environment:

    ```bash
    git clone https://github.com/your-username/telegram-job-bot.git
    cd telegram-job-bot
    ```

2. Create and activate a virtual environment (optional, but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables. Create a `.env` file based on the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

5. Edit the `.env` file and add your credentials (Telegram API, phone number, MongoDB, etc.):

    ```env
    API_ID=1234567
    API_HASH=abcd1234efgh5678ijkl9012mnopqrst
    PHONE_NUMBER=+5511999999999
    TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abc
    MONGO_URI=mongodb://localhost:27017
    ```

6. Start the bot:

    ```bash
    python main.py
    ```

## Bot Commands

- `/start` — Displays a list of available commands.
- `/reset` — Refreshes job group messages in MongoDB.
- `/show` — Displays messages collected from all groups stored in MongoDB.
- `/group_name` — Displays messages from a specific group (example: `/MidLevel_IT_Jobs`).

## How to Obtain Telegram Credentials

1. Register as a developer on [My Telegram](https://my.telegram.org) to get your **API ID** and **API Hash**.
2. Create a bot on Telegram using [BotFather](https://core.telegram.org/bots#botfather) to get your bot's **TOKEN**.
