import discord
from discord.ext import commands
import logging


description = '''Knish The Dog In Bot Form.
Please Use All Lowercase Letters.'''
bot = commands.Bot(command_prefix='>', description=description)
logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
	await bot.change_presence(game=discord.Game(name="over my family | >help", type=3), status=discord.Status("online"))
	#0=Playing 1=Streaming 2=Listening 3=Watching
	print('')
	print('------')
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
	print('------')
	print('Running API Version: ' + discord.__version__)
	print('------')
	print('')



# General Commands

@bot.command()
async def hi():
	'''Say Hi To Me.'''
	await bot.say('Woof!')
	
@bot.command()
async def aww():
	'''Basicly saying I'm Cute.'''
	await bot.say('Happy Woof!')
	
@bot.command()
async def bork():
	'''Says 'bork' To Me.'''
	await bot.say('*runs around house at top speed*')
	
@bot.command()
async def quiet():
	'''Tells Me To Be Quiet.'''
	await bot.say('Loud Bark!')
	
@bot.command()
async def sit():
	'''Tells Me To Sit.'''
	await bot.say('*lays*')
	
@bot.command()
async def lay():
	'''Tells Me To Lay Down.'''
	await bot.say('*sits*')
	
@bot.command()
async def squirrel():
	'''Did Somebody Say Squirrel?!'''
	await bot.say('OMG SQUIRREL WHAT WHERE')
	
@bot.command()
async def add():
  '''Add Me To A Server.'''
  await bot.say('https://discordapp.com/api/oauth2/authorize?client_id=413728059645100039&permissions=36957248&scope=bot')
  
  
  
# 'Cool' Command

@bot.group(pass_context=True)
async def cool(ctx):
	"""Says If Someone Is Cool."""
	if ctx.invoked_subcommand is None:
		await bot.say('Growl..!'.format(ctx))


@cool.command(name='knish')
async def _bot():
	await bot.say('*Happy Bork!*')


@cool.command(name='alex')
async def _bot():
	await bot.say('*Happy Bork!*')


@cool.command(name='davati')
async def _bot():
	await bot.say('*Happy Bork!*')


@cool.command(name='whatever you want to say')
async def _bot():
	await bot.say('Growl..!')



# Photos Below
	
@bot.command()
async def sleep():
  '''Shows Me Sleeping.'''
  await bot.say('https://i.imgur.com/Dwr7SE2.jpg')
	
@bot.command()
async def god():
  '''Shows Me In My True Form.'''
  await bot.say('https://i.imgur.com/1ALnOwp.jpg')


@bot.command()
async def alert():
  '''Shows Me Being Alert (and definately not scared).'''
  await bot.say('https://i.imgur.com/sfmwytD.jpg')


@bot.command()
async def hello():
	'''Shows Me Being Friendly.'''
	await bot.say('https://i.imgur.com/LOrTu7N.jpg')

@bot.command()
async def snow():
	'''Shows Me Walking Through Snow.'''
	await bot.say('https://i.imgur.com/xYWit3A.jpg')
	
@bot.command()
async def sun():
  '''Shows Me Sunbathing.'''
  await bot.say('https://i.imgur.com/ykjEPtZ.jpg')

@bot.command()
async def spotted():
  '''I've Been Seen!'''
  await bot.say('https://i.imgur.com/6UTehGk.jpg')


bot.run('INSERT_TOKEN_HERE')
