import asyncio
import discord
from discord.ext import commands

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Question(bot, settings))

class Question(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def question(self, ctx, *, message):
		"""[Question to ask]
		Asks a question for someone to answer"""
		await ctx.message.delete()
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			description = message,
			colour = col
		)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")

		def check(reaction: discord.Reaction, adder: discord.User) -> bool:
			return reaction.message.id == msg.id and adder != self.bot.user

		try:
			reaction, adder = await self.bot.wait_for('reaction_add', timeout=20, check=check)
		except asyncio.exceptions.TimeoutError:
			await msg.delete()
			await ctx.send('Question timed out')
			return

		if reaction.emoji == '✅':
			choice = "Yes"

		if reaction.emoji == '❌':
			choice = "No"

		await msg.delete()  
		embed = discord.Embed(
			description = "**{}** picked the answer: {}".format(adder, choice),
			colour = col
		)
		msg = await ctx.send(embed=embed)	
		