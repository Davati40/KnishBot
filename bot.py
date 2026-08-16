import os
import logging
import platform
import discord
from discord import app_commands
from discord.ext import commands

# --- Custom Logging Formatter ---
class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.reset)
        fmt = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        fmt = fmt.replace("(black)", self.black + self.bold)
        fmt = fmt.replace("(reset)", self.reset)
        fmt = fmt.replace("(levelcolor)", log_color)
        fmt = fmt.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

# Configure logger
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
logger.addHandler(console_handler)


# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True

class KnishBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('$'),
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False)
        )

    async def setup_hook(self):
        # Register the slash command group
        self.tree.add_command(CoolGroup(name="cool", description="Says if someone is cool"))
        
        # Sync slash commands globally
        logger.info("Syncing slash commands...")
        synced = await self.tree.sync()
        logger.info(f"Synced {len(synced)} slash command(s).")

bot = KnishBot()
activity = discord.Game(name="nothing. I'm napping.")

@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    logger.info(f"Logged in as: {bot.user}")
    logger.info(f"Running discord.py Version: {discord.__version__}")
    logger.info(f"Running Python Version: {platform.python_version()}")


# --- General Commands (Slash Commands) ---

@bot.tree.command(name="hi", description="Say Hi To Knish")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message("Woof!")

@bot.tree.command(name="aww", description="Basically saying Knish is cute")
async def aww(interaction: discord.Interaction):
    await interaction.response.send_message("Happy Woof!")

@bot.tree.command(name="bork", description="Says 'bork' to Knish")
async def bork(interaction: discord.Interaction):
    await interaction.response.send_message("*runs around house at top speed*")

@bot.tree.command(name="quiet", description="Tells Knish to be quiet")
async def quiet(interaction: discord.Interaction):
    await interaction.response.send_message("Loud Bark!")

@bot.tree.command(name="sit", description="Tells Knish to sit")
async def sit(interaction: discord.Interaction):
    await interaction.response.send_message("*lays*")

@bot.tree.command(name="lay", description="Tells Knish to lay down")
async def lay(interaction: discord.Interaction):
    await interaction.response.send_message("*sits*")

@bot.tree.command(name="squirrel", description="Did somebody say squirrel?!")
async def squirrel(interaction: discord.Interaction):
    await interaction.response.send_message("OMG SQUIRREL? WHERE??")


# --- Cool Group (Slash Command Subcommands) ---

class CoolGroup(app_commands.Group):
    @app_commands.command(name="knish", description="Is Knish cool?")
    async def cool_knish(self, interaction: discord.Interaction):
        await interaction.response.send_message("*Happy Bork!*")

    @app_commands.command(name="davati", description="Is Davati cool?")
    async def cool_davati(self, interaction: discord.Interaction):
        await interaction.response.send_message("*Happy Bork!*")

    @app_commands.command(name="check", description="Check if someone else is cool")
    async def cool_check(self, interaction: discord.Interaction, name: str):
        # Default behavior for any custom name input
        await interaction.response.send_message(f"Growl..! ({name})")


# --- Photo Commands ---

@bot.tree.command(name="sleep", description="Shows Knish sleeping")
async def sleep(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/Dwr7SE2.jpg")

@bot.tree.command(name="alert", description="Shows Knish being alert (and definitely not scared)")
async def alert(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/sfmwytD.jpg")

@bot.tree.command(name="hello", description="Shows Knish being friendly")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/LOrTu7N.jpg")

@bot.tree.command(name="snow", description="Shows Knish walking through snow")
async def snow(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/xYWit3A.jpg")

@bot.tree.command(name="sun", description="Shows Knish sunbathing")
async def sun(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/ykjEPtZ.jpg")

@bot.tree.command(name="spotted", description="Knish has been seen!")
async def spotted(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/6UTehGk.jpg")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.critical("DISCORD_TOKEN environment variable not found!")
    else:
        bot.run(token)
