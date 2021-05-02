# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

from Utils import Member
from Utils import Computer
import discord
from discord.ext import commands

class Shart(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def shart(self, ctx, member=None):
		"""
		[object]
		Sharts an object
		Credits to my friend Slug for the idea
		Credits to CorpNewt for Computer and Member
		"""

		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()

		nothingList = [ 'you bend down to shart and nothing comes out...']

		selfList = [	'you shart and some how it sticks on yourself', 'you try to shart but a mysterious rat sharts on you instead']

		memberList = [  'you sit on *{}*\'s face and shart on them.', 'Mooshi Mooshi Shart desu I shart on {}']
		
		itemList = [	'you shart on *{}*\'s head. *Arg.*']
		
		if member:
			m = M.displayName(ctx, member)
			if m == None:
				msg = C.text(ctx, itemList, member)
			elif m.id == ctx.author.id:
				msg = C.text(ctx, selfList, m.name)
			else:
				msg = C.text(ctx, memberList, m.name)
		else:
			msg = C.text(ctx, nothingList)

		# print(msg)
		await ctx.send(msg)

def setup(bot):
	bot.add_cog(Shart(bot))