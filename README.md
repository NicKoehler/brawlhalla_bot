<center><img src="https://raw.githubusercontent.com/nickoehler/brawlhalla_bot/master/logo.svg" alt="drawing" width="400"/></center>

# Brawlhalla Telegram Bot

Open source rewriting of the original [Brawl Tool](https://t.me/brawltool_bot).

# Table of contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contributions](#contributions)

## Installation

1.  [Optional] Create and activate a virtual enviroment:

    ```sh
    python -m venv venv
    ```

    linux - macos

    ```sh
    source venv/bin/activate
    ```

    windows

    ```powershell

    .\venv\Scripts\activate
    ```

2.  Install the requirements:
    ```
    pip install -r requirements.txt
    ```
3.  Create a .env file:

    ```sh
    cp .env.example .env
    ```

    edit the .env file and add the following variables:

    ```
    API_ID=XXXXXX
    API_KEY=XXXXXXXXXXXXXXXXX
    API_HASH=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    BOT_TOKEN=XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    DATABASE_URL=postgres://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    FLOOD_WAIT_SECONDS=60
    CLEAR_TIME_SECONDS=3600
    ```

    > You can find the **API_ID** and **API_HASH** logging on https://my.telegram.org.

    > Speak with [@BotFather](https://t.me/BotFather) to generate your **BOT_TOKEN**.

    > To use the Brawlhalla API, you need to provide an **API_KEY**. Send an email to api@brawlhalla.com to request one.

4.  Push prisma db:
    ```sh
    prisma db push
    ```

## Usage

Start the bot with:

```sh
python src/bot.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributions

Contributions to this project are welcome. To contribute, follow these steps:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes and commit them with clear commit messages
4. Push your changes to your forked repository
5. Submit a pull request

> Before making any significant changes, please open an issue to discuss the changes you plan to make.
