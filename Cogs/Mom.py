
import discord
from discord.ext import commands

def setup(bot):
	bot.add_cog(Mom(bot))

class Mom(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Add Message Checker like No u and honk

	@commands.command(aliases=['mom', 'mum'])
	async def urmom(self, ctx):
		"""Sends out ur mom"""
		await ctx.send('**Ur mom**')