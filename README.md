# 🤖 Ilie Moromete – Discord Bot

A multifunctional Discord bot built with `discord.py`, offering fun commands, news updates, music playback from YouTube, and real-time weather information. Designed for Romanian-language communities but easily extendable for any server.

---

## 🚀 Features

- 👋 Greets new members and gives them a role automatically
- 📰 Fetches the latest news from BBC using NewsAPI
- 🎵 Plays music from YouTube using `yt-dlp` and FFmpeg
- 🌦️ Displays real-time weather using OpenWeatherMap API
- 🎲 Fun commands like `!roll`, `!ping`, `!echo`
- 📦 Queue system for music with skip and leave commands

---

## 🛠 Technologies & Libraries

- [`discord.py`](https://github.com/Rapptz/discord.py) – Bot framework
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) – YouTube download
- [`NewsAPI`](https://newsapi.org/)
- [`OpenWeatherMap`](https://openweathermap.org/)
- `asyncio`, `requests`, `python-dotenv`

---

## 🔐 Environment Variables

All sensitive keys and tokens are stored in a `.env` file (ignored via `.gitignore`):

```
DISCORD_TOKEN=your_discord_bot_token
WEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
```

Install `python-dotenv` if not already:

```bash
pip install python-dotenv
```

---

## ▶️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ilie-moromete-discord-bot.git
   cd ilie-moromete-discord-bot
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your `.env` file to the root of the project.

4. Run the bot:
   ```bash
   python Bot_SECURE.py
   ```

---

## 📸 Screenshots

### 🎵 Music Playback with `!play`
![Music Playback](da77ce66-9601-4dc4-9dd9-99f8b3bb2608.png)

### ⏭️ Skipping Songs with `!skip`
![Skip Command](edd2039e-5c54-4201-870f-af95c8b52422.png)

### 📰 News Command with `!news`
![News Command](30d162e5-ff90-41cb-9afa-35cac5f5c5c5.png)

### 🌤️ Weather Info with `!weather`
![Weather Command](dc06e289-1bfa-46ce-a9cc-a4774b6b2369.png)

---

## 📂 File Structure

```
├── Bot_SECURE.py           # Main bot script (token/API safe)
├── .env                    # Environment variables (not committed)
├── Pisica.gif              # Animated asset
├── song.mp3                # Sample audio file
├── ffmpeg/...              # FFmpeg directory (for playback)
├── Librarii utilizate.txt  # List of libraries used
```

---

## 👤 Author

Created by **Ciprian Belet**  
Feel free to contribute, open issues, or fork the project.

---

## 📜 License

This project is open-source and available under the MIT License.
