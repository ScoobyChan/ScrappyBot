import discord
from discord.ext import commands

# Remove Guild when server leave

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Tableflip(bot, settings))

class Tableflip(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	async def onmessage(self, message):
		if message.author.bot:
			return
		
		if '(╯°□°）╯︵ ┻━┻' in message.content: 
			mute = self.bot.get_cog('Mute')
			if mute:
				ctx = self.bot.get_context(message)
				mute._mute(ctx, message.author.id, message.guild.id, 60)

			message.channel.send('We don\'t flip tables here. {}'.format('' if not mute else 'You have been muted for 1 minute.'))
			message.delete()
		
	@commands.command()
	async def enabletableflip(self, ctx):
		if self.settings.ServerConfig(ctx.guild.id, 'tableflip'): tab = False
		else: tab = True

		self.settings.ServerConfig(ctx.guild.id, 'tableflip', tab)
		
		await ctx.send('I have {} TableFlip checker'.format('Enabled' if tab else 'Disabled'))