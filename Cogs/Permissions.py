from Utils import Utils
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Permissions(bot, settings))

class Permissions(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.Utils = Utils.Utils()

	@commands.command()
	async def roleperm(self, ctx, role: discord.Role = None):
		"""[role]
		Lists the permissions for the role"""
		if not role: 
			return await ctx.send('Missing or cannot find the Role')

		perms = [x for x in role.permissions]

		desc = ''
		for p, t in perms:
			desc += f'**{p}**: `{t}`\n'

		col = ctx.author.top_role.colour
		embed = self.Utils.embed({"title":"Role Permissions", "desc":f"{role.mention}\n{desc}", "color":col})		
		await ctx.send(embed=embed)

	@commands.command()
	async def userperm(self, ctx, member: discord.Member = None):
		"""[member]
		Lists the permissions for the member"""
		if not member: 
			member = ctx.author

		perms = [x for x in member.guild_permissions]

		desc = ''
		for p, t in perms:
			desc += f'**{p}**: `{t}`\n'

		col = ctx.author.top_role.colour
		embed = self.Utils.embed({"title":"User Permissions", "desc":f"User: {member.mention}\n{desc}", "color":col, "thumb":member.avatar_url})		
		await ctx.send(embed=embed)

	@commands.command()
	async def voiceperm(self, ctx, channel: discord.VoiceChannel = None, member: discord.Member = None):
		"""[channel][member(optional)]
		Lists the permissions for the member for the Voice Channel"""

		if not channel: 
			return await ctx.send('Missing Voice Channel')

		if not member:
			member = ctx.author
			
		perms = [x for x in channel.permissions_for(member)]

		desc = ''
		for p, t in perms:
			desc += f'**{p}**: `{t}`\n'

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col = self.settings.randomColor()

		embed = self.Utils.embed({"title":f"Voice Channel Permissions for {member.name}", "desc":f"User Permissions for {channel.mention}\n{desc}", "color":col, "thumb":member.avatar_url})
		await ctx.send(embed=embed, delete_after=15)

	@commands.command()
	async def textperm(self, ctx, channel: discord.TextChannel = None, member: discord.Member = None):
		"""[channel][member(optional)]
		Lists the permissions for the member for the Voice Channel"""
		
		if not channel: 
			return await ctx.send('Missing Text Channel')

		if not member:
			member = ctx.author

		perms = [x for x in channel.permissions_for(member)]

		desc = ''
		for p, t in perms:
			desc += f'**{p}**: `{t}`\n'
		
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = self.Utils.embed({"title":f"Text Channel Permissions for {member.name}", "desc":f"User Permissions for {channel.mention}\n{desc}", "color":col, "thumb":member.avatar_url})
		await ctx.send(embed=embed, delete_after=15)