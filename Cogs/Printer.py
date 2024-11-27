import time
import random
import discord
from discord.ext import commands
from discord.utils import get


class Printer(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def print(self, ctx, url=None):
		"""
		[url]
		Prints the image into an embed
		"""
		if search[:5] == 'https' or search[:4] ==  'http' or search[:3] ==  'www': 
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col = random.choice(self.bot.color)

			embed=discord.Embed(color=col)
			embed.set_image(url=url)
			await ctx.send(embed=embed)
		else:
			return await ctx.send('Url is not Valid')

	@commands.command()
	async def printavi(self, ctx, user=None):
		"""
		[user(optional)]
		prints the users avatar in an embed
		"""
		""""""

		if not user:
			u = ctx.author
		else:
			if not self.settings.Get(ctx, 'user', user):
				return await ctx.send(f'**{user}** is not found')

			u = self.settings.Get(ctx, 'user', user)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)

		embed=discord.Embed(title=f"{u.name}'s Avartar", color=col)
		embed.set_image(url=f'https://cdn.discordapp.com/avatars/{u.id}/{u.avatar}.webp?size=1024')
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Printer(bot))