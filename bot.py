import discord
from discord.ext import commands
import logging
import platform

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
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
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),
                   intents=intents,
                   case_insensitive=True,
                   allowed_mentions=discord.AllowedMentions(everyone=False))
description = 'Knish The Dog In Bot Form'
activity = discord.Game(name="nothing. I'm napping. $help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    print('')
    print('------')
    print(f"{LoggingFormatter.blue}Logged in as:")
    print(f"{LoggingFormatter.yellow}{bot.user}{LoggingFormatter.reset}")
    print('------')
    print(f"{LoggingFormatter.blue}Running API Version: {LoggingFormatter.yellow}{discord.__version__}{LoggingFormatter.reset}")
    print(f"{LoggingFormatter.blue}Running Python Version: {LoggingFormatter.yellow}{platform.python_version()}{LoggingFormatter.reset}")
    print('------')
    print('')


#General Commands

@bot.command()
async def hi(ctx):
    'Say Hi To Me'
    await ctx.send('Woof!')

@bot.command()
async def aww(ctx):
    "Basicly saying I'm Cute"
    await ctx.send('Happy Woof!')

@bot.command()
async def bork(ctx):
    "Says 'bork' To Me"
    await ctx.send('*runs around house at top speed*')

@bot.command()
async def quiet(ctx):
    'Tells Me To Be Quiet'
    await ctx.send('Loud Bark!')

@bot.command()
async def sit(ctx):
    'Tells Me To Sit'
    await ctx.send('*lays*')

@bot.command()
async def lay(ctx):
    'Tells Me To Lay Down'
    await ctx.send('*sits*')

@bot.command()
async def squirrel(ctx):
    'Did Somebody Say Squirrel?!'
    await ctx.send('OMG SQUIRREL? WHERE??')



# 'Cool' Command
# >cool "name" - If name is not in the list below, Knish will say "Growl..!"

@bot.group(pass_context=True)
async def cool(ctx):
    'Says If Someone Is Cool'
    if ctx.invoked_subcommand is None:
        await ctx.send('Growl..!'.format(ctx))


@cool.command(name='knish')
async def _bot(ctx):
    await ctx.send('*Happy Bork!*')


@cool.command(name='davati')
async def _bot(ctx):
    await ctx.send('*Happy Bork!*')

# You can copy and paste the next 3 lines to add more to this command
@cool.command(name='whatever you want to say') #Change the name here
async def _bot(ctx):
    await ctx.send('Growl..!') #Customize what Knish's response is here



# Photos Below

@bot.command()
async def sleep(ctx):
  'Shows Me Sleeping'
  await ctx.send('https://i.imgur.com/Dwr7SE2.jpg')


@bot.command()
async def alert(ctx):
  'Shows Me Being Alert (and definately not scared)'
  await ctx.send('https://i.imgur.com/sfmwytD.jpg')


@bot.command()
async def hello(ctx):
    'Shows Me Being Friendly'
    await ctx.send('https://i.imgur.com/LOrTu7N.jpg')

@bot.command()
async def snow(ctx):
    'Shows Me Walking Through Snow'
    await ctx.send('https://i.imgur.com/xYWit3A.jpg')

@bot.command()
async def sun(ctx):
  'Shows Me Sunbathing'
  await ctx.send('https://i.imgur.com/ykjEPtZ.jpg')

@bot.command()
async def spotted(ctx):
  "I've Been Seen!"
  await ctx.send('https://i.imgur.com/6UTehGk.jpg')


bot.run('TOKEN')
