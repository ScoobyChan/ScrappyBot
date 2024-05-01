import json
import urllib.request
import discord
import random
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Anime(bot, settings))

class Anime(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		
		if self.bot.get_cog('Perms'):
			self.bot.nsfw.append('Anime')
		

	@commands.group(pass_context=True)
	async def waifu(self, ctx):
		""" [nsfw/sfw][object]
		Used to send different images of waifu's
		"""
		if ctx.invoked_subcommand is None:
			await ctx.send('Missing  Sub command of sfw or nsfw. eg {0.prefix}waifu sfw '.format(ctx))

	@commands.is_nsfw()
	@waifu.command()
	async def nsfw(self, ctx, _cat=None):
		cat = ['waifu','neko','trap','blowjob']
		with urllib.request.urlopen("https://waifu.pics/api/{}/{}".format('nsfw', random.choice(cat) if not _cat in cat else _cat)) as url:
			data = json.loads(url.read().decode())
			data = data['url']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Waifu NSFW", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)

	@waifu.command()
	async def sfw(self, ctx, _cat=None):
		cat = ['waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','smile','wave','highfive','handhold','nom','bite','glomp','kill','slap','happy','wink','poke','dance','cringe','blush']
		with urllib.request.urlopen("https://waifu.pics/api/{}/{}".format('sfw', random.choice(cat) if not _cat in cat else _cat)) as url:
			data = json.loads(url.read().decode())
			data = data['url']

			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
			
			embed=discord.Embed(title="Waifu SFW", color=col)
			embed.set_image(url=data)
			await ctx.send(embed=embed)