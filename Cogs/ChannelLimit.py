# Global
# - channels
# Image only:
# - allow text with attachment
# Text only:
# - allow attachment with text
import asyncio
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(ChannelLimit(bot, settings))

class ChannelLimit(commands.Cog):
	def __init__(self, bot, settings):
		self.settings = settings
		self.bot = bot
		self.defaultChann = {"txt":None,"img":None,"txt_img":None, "txt_img_or_img":None}
		
	async def onmessage(self, message):
		SettingJson = self.settings.LoadSettings()
		if type(message.channel) == discord.DMChannel:
			return


		if channels == 0:
			return

		self.text_img = channels.get("txt_img", None)
		self.img = channels.get("img", None)
		self.text = channels.get("txt", None)
		self.img_or_text_img = channels.get("txt_img_or_img", None)

		if message.author.id == self.bot.user.id:
			return 	

		if self.img_or_text_img:
			if not message.content and not message.attachments or not message.attachments:
				await message.delete()

		if self.text_img:
			if not message.content and not message.attachment:
				await message.delete()
		
		if self.text:
			if message.attachments:
				await message.delete()
		
		if self.img:
			if message.content:
				await message.delete()

	def ResetChannel(self, ctx, channel=None):
		SettingJson = self.settings.LoadSettings()
			
		if type(ctx.channel) == discord.DMChannel:
			return

		if not channel:	
			channel = ctx.channel

		channels = SettingJson.get('Server', {}).get(str(ctx.guild.id), {}).get('ChannelContent', {}).get(str(channel.id), None)
		if channels != None:
			for c in SettingJson.get('Server', {}).get(str(ctx.guild.id), {}).get('ChannelContent', {}).get(str(channel.id), {}):
				SettingJson['Server'][str(ctx.guild.id)]['ChannelContent'][str(channel.id)][c] = None

		self.settings.SaveSettings(SettingJson)

	@commands.command()
	async def setChannelLimitSettings(self, ctx, channel=None):
		"""[Channel (Optiona;)] Channel Content Settings"""
		if type(ctx.channel) == discord.DMChannel:
			return

		if not channel:	
			channel = ctx.channel
		
		SettingJson = self.settings.ServerConfig(ctx.guild.id, 'ChannelContent')
		channels = SettingJson.get(str(channel.id), None)
		if channels == None:
			SettingJson[str(channel.id)] = self.defaultChann

		try:
			msg = await ctx.send(f'Channel Content Options for **{channel}**:\n```\n1 - Text Only\n2 - Images only\n3 - Images with text only\n4 - Images or Images with text only\n5 - Reset\n🚫 - Cancel\n```')

			await msg.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
			await msg.add_reaction('\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
			await msg.add_reaction('\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
			await msg.add_reaction('\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}')
			await msg.add_reaction('\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}')
			await msg.add_reaction('🚫')

			def check(reaction: discord.Reaction, adder: discord.User) -> bool:
				return adder == ctx.message.author and reaction.message.id == msg.id

			reaction, adder = await self.bot.wait_for('reaction_add', check=check, timeout=10)

			if reaction.emoji == '1⃣':
				choice = 'txt'

			elif reaction.emoji == '2⃣':
				choice = 'img'

			elif reaction.emoji == '3⃣':
				choice = 'txt_img'

			elif reaction.emoji == '4⃣':
				choice = 'txt_img_or_img'

			elif reaction.emoji == '5⃣':
				choice = 'reset'

			elif reaction.emoji == '🚫':
				await msg.delete()  
				await ctx.send('Search has been cancelled')
				return

			if choice == 'reset':
				if channels != None:
					del SettingJson[str(channel.id)]
			else:
				self.ResetChannel(ctx, channel)
				SettingJson[str(channel.id)][choice] = True

			self.settings.ServerConfig(ctx.guild.id, 'ChannelContent', SettingJson)

			await msg.delete()
			await ctx.send('Settings Updated Channel **' + str(channel) + '** to: ** ' + choice + ' **')
		except asyncio.TimeoutError:
			await ctx.send('Selection Timeout')
			await msg.delete()

	@commands.command()
	async def checkChannelLimit(self, ctx, ch=None):
		"""
		[channel(if not will do current channel)]
		Checks the channel limits for selected channel
		"""			
		if type(ctx.channel) == discord.DMChannel:
			return

		channel = self.settings.Get(ctx, 'channel', ch)
		if not channel:
			channel = ctx.channel

		SettingJson = self.settings.LoadSettings()
		channels = SettingJson.get('Server', {}).get(str(ctx.guild.id), {}).get('ChannelContent', {}).get(str(channel.id), {})
		msg = await ctx.send('Loading Channel Limitations for: **' + str(channel) + '** ...')
		await asyncio.sleep(1)
		m = 'Channel Limitations\n'
		for o in channels:
			m += ' - ' + o + ': **' + str(channels.get(o, None)) + '**\n'

		await msg.edit(content=m)
