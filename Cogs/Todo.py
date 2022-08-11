
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Todo(bot, settings))

class Todo(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def todo(self, ctx):
		"""Lists what I have left to do"""
		await ctx.send('''To make:
				XP
				About Me
				Rate limit?
				Define between Admins(Role) and Admins(Perms) and Server owner
				Admin Override(Perms and Server owner) for NSFW - Disable NSFW items if disabled and not NSFW channel - Add warning about TOS
				NSFW override - dont care about anything
				Fix/test Perms
				Logging 
				Maintainence Notifier
				Redo Settings
				Telephone
					Webhooks
				Invite remover
				Booster Role
				Channel limiter
				Check if Server available? || Location for Minecraft server
				Wiki search/definer
				Voting system
				Role Selector
				Spotify API
				Tag Permissions
				Run on linux
					Remake Time Module
					Installation Module
				Spooktober
				Rework Currency
				Fix Reboot sequence
				Fuzzy search to find users
				ignore users
				Monitor
				Debug
				Role play webhook
				Regex
					Checker
					Tester
					Match n Mute

				Roleadd as function in temp
				''')