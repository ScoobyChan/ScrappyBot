import discord
from discord.ext import commands

from Utils import Utils

class Invite(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils

	@commands.command()
	async def Invite(self, ctx):
		"""
		Sends an Invite URL for the bot
		Highly suggests having admin as perms
		"""
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()
			
		embed=discord.Embed(title="Invite this Joyful Bot", description="Small But Smoler", color=col)
		embed.set_author(name="self.bot.is_owner(ctx.author)", url="https://github.com/ScoobyChan/", icon_url="https://9b16f79ca967fd0708d1-2713572fef44aa49ec323e813b06d2d9.ssl.cf2.rackcdn.com/1140x_a10-7_cTC/scooby-1552600726.jpg")
		embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/p__/images/8/8f/Scrappy-Doo_promo.png/revision/latest?cb=20180311032506&path-prefix=protagonist")
		embed.add_field(name="Invite Link", value='https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n'.format(self.bot.user.id), inline=False)
		embed.set_footer(text="Just another Bot")
		await ctx.send(embed=embed)

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
	settings = bot.get_cog("Settings")
	bot.add_cog(Invite(bot, settings))