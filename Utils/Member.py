import discord
from discord.ext import commands 

class member:
	def displayName(self, ctx, member):
		if member:
			try:
				member = member.strip('<>@!')
				m = int(member)
				m = discord.utils.get(ctx.guild.members, id=m)
				return m
			except:
				pass

			try:
				m = str(member)
				m = discord.utils.get(ctx.guild.members, name=m)
				return m
			except:
				pass

	def Channels(self, ctx, member):
		member = str(member)
		if member:
			member = member.strip('<>#!')
			try:
				m = int(member)
				m = discord.utils.get(ctx.guild.channels, id=m)
				return m
			except:
				pass

