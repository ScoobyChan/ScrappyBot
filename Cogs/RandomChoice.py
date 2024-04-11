import random
import discord
from discord.ext import commands

class RandomChoice(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot

	@commands.command()
	async def dice(self, ctx, size:int=6, roll:int=1):
		""" 
		This Command Rolls a Dice 1 or more times that ranges from size 2 - 100 sided
		"""

		if not size > 2 and roll < 101:
			return await ctx.send('Number is invalid for dice size pick a number bigger than 1 and less than or equal to 100')


		D = 'You have choosen to roll a **d'+str(size)+'**'
		for i in range(0,roll):	
			r = random.randint(1,size)
			D += '\nYou have rolled a: **' + str(r) + '**'

		col = ctx.author.top_role.colour if ctx.author.top_role.colour else random.choice(self.bot.color)

		embed = discord.Embed(
			description = D,
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def randomnumber(self, ctx, rand_num:int=2):
		""" 
		This Command picks a random number for you
		"""

		if not rand_num > 2 and d < 101:
			return await ctx.send('Number is invalid for dice size pick a number bigger than 1')

		col = ctx.author.top_role.colour if ctx.author.top_role.colour else random.choice(self.bot.color)
		
		r = random.randint(1,rand_num)
		D = "Your random number is: " + str(r)

		embed = discord.Embed(
			description = D,
			colour = col
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def coinflip(self, ctx):	
		coin = ["Heads", "Tails"]
		coin_flip = random.choice(coin)
		
		col = ctx.author.top_role.colour if ctx.author.top_role.colour else random.choice(self.bot.color)
		
		D = "You flipped a coin and it landed on: " + coin_flip

		embed = discord.Embed(
			description = D,
			colour = col
		)
		await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(RandomChoice(bot, settings))