TubulenceBot - Telegram Chatbot Powered by LLaMA 3 via Groq API

TubulenceBot is a conversational Telegram bot that interacts with users naturally. It uses [Groq](https://console.groq.com/)’s blazing fast LLaMA 3 model (`llama3-8b-8192`) to generate intelligent responses in real-time.

 [Talk to the Bot](https://t.me/tubulenceBot)

Features

- Collects user name, age, and favorite programming language
- Initiates a natural, AI-driven conversation
- Keeps chat memory across messages using Groq API
- Fully asynchronous and scalable with `python-telegram-bot`

Requirements

- Python 3.9+
- `python-telegram-bot`
- `requests`
- `python-dotenv`

Install dependencies:

```bash
pip install python-telegram-bot requests python-dotenv
