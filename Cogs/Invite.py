import discord
from discord.ext import commands
from datetime import datetime

class Invite(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def Invite(self, ctx):
		"""
		Sends an Invite URL for the bot
		Highly suggest having admin as perms
		"""
		bot_invite = "Logged in as:{0} (ID: {0.id})\nInvite Link:\nhttps://discordapp.com/oauth2/authorize?client_id={0.id}&scope=bot&permissions=8\n".format(self.bot.user)
		await ctx.send(bot_invite)

	@commands.command()
	async def invite_info(self, ctx, url:str):
		try:
			invite = await self.bot.fetch_invite(url)
			# Format a message with details about the invite
			details = (f"Invite Details:\n"
			f" - Server: {invite.guild.name}\n"
			f" - Channel: {invite.channel.name}\n"
			f" - Inviter: {invite.inviter}\n"
			f" - Uses: {invite.uses}\n"
			f" - Max Uses: {invite.max_uses}\n"
			f" - Expires At: {datetime.fromisoformat(str(invite.expires_at)).strftime('%Y-%m-%d %H:%M:%S')}")
			await ctx.send(details)
		except discord.NotFound:
			await ctx.send("That invite does not exist or is no longer valid.")
		except discord.Forbidden:
			await ctx.send("I don't have permissions to access invite details.")
		except discord.HTTPException:
			await ctx.send("Failed to retrieve invite.")


async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Invite(bot, settings))