import time
import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter

class Webhook(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def testwebhook(self, ctx):
		print('creating webhook')
		webhook = await ctx.channel.create_webhook(name="Vic is a Dick")
		await webhook.send('test')
		print('deleting webhook')
		await webhook.delete()

	@commands.command()
	async def msgwh(self, ctx, hookname, *, msg):
		await ctx.message.delete()
		webhook = await ctx.channel.create_webhook(name=hookname)
		await webhook.send(msg)
		await webhook.delete()


	@commands.command()
	async def userwh(self, ctx, user: discord.Member, *, msg=None):
		await ctx.message.delete()
		if not msg: return
		print(user.name)
		print(user.avatar_url)
		webhook = await ctx.channel.create_webhook(name=user.name if not user.nick else user.nick)
		await webhook.send(content=msg, avatar_url=user.avatar_url)
		await webhook.delete()

def setup(bot):
	bot.add_cog(Webhook(bot))