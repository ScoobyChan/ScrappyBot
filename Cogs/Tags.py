from Utils import Configuration
import time
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Tags(bot, settings))

class Tags(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

		self.Conf = Configuration.Configuration(bot)

	@commands.command()
	async def taginfo(self, ctx, tag=None):
		"""[tag]
		Shows info """
		Tags = self.settings.ServerConfig(ctx.guild.id, Tags)
		Res = fuz.fuzSearch(ctx, tag, Tags)

		_user = self.settings.Get(ctx, 'user', Tags[Res]['user'])

		await ctx.send('Last Edited by {} on {}'.format(_user, Tags[Res]['time']))

	@commands.command(alias='tag')
	async def tags(self, ctx, tag=None):
		"""[tag]
		gets a tag with all the info for it """
		num = 0
		Tags = self.settings.ServerConfig(ctx.guild.id, 'Tags')
		fuz = self.bot.get_cog('FuzzySearch')
		if not fuz:
			return await ctx.send('Can\'t find FuzzySearch Cog')

		Res = fuz.fuzSearch(ctx, tag, Tags)

				
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = Res[num],
			description = Tags[Res]['data'],
			colour = col
		)
		embed.set_footer(text='Last Edited {}'.format(Tags[Res]['time']))
		await ctx.send(embed=embed)

	@commands.command()
	async def addtags(self, ctx, tag, *, data):
		"""[Tag name][data]
		Adds or edits a tag
		"""
		Tag = self.settings.ServerConfig(ctx.guild.id, 'Tags')
		if not tag in Tag:
			Tag[tag] = self.Conf.Tags
			await ctx.send('Added Tag: {}'.format(tag))
		else:
			await ctx.send('Edited Tag: '.format(tag))

		Tag[tag]['user'] = ctx.author.id
		Tag[tag]['data'] = data
		Tag[tag]['time'] = '{}:{}, {}/{}/{}'.format(local[3], local[4], local[2], local[1], local[0])
		self.settings.ServerConfig(ctx.guild.id, 'Tags', Tag)

	@commands.command()
	async def addtagrole(self, ctx, _role):
		"""[role]
		Adds the role to the tag role so that users with the role add items to database
		"""
		if _role == 0:
			self.settings.ServerConfig(ctx.guild.id, 'TagRole', 0)
			await ctx.send('Tag role set to: {}'.format(0))
		else:	
			role = self.settings.Get(ctx, 'role', _role)
			if not role: return await ctx.send('Can\'t find role: {}'.format(_role))

			self.settings.ServerConfig(ctx.guild.id, 'TagRole', role.id)
			await ctx.send('Tag role set to: {}'.format(role))

	@commands.command()
	async def tagrole(self, ctx):
		"""
		Displays what role is needed to use addTags. Admins have override
		"""
		role = self.settings.Get(ctx, 'role', self.settings.ServerConfig(ctx.guild.id, 'TagRole'))
		if not role: return await ctx.send('Can\'t find role: {}'.format(role))
		await ctx.send('Tag role set to: {}'.format(role))

	@commands.command()
	async def removetags(self, ctx, tag=None):
		"""[tag]
		Used to remove the tag
		"""
		Tag = self.settings.ServerConfig(ctx.guild.id, 'Tags')
		if not tag in Tag:
			return await ctx.send('Can\'t find Tag: '.format(tag))	

		del Tag[tag]
		self.settings.ServerConfig(ctx.guild.id, 'Tags', Tag)

		await ctx.send('Removed Tag: '.format(tag))