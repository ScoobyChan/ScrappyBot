import asyncio
import json
import datetime
import discord
from discord.ext import commands
from discord.utils import get, find


class Quote(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	async def sendQuote(self, gID, chID, uID, msgID, ctx=None, quote:str=None):
		for g in self.bot.guilds:
			if g.id == gID: guild = g; break
		
		ch = self.bot.get_channel(chID)
		quotech = discord.utils.get(guild.channels, id=self.settings.ServerConfig(gID, 'quoteChannel'))

		u = discord.utils.get(guild.members, id=int(uID))
		if not quotech:
			return
	
		msg = await ch.fetch_message(msgID)
		
		if quote:
			m = quote
		else:
			m = msg.content
		
		if msg.author.top_role.colour:
			col = msg.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed=discord.Embed(color=col)
		embed.set_author(name=f"{msg.author.name}", icon_url=f"{msg.author.avatar_url}")
		embed.add_field(name="\u200b", value=f"{m}\n\nSent by <@{msg.author.id}> in <#{msg.channel.id}> | [Link](https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}) | {datetime.datetime.utcnow()}", inline=False)
		embed.set_footer(text=f"Quoted by {u}")
		await quotech.send(embed=embed)

	def react_check(self, user, msg, emoji):
		def check(reaction, usr):
			return reaction.message.id==msg.id and reaction.emoji==emoji
		return check

	@commands.command()
	async def addQuoteReaction(self, ctx, *, quote:str=None):
		"""
		[reaction]
		Sets the quote reaction
		"""
		unimoji = quote.encode('unicode-escape').decode('ASCII')
		msg = await ctx.send('Testing {}'.format(quote))
		try:
			await msg.add_reaction(quote)
		except:
			return await ctx.send(f'{quote} is not a Emoji. please add a valid Emoji')
		
		await msg.delete()
		self.settings.ServerConfig(ctx.guild.id, 'quoteEmote', unimoji)
		await ctx.send(f'I have set the quote reaction to: {quote}')

	async def onrawreactionadd(self, payload):
		gID = payload.guild_id
		chID = payload.channel_id
		msgID = payload.message_id
		uID = payload.user_id

		if payload.user_id == self.bot.user.id:
			return

		s = payload.emoji.name
		uniCode = s.encode('unicode-escape').decode('ASCII')
		r = self.settings.ServerConfig(gID, 'quoteEmote')

		print(r)
		print(uniCode)
		print(uniCode in r)

		if not uniCode in r: return

		print('check')
		await self.sendQuote(gID, chID, uID, msgID)
	
	@commands.command()
	async def Quote(self, ctx, *, quote:str=None):
		"""
		[Quote or msg link]
		Sends quote to channel
		"""			
		if not quote: 
			return await ctx.send("please send a message link or a Quote")	

		ch = self.settings.ServerConfig(ctx.guild.id, 'quoteChannel')
		if ch == 0:	return await ctx.send('No Quotes Channel Has Been Set')

		if "https://discordapp.com/channels" in quote:
			spl = quote.split('/')
			gID = spl[4]
			chID = spl[5]
			msgID = spl[6]
			uID = ctx.author.id
			await self.sendQuote(gID, chID, uID, msgID, ctx)
		else:
			gID = ctx.message.guild.id
			chID = ctx.message.channel.id
			msgID = ctx.message.id
			uID = ctx.message.author.id
			await self.sendQuote(gID, chID, uID, msgID, ctx, quote)
		
	@commands.command()
	async def testQuoteChannel(self, ctx):
		"""Tests quote channel"""

		c = self.settings.Get(ctx, 'channel', self.settings.ServerConfig(ctx.guild.id, 'quoteChannel'))
		if c:
			await c.send('Quote channel')
		else:
			await ctx.send('Invalid Channel has been give')

	@commands.command()
	async def setQuoteChannel(self, ctx, channel=None):
		"""
		[channel[
		sets quote channel
		"""
		if channel != 0:
			if not channel:
				channel = ctx.channel
			chan = self.settings.Get(ctx, 'channel', channel)
			self.settings.ServerConfig(ctx.guild.id, 'quoteChannel', chan.id)
			
			await ctx.send(f'I have set Quote Channel to: **{chan}** ')
		else:
			await ctx.send(f'I have removed Quote Channel')

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Quote(bot, settings))