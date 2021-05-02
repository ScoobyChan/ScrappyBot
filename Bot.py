# Credits from CorpBot and CorpNewt

# Discord Bot to do:
# Lock down
# Anti raid
# Minecraft?
# Links - Tomorrow
# Role Selection
# Rework  Reboot , Shutdown
# App Info - https://discordpy.readthedocs.io/en/latest/api.html#discord.AppInfo | Check info.py for help (find BO)

# EFI Creator

# REWORK BOT From scratch
# Sudo = Admin
# Dry-run

import json
import os
import json 
import asyncio
import time
import shlex

from ast import literal_eval
from io import StringIO
import yaml

from Utils import Configuration

import discord
from discord.ext import commands


#Loads the TOKEN
imp = 'Json/'
if os.path.exists(imp + 'BotSettings.yaml'):
	with open(imp + 'BotSettings.yaml') as t:
		t = yaml.load(t, Loader=yaml.FullLoader)
		PREFIX = t['Prefix']
		TOKEN = t['Token']
		OWM = t['OWM']
		MINECRAFT = t['Minecraft_IP']
		GIPHY_API = t['GIPHY']
		wavepass = t['PassWavelink']
		repo = t.get('Repo', None)
		FixerAPI = t['FixerAPI']
else:
	PREFIX = '$'
	TOKEN = ''
	MINECRAFT = 'None'
	GIPHY_API = ''
	OWN = ''
	wavepass = ''
	repo = ''
	FixerAPI = ''

async def get_pre(bot, message):
	guild = message.guild.id
	set_cog = bot.get_cog('Settings')
	if set_cog:
		return set_cog.ServerConfig(guild, 'Prefix')
	else:
		return PREFIX

intents = discord.Intents.all()
Bot = discord.Client()

# use AutoShared for more than 5 servers
bot = commands.AutoShardedBot(command_prefix=PREFIX, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, shard_count=6, intents=intents)

# use this for initialising the Bot but only use for under 5 servers.
# bot = commands.Bot(command_prefix=get_pre, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, intents=intents)

bot.minecraft = MINECRAFT
bot.GIPHY_API = GIPHY_API
bot.OWM = OWM
bot.wavepass = wavepass
bot.repo = repo
bot.FixerAPI = FixerAPI

time.sleep(0.1)

bot.color = {"teal": discord.Color.teal(),
	"dark_teal": discord.Color.dark_teal(),
	"green": discord.Color.green(),
	"dark_green": discord.Color.dark_green(),
	"blue": discord.Color.blue(),
	"dark_blue": discord.Color.dark_blue(),
	"purple": discord.Color.purple(),
	"dark_purple": discord.Color.dark_purple(),
	"magenta": discord.Color.magenta(),
	"dark_magenta": discord.Color.dark_magenta(),
	"gold": discord.Color.gold(),
	"dark_gold": discord.Color.dark_gold(),
	"orange": discord.Color.orange(),
	"dark_orange": discord.Color.dark_orange(),
	"red": discord.Color.red(),
	"dark_red": discord.Color.dark_red(),
	"lighter_grey": discord.Color.lighter_grey(),
	"dark_grey": discord.Color.dark_grey(),
	"light_grey": discord.Color.light_grey(),
	"darker_grey": discord.Color.darker_grey(),
	"blurple": discord.Color.blurple(),
	"greyple": discord.Color.greyple()
}

bot.res = time.localtime()

@bot.event
async def on_ready():
	# Settings
	loc = 'Cogs/'
	err = 0
	if os.path.exists(loc+'Settings.py'):
		bot.load_extension("Cogs.Settings")
		sett = bot.get_cog('Settings')
		err = sett.BotConfig('ErrorChannel')
	
	Conf = Configuration.Configuration(bot)

	# Fix Syncing
	Conf.UpdateJson()

	if not bot.get_cog("CogLoader"):
		# CogLoader
		bot.load_extension("Cogs.CogLoader")
		cg_load = bot.get_cog('CogLoader')
		cg_load._update()
		cg_load._load_extension()
	
	# Make sure Bot is Loaded fully
	await bot.wait_until_ready()
	
	# PyBot
	time.sleep(1)
	# input('[ Enter ]')
	cg_load.loaded()

	if err != 0:
		ch = bot.get_channel(err)
		await ch.send('I am back mystery crew')

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
async def on_message(message):
	if message.author.bot:
		return

	# Post the context too
	context = await bot.get_context(message)
	bot.dispatch("message_context", context, message)
	
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			check = await cog.onmessage(message)
		except AttributeError:
			# Onto the next
			continue

	await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onguildjoin(guild)
		except AttributeError:
			continue

@bot.event
async def on_guild_remove(guild):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onguildremove(guild)
		except AttributeError:
			continue

@bot.event
async def on_member_join(member):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onmemberjoin(member)
		except AttributeError:
			continue

@bot.event
async def on_member_remove(member):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			# Initiates onmessage function if it exists
			await cog.onmemberremove(member)
		except AttributeError:
			continue

while True:
	try:	
		# Initialise Mass Destruction
		if TOKEN:
			bot.run(TOKEN, bot=True, reconnect=True)
		else:
			print('I have no TOKEN')
			break
	except discord.errors.HTTPException:
		print('Connection issues, waiting 30secs')
		time.sleep(30)

	except RuntimeError:
		print('Shutting down by keyboard')
		break