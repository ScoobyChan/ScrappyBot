import asyncio
import discord
from discord.ext import commands 


class Purge(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def purge(self, ctx, channel: discord.TextChannel = None , user: discord.Member=None, limit:int=None):
		if not channel: channel = ctx.channel

		if not limit:
			limit = 1

		channel = self.bot.get_channel(ch)

		def is_me(m):
			if user:
				return m.author == user
			else:
				return True

		deleted = await channel.purge(limit=limit, check=is_me)
		await channel.send('Deleted **{}** message(s){}'.format(len(deleted), "for **`{}`**".format(user.name) if user else ""))

def setup(bot):
	bot.add_cog(Purge(bot))