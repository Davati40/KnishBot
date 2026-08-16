FROM python:latest

WORKDIR /app

# Copy dependencies first for efficient layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all repository files (including bot.py)
COPY . .

# Start the bot
CMD ["python", "bot.py"]
