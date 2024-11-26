import random
import discord
from discord.ext import commands

class Dice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def dice(self, ctx, d=6, t=1):
		""" 
		[Dice Size] [Rolls(Optional)]
		This Command Rolls a Dice 1 or more times that ranges from size 6 - 20 sided
		"""

		if not d > 0:
			return await ctx.send('Number is too small for a dice')


		D = 'You have choosen to roll a **d'+str(d)+'**'
		for i in range(0,t):	
			r = random.randint(1,d)
			D += 'You have rolled a: **' + str(r) + '**'

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = random.choice(self.bot.color)

		embed = discord.Embed(
			description = D,
			colour = col
		)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Dice(bot))