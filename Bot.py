import Settings
import Intents

from Utils import Configuration

import Startup
Startup.prereq()

import os
import time
import discord
from discord.ext import commands
import asyncio

async def get_pre(bot, message):
	guild = message.guild.id
	set_cog = bot.get_cog('Settings')
	if set_cog:
		return set_cog.ServerConfig(guild, 'Prefix')
	else:
		return Settings.prefix

allowed_mentions = discord.AllowedMentions(
	users=False,
	everyone=False,
	roles=False,
	replied_user=False
)

Bot = discord.Client()
bot = commands.Bot(command_prefix=get_pre, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, intents=Intents.intents, allowed_mentions=allowed_mentions)
Conf = Configuration.Configuration(bot)

# # use AutoShared for more than 5 servers
# # bot = commands.AutoShardedBot(command_prefix=get_pre, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, shard_count=6)

# # use this for initialising the Bot but only use for under 5 servers.
# bot = commands.Bot(command_prefix=get_pre, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, intents=intents)

# Spotify Use
bot.wavepass = Settings.PassWavelink
bot.spotcli = Settings.spotcli
bot.spotsec = Settings.spotsec

bot.OWM = Settings.OWM

bot.color = [
	discord.Color.teal(), 
	discord.Color.dark_teal(), 
	discord.Color.green(),
	discord.Color.dark_green(),
	discord.Color.blue(),
	discord.Color.dark_blue(),
	discord.Color.purple(),
	discord.Color.dark_purple(),
	discord.Color.magenta(),
	discord.Color.dark_magenta(),
	discord.Color.gold(),
	discord.Color.dark_gold(),
	discord.Color.orange(),
	discord.Color.dark_orange(),
	discord.Color.red(),
	discord.Color.dark_red(),
	discord.Color.lighter_grey(),
	discord.Color.dark_grey(),
	discord.Color.light_grey(),
	discord.Color.darker_grey(),
	discord.Color.blurple(),
	discord.Color.greyple()
]

bot.res = time.localtime()
bot.debug = False


@bot.event
async def on_ready():
	if not bot.get_cog("CogLoader"):
		# for g in self.bot.guilds:
		# 	Configuration.Configuration(bot).UpdateJson(g.id)

		print("Loading cog loader")
		if not bot.get_cog('Settings'):
			if os.path.exists('Cogs/Settings.py'):
				bot.load_extension("Cogs.Settings")
		
		if not bot.get_cog("CogLoader"):
			# CogLoader
			try:
				bot.load_extension("Cogs.Cogloader")
				cg_load = bot.get_cog('Cogloader')
				cg_load._load_extension()
				
				# Make sure Bot is Loaded fully
				await bot.wait_until_ready()
				cg_load.loaded()
			except:
				print('Cogloader already loaded')


@bot.event
async def on_typing(channel, user, when):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates ontyping function if it exists
			await cog.ontyping(channel, user, when)
		except AttributeError:
			continue

@bot.event
async def on_message(message): # Need to fix this
	# Post the context too
	context = await bot.get_context(message)
	bot.dispatch("message_context", context, message)

	if not message.guild:
		# This wasn't said in a server, process commands, then return
		await bot.process_commands(message)
		return

	if message.author.bot:
		# We don't need other bots controlling things we do.
		return

	try:
		message.author.roles
	except AttributeError:
		# Not a User
		await bot.process_commands(message)
		return
	
	# Check if we need to ignore or delete the message
	# or respond or replace
	
	ignore = delete = react = respond = False
	x = False

	check = None

	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			try:	
				check = await cog.onmessage(message)
			except TypeError as e:
				if bot.debug: print(cog); print(type(message)); print(message)
				print('########## Big error :P #############')
				print(e)
	
		except AttributeError:
			# Onto the next
			continue
		# Make sure we have things formatted right

		if not type(check) is dict:
			check = {}
		if check.get("Delete",False):
			delete = True
		if check.get("Ignore",False):
			ignore = True
		try: respond = check['Respond']
		except KeyError: pass
		try: react = check['Reaction']
		except KeyError: pass
	
	if delete:
		# We need to delete the message - top priority
		await message.delete()

	if not ignore:
		# We're processing commands here
		if respond:
			# We have something to say
			await message.channel.send(respond)
		if react:
			# We have something to react with
			for r in react:
				await message.add_reaction(r)
		await bot.process_commands(message)

@bot.event
async def on_guild_join(message):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onguildjoin(message)
		except AttributeError:
			continue

@bot.event
async def on_guild_remove(message):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onguildremove(message)
		except AttributeError:
			continue

@bot.event
async def on_member_join(message):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onmemberjoin(message)
		except AttributeError:
			continue

@bot.event
async def on_member_remove(message):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onmemberremove(message)
		except AttributeError:
			continue

@bot.event
async def on_raw_reaction_add(payload):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onrawreactionadd(payload)
		except AttributeError:
			continue

def BotConfig(setting, passback=None):
	l = Conf.LoadConfigBot()
	_set = l.get(setting, 'not_found')
	if _set == 'not_found':
		raise commands.DisabledCommand(f'Can not find {setting}')

	if not passback:
		return _set

	l[setting] = passback

	Conf.SaveConfigBot(l)

while True:
	reboot = BotConfig('reboot')

	if reboot:
		try:	
			# Initialise Mass Destruction
			if Settings.token:
				BotConfig('reboot', False)
				bot.run(Settings.token, bot=True, reconnect=True)
			else:
				print('I have no TOKEN')
				break
		except discord.errors.HTTPException:
			print('Connection issues, waiting 30secs')
			time.sleep(30)

		except RuntimeError:
			print('Exiting by keyboard')
			exit()
	else:
		print('Quitting Bot')
		BotConfig('reboot', True)
		break
