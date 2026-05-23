# Telegram Bot for Raspberry Pi

A simple Python-based Telegram bot for Raspberry Pi that saves photos and text messages to your local storage.

## Features

 **Photo Upload** - Send photos through Telegram and they'll be saved with timestamps
 **Message Storage** - Send text messages to save them as `.txt` files organized by date
 **Auto-Organization** - Files are automatically organized into subdirectories
 **Logging** - All activities are logged for debugging
 **Error Handling** - Graceful error handling with user feedback

## Requirements

- Python 3.7+
- Raspberry Pi (or any Linux system)
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Internet connection

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/anaswarramesh/telegram_rpi_bot.git
cd telegram_rpi_bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
cp .env.example .env
nano .env
```

Add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

### 4. Create Storage Directory
```bash
mkdir -p /home/user/telegram_rpi/photos
mkdir -p /home/user/telegram_rpi/messages
mkdir -p /home/user/telegram_rpi/logs
```

### 5. Run the Bot
```bash
python bot.py
```

## Directory Structure

After setup, your storage will look like this:
```
/home/user/telegram_rpi/
├── photos/              # Saved photos
│   └── photo_2026_04_26_143022.jpg
├── messages/            # Saved text messages
│   └── 2026-04-26.txt
├── logs/                # Bot logs
│   └── telegram_bot.log
```

## Usage

### Commands

- `/start` - Shows welcome message and available commands
- `/help` - Shows list of available features

### How to Use

1. **Send a Photo**
   - Just send a photo directly to the bot
   - The bot will save it with a timestamp and confirm

2. **Send a Message**
   - Type any text message and send it to the bot
   - It will be saved to today's `.txt` file in `/messages/` directory
   - Each message includes timestamp

## Bot Features

### Photo Handling
- Photos are saved with timestamp format: `photo_YYYY_MM_DD_HHMMSS.jpg`
- Stored in `/home/user/telegram_rpi/photos/`
- Includes file size information in logs

### Message Handling
- Messages are saved to date-named files: `YYYY-MM-DD.txt`
- Each message includes timestamp: `[HH:MM:SS] message_text`
- Automatic directory creation if missing

### Logging
- All activities logged to `/home/user/telegram_rpi/logs/telegram_bot.log`
- Console output for real-time monitoring
- Includes errors, saves, and system events

## Optional: Auto-Start on Raspberry Pi

### Using Systemd Service

1. Copy the service file:
```bash
sudo cp systemd/telegram_bot.service /etc/systemd/system/
```

2. Edit the service file if needed:
```bash
sudo nano /etc/systemd/system/telegram_bot.service
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram_bot.service
sudo systemctl start telegram_bot.service
```

4. Check status:
```bash
sudo systemctl status telegram_bot.service
```

5. View logs:
```bash
journalctl -u telegram_bot.service -f
```

## Troubleshooting

### Bot not responding
- Check if the token is correct in `.env`
- Ensure internet connection is working
- Check logs: `tail -f /home/user/telegram_rpi/logs/telegram_bot.log`

### Files not being saved
- Verify directory exists: `ls -la /home/user/telegram_rpi/`
- Check permissions: `sudo chmod 755 /home/user/telegram_rpi`
- Check disk space: `df -h`

### Python module not found
- Reinstall requirements: `pip install --upgrade -r requirements.txt`
- Use virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## Configuration

Edit `config.py` to customize:
- Storage paths
- Logging format
- Bot messages
- File naming conventions

## License

MIT License - Feel free to modify and use as needed.

## Support

For issues or questions, create an issue in the repository.
