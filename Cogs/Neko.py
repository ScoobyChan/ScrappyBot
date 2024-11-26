
import asyncio
import os
import json
import urllib.request
import requests
import discord
import aiohttp
import random
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Neko(bot, settings))

class Neko(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.options = ['8ball', 'Random_hentai_gif', 'meow', 'erok', 'lizard', 'feetg', 'baka', 'v3', 'bj', 'erokemo', 'tickle', 'feed', 'neko', 'kuni', 'femdom', 'futanari', 'smallboobs', 'goose', 'nekoapi_v3.1', 'poke', 'les', 'trap', 'pat', 'boobs', 'blowjob', 'hentai', 'hololewd', 'ngif', 'fox_girl', 'wallpaper', 'lewdk', 'solog', 'pussy', 'yuri', 'lewdkemo', 'lewd', 'anal', 'pwankg', 'nsfw_avatar', 'eron', 'kiss', 'pussy_jpg', 'woof', 'hug', 'keta', 'cuddle', 'eroyuri', 'slap', 'cum_jpg', 'waifu', 'gecg', 'tits', 'avatar', 'holoero', 'classic', 'kemonomimi', 'feet', 'gasm', 'spank', 'erofeet', 'ero', 'solo', 'cum', 'smug', 'holo', 'nsfw_neko_gif']

		if self.bot.get_cog('Perms'):
			self.bot.nsfw.append('Neko')
		


	@commands.group(pass_context=True)
	async def neko(self, ctx):
		"""[Subcom][Object]
		Neko API
		Run command to find subcommands
		"""
		coms  = ''
		for com in self.options:
			coms += '\n - '+com

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)

		desc = ''
		for c in self.options:
			desc += '\n - ' + c

		if ctx.invoked_subcommand is None:
			embed=discord.Embed(title="Neko Commands", description=desc, color=col)
			await ctx.send(embed=embed)


	
	@neko.command(name='8ball')
	async def _8ball(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/8ball')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko 8ball", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


		
	@neko.command(name='Random_hentai_gif')
	async def _Random_hentai_gif(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/Random_hentai_gif')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko Random_hentai_gif", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='meow')
	async def _meow(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/meow')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko meow", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='erok')
	async def _erok(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/erok')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko erok", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='lizard')
	async def _lizard(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/lizard')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko lizard", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='feetg')
	async def _feetg(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/feetg')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko feetg", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='baka')
	async def _baka(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/baka')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko baka", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='v3')
	async def _v3(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/v3')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko v3", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='bj')
	async def _bj(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/bj')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko bj", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='erokemo')
	async def _erokemo(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/erokemo')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko erokemo", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='tickle')
	async def _tickle(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/tickle')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko tickle", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='feed')
	async def _feed(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/feed')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko feed", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='neko')
	async def _neko(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/neko')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko neko", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='kuni')
	async def _kuni(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/kuni')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko kuni", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='femdom')
	async def _femdom(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/femdom')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko femdom", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='futanari')
	async def _futanari(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/futanari')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko futanari", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='smallboobs')
	async def _smallboobs(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/smallboobs')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko smallboobs", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='goose')
	async def _goose(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/goose')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko goose", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='nekoapi_v3.1')
	async def _nekoapi_v3(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/nekoapi_v3.1')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko nekoapi_v3.1", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='poke')
	async def _poke(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/poke')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko poke", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='les')
	async def _les(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/les')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko les", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='trap')
	async def _trap(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/trap')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko trap", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='pat')
	async def _pat(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/pat')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko pat", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='boobs')
	async def _boobs(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/boobs')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko boobs", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='blowjob')
	async def _blowjob(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/blowjob')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko blowjob", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='hentai')
	async def _hentai(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/hentai')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko hentai", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='hololewd')
	async def _hololewd(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/hololewd')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko hololewd", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='ngif')
	async def _ngif(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/ngif')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko ngif", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='fox_girl')
	async def _fox_girl(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/fox_girl')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko fox_girl", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='wallpaper')
	async def _wallpaper(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/wallpaper')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko wallpaper", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='lewdk')
	async def _lewdk(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/lewdk')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko lewdk", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='solog')
	async def _solog(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/solog')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko solog", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='pussy')
	async def _pussy(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/pussy')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko pussy", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='yuri')
	async def _yuri(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/yuri')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko yuri", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='lewdkemo')
	async def _lewdkemo(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/lewdkemo')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko lewdkemo", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='lewd')
	async def _lewd(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/lewd')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko lewd", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='anal')
	async def _anal(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/anal')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko anal", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='pwankg')
	async def _pwankg(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/pwankg')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko pwankg", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='nsfw_avatar')
	async def _nsfw_avatar(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/nsfw_avatar')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko nsfw_avatar", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='eron')
	async def _eron(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/eron')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko eron", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='kiss')
	async def _kiss(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/kiss')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko kiss", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='pussy_jpg')
	async def _pussy_jpg(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/pussy_jpg')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko pussy_jpg", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='woof')
	async def _woof(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/woof')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko woof", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='hug')
	async def _hug(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/hug')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko hug", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='keta')
	async def _keta(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/keta')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko keta", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='cuddle')
	async def _cuddle(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/cuddle')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko cuddle", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='eroyuri')
	async def _eroyuri(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/eroyuri')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko eroyuri", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='slap')
	async def _slap(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/slap')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko slap", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='cum_jpg')
	async def _cum_jpg(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/cum_jpg')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko cum_jpg", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='waifu')
	async def _waifu(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/waifu')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko waifu", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='gecg')
	async def _gecg(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/gecg')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko gecg", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='tits')
	async def _tits(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/tits')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko tits", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='avatar')
	async def _avatar(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/avatar')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko avatar", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='holoero')
	async def _holoero(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/holoero')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko holoero", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)


	
	@neko.command(name='classic')
	async def _classic(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/classic')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko classic", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)

	@neko.command(name='kemonomimi')
	async def _kemonomimi(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/kemonomimi')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko kemonomimi", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='feet')
	async def _feet(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/feet')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko feet", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='gasm')
	async def _gasm(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/gasm')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko gasm", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='spank')
	async def _spank(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/spank')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko spank", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)

	@neko.command(name='erofeet')
	async def _erofeet(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/erofeet')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko erofeet", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)

	@neko.command(name='ero')
	async def _ero(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/ero')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko ero", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='solo')
	async def _solo(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/solo')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko solo", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='cum')
	async def _cum(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/cum')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko cum", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='smug')
	async def _smug(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/smug')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko smug", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)

	@neko.command(name='holo')
	async def _holo(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/holo')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko holo", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)
	
	@neko.command(name='nsfw_neko_gif')
	async def _nsfw_neko_gif(self, ctx):
		data = requests.get('https://nekos.life/api/v2/img/nsfw_neko_gif')
		data = data.json()['url']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)
		
		embed=discord.Embed(title="Neko nsfw_neko_gif", color=col)
		embed.set_image(url=data)
		await ctx.send(embed=embed)