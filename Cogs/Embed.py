import discord
from discord.ext import commands

class Embed(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	def _embed(self, footer, header, image, thumbnail, author, color, description):
		pass

	@commands.command()
	async def testEmbed(self, ctx):
		"""
		Tests Embed format
		"""

		# Make universal function

		# Title
		# Type
		# Description
		# Url
		# Color
		# Footer
		# Image
		# Thumbnail
		# Video
		# Provider
		# Author
		# Fields
		# delete after
		# max chars
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'Title',
			description = 'This is a **description**',
			colour = discord.Color.blue()
		)
		# \n```md\n[test][test]\n<Testing this>\n```
		embed.set_footer(text='Footer')
		embed.set_image(url='https://cdn.discordapp.com/attachments/476978593528807437/672658069997617153/GooseDance.gif')
		embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/476978593528807437/672658063756492822/Meme3.png')
		embed.set_author(name='Author of this Junk', icon_url='https://cdn.discordapp.com/attachments/476978593528807437/672658051165061130/Meme1.png')
		await ctx.send(embed=embed)

	@commands.command()
	async def embed(self, ctx, *, desc=None):
		"""
		[Input]
		Adds what you want into an Embed
		"""
			
		if desc:
			await ctx.message.delete()
			if ctx.author.top_role.colour:
				col = ctx.author.top_role.colour
			else:
				col =self.settings.randomColor()
				
			embed = discord.Embed(
				description = desc,
				colour = col
			)
			await ctx.send(embed=embed)

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Embed(bot, settings))