
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Guild(bot, settings))

class Guild(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def guild_info(self, ctx):
		guild: discord.Guild = ctx.guild
		title = "{0.name}({0.id})".format(guild)
		guild_info = [
			guild.afk_channel, 
			'Emoji count: {}'.format(len(guild.emojis)),
			guild.afk_timeout,
			guild.max_presences,
			guild.max_members,
			guild.max_video_channel_users,
			guild.description,
			guild.verification_level,
			guild.explicit_content_filter,
			guild.default_notifications,
			guild.features,
			guild.premium_tier,
			guild.premium_subscription_count,
			guild.preferred_locale,
			guild.mfa_level,
			'Channel count: {}'.format(len(guild.channels)),
			guild.large,
			'Stage Channel count: {}'.format(len(guild.stage_channels))
		]

		
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: 
			await fuz.fuzList(ctx, guild_info, title, 25)