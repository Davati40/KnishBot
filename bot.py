import discord
from discord.ext import commands
import logging
import platform

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='>')
description = '''Knish The Dog In Bot Form. Please Use All Lowercase Letters.'''
activity = discord.Game(name="nothing. I'm napping. >help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    print('')
    print('------')
    print('Logged in as:\n{0} (ID:{0.id})'.format(bot.user))
    print('------')
    print('Running API Version:' + discord.__version__)
    print('Running Python Version:' + platform.python_version())
    print('------')
    print('')


# General Commands

@bot.command()
async def hi(ctx):
    '''Say Hi To Me.'''
    await ctx.send('Woof!')

@bot.command()
async def aww(ctx):
    '''Basicly saying I'm Cute.'''
    await ctx.send('Happy Woof!')

@bot.command()
async def bork(ctx):
    '''Says 'bork' To Me.'''
    await ctx.send('*runs around house at top speed*')

@bot.command()
async def quiet(ctx):
    '''Tells Me To Be Quiet.'''
    await ctx.send('Loud Bark!')

@bot.command()
async def sit(ctx):
    '''Tells Me To Sit.'''
    await ctx.send('*lays*')

@bot.command()
async def lay(ctx):
    '''Tells Me To Lay Down.'''
    await ctx.send('*sits*')

@bot.command()
async def squirrel(ctx):
    '''Did Somebody Say Squirrel?!'''
    await ctx.send('OMG SQUIRREL WHAT WHERE')

@bot.command()
async def add(ctx):
  '''Add Me To A Server.'''
  await ctx.send('ENTER_INVITE_URL_HERE') #Insert your bot's URL here



# 'Cool' Command
# >cool "name" - If name is not in the list below, Knish will say "Growl..!"

@bot.group(pass_context=True)
async def cool(ctx):
    """Says If Someone Is Cool."""
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
  '''Shows Me Sleeping.'''
  await ctx.send('https://i.imgur.com/Dwr7SE2.jpg')

@bot.command()
async def god(ctx):
  '''Shows Me In My True Form.'''
  await ctx.send('https://i.imgur.com/1ALnOwp.jpg')


@bot.command()
async def alert(ctx):
  '''Shows Me Being Alert (and definately not scared).'''
  await ctx.send('https://i.imgur.com/sfmwytD.jpg')


@bot.command()
async def hello(ctx):
    '''Shows Me Being Friendly.'''
    await ctx.send('https://i.imgur.com/LOrTu7N.jpg')

@bot.command()
async def snow(ctx):
    '''Shows Me Walking Through Snow.'''
    await ctx.send('https://i.imgur.com/xYWit3A.jpg')

@bot.command()
async def sun(ctx):
  '''Shows Me Sunbathing.'''
  await ctx.send('https://i.imgur.com/ykjEPtZ.jpg')

@bot.command()
async def spotted(ctx):
  '''I've Been Seen!'''
  await ctx.send('https://i.imgur.com/6UTehGk.jpg')


bot.run('ENTER_TOKEN_HERE')
