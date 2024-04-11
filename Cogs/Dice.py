import random
import discord
from discord.ext import commands

class Dice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def dice(self, ctx, d:int=6, t:int=1):
		""" 
		[Dice Size] [Rolls(Optional)]
		This Command Rolls a Dice 1 or more times that ranges from size 2 - big sided
		"""

		if not d > 2:
			return await ctx.send('Number is invalid for dice size pick a number bigger than 1')


		D = 'You have choosen to roll a **d'+str(d)+'**'
		for i in range(0,t):	
			r = random.randint(1,d)
			D += 'You have rolled a: **' + str(r) + '**'

		col = ctx.author.top_role.colour if ctx.author.top_role.colour else random.choice(self.bot.color)

		embed = discord.Embed(
			description = D,
			colour = col
		)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Dice(bot))