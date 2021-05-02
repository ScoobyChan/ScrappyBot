import time
import discord
from discord.ext import commands

class Ping(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		"""
		Ping response
		"""
		t1 = time.perf_counter()
		await ctx.trigger_typing()
		t2 = time.perf_counter()
		ms = round((t2-t1) * 1000)
		await ctx.send(content='**Pong!** <@{}> - {}ms'.format(ctx.author.id, int(ms)))

	@commands.command()
	async def invite_test(self, ctx):
		member = ctx.author
		guild = ctx.guild
		invite = 'https://discord.gg/JRwXCd7'
		c = await self.bot.fetch_invite(invite)

		embed=discord.Embed(title="{0}({0.id}) has joined {1}".format(member, guild), color=discord.Color.dark_blue())
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name="Invite URL:", value=c.url, inline=False)
		if c.created_at:
			embed.add_field(name="Created at:", value=c.created_at, inline=True)
		embed.add_field(name="Created By", value=c.inviter, inline=True)
		if c.max_age:	
			embed.add_field(name="Expires:", value=c.max_age, inline=False)
		embed.add_field(name="Pointed to channel:", value=c.channel, inline=True)
		embed.add_field(name="Temporary", value=c.temporary if c.temporary else "False", inline=True)
		embed.add_field(name="For Guild:", value=c.guild, inline=True)
		if c.max_uses != 0 and c.max_uses:
			embed.add_field(name="Uses", value="{}/{}".format(0 if not c.uses else c.uses, c.max_uses), inline=True)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Ping(bot))