import re
import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter

class Regex(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	"""
	Setup usage:

	alert mention if any
	[[here]]
	[[rolemen:id]]
	[[alertusermen:id]]
	[[everyone]]
	[[alertchannel]]
	
	action
	[[kick:time]]
	[[ban:time]]
	[[mute:time]]

	user mentions
	[[username:id]]
	[[userid:id]]
	[[userment:id]]

	channel to send
	[[sendchan]]
	

	example:
	[[user:mention]] has sent a scam link. [[role_id:5656565]] please take action. **[[user:name]]** has been [[mute:600]]

	[[user:mention]] has sent a scam link in [[sendchan]]. **[[user:name]]** has been [[kick]]

	"""

	async def onmessage(self, message):
		if message.author.bot: return
		ctx = await self.bot.get_context(message)

		print(message.content)

		# Check if Admin
		responses = []
		responses = self.settings.ServerConfig(ctx.guild.id, 'Responses')
		triggers = self.settings.ServerConfig(ctx.guild.id, 'Triggers')
		
		if len(triggers) > 0:
			for r in triggers:
				re.compile(r)
				match = re.search(r, message.content)
				if match: 
					txt = triggers.get(r, {}).get('Name', None)
					if not txt: return

					r = re.split('\s', txt)
					for v in r:
						pat = '\[\[.*\]\]'
						x = re.search(pat, v)

						if x:
							t = v.replace('[', '').replace(']', '')
							u = t.split(':')
							
							rep = None

							if 'here' == u[0]: rep = '@here'
							if 'rolemen' == u[0]: rep = '<@&{}>'.format(u[1])
							if 'alertusermen' == u[0]: rep = '<@{}>'.format(u[1])
							if 'everyone' == u[0]: rep = '@everyone'
							
							if 'kick' == u[0]:
								admin = self.bot.get_cog('Admin')
								await admin._kick(ctx, u, 'Removed by trigger', skip_conf=True, kick_time=False if len(u) == 1 else u[1])
								rep = 'Kicked{}'.format('' if len(u) == 1 else ' for {}'.format(self.settings.Time(u[1])[1]))

							if 'ban' == u[0]: 
								admin = self.bot.get_cog('Admin')
								await admin._ban(ctx, u, 'Removed by trigger', skip_conf=True, kick_time=False if len(u) == 1 else u[1])
								rep = 'Banned{}'.format('' if len(u) == 1 else ' for {}'.format(self.settings.Time(u[1])[1]))

							if 'mute' == u[0]:
								mute = self.bot.get_cog('Mute')
								await mute._mute(ctx, message.author.id, ctx.guild.id, 0 if len(u) == 1 else u[1])
								rep = 'Muted{}'.format('' if len(u) == 1 else ' for {}'.format(self.settings.Time(u[1])[1]))

							if 'username' == u[0]: user = message.author; rep = user.nick or user.name
							if 'userment' == u[0]: user = message.author; rep = user.mention
							if 'userid' == u[0]: user = message.author; rep = str(user.id)
							if 'sendchan' == u[0]: rep = message.channel.mention

							if rep: txt = txt.replace(v, rep)

					pat = '\\b\[\[alertchannel.\\w+\]\]'
					x = re.search(pat, txt)
					
					if x:
						r = re.findall(pat, txt)
						r = r.split(' ')
						print(r)
						for b in r:
							txt = txt.replace(b, '')
							r = b.replace('[', '').replace(']', '')
						if isinstance(r.split(':')[1], int):
							alert = self.bot.get_channel(int(r.split(':')[1]))
							await alert.send(txt)
						else:
							await ctx.send(txt)
					else:
						await ctx.send(txt)

		
		if len(responses) > 0:
			for r in responses:
				re.compile(r)
				match = re.search(r, message.content)
				if match: 
					return await ctx.send(responses[r])


	@commands.command()
	async def testmatchres(self, ctx, _regex: str, *, msg: str):
		match = re.search(_regex, msg)
		if match: await ctx.send('Match was found')
		else: await ctx.send('Match not found')

	@commands.command()
	async def addtrig(self, ctx, _regex: str, _action: str):
		re.compile(_regex)
		re.compile(_action)
		response = self.settings.ServerConfig(ctx.guild.id, 'Triggers')
		
		if _regex in response: return await ctx.send('Trigger already in list')

		response[str(_regex)] = {}
		response[str(_regex)]['Name'] = str(_action) 
		
		self.settings.ServerConfig(ctx.guild.id, 'Triggers', response)

		await ctx.send('Added trigger to list')

	@commands.command()
	async def remtrig(self, ctx, *, index: int = None):
		response = self.settings.ServerConfig(ctx.guild.id, 'Triggers')
		newindex = (index - 1)
		if newindex > len(response): return await ctx.send('Index too high')
		
		num = 0
		for x in response:
			if str(num) == str(newindex):
				del response[x]
				break

		self.settings.ServerConfig(ctx.guild.id, 'Triggers', response)

		await ctx.send('Removed trigger from list')

	@commands.command()
	async def triggers(self, ctx):
		res = self.settings.ServerConfig(ctx.guild.id, 'Triggers')
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: await fuz.fuzList(ctx, res, 'Regex Triggers', max_num = 10)

	@commands.command()
	async def trigtest(self, ctx, *, message: str = None):
		print(message)

	@commands.command()
	async def addresp(self, ctx, _regex: str, _action: str):
		re.compile(_regex)
		response = self.settings.ServerConfig(ctx.guild.id, 'Triggers')
		
		if _regex in response: return await ctx.send('Response already in list')

		response[str(_regex)] = {}
		response[str(_regex)]['Name'] = str(_action) 
		
		self.settings.ServerConfig(ctx.guild.id, 'Responses', response)

		await ctx.send('Added response to list')

	@commands.command()
	async def remresp(self, ctx, *, index: int = None):
		response = self.settings.ServerConfig(ctx.guild.id, 'Responses')
		newindex = (index - 1)
		if newindex > len(response): return await ctx.send('Index too high')
		
		num = 0
		for x in response:
			if str(num) == str(newindex):
				del response[x]
				break

		self.settings.ServerConfig(ctx.guild.id, 'Responses', response)

		await ctx.send('Removed response from list')

	@commands.command()
	async def responses(self, ctx):
		res = self.settings.ServerConfig(ctx.guild.id, 'Responses')
		fuz = self.bot.get_cog('FuzzySearch')
		if fuz: await fuz.fuzList(ctx, res, 'Regex Responses', max_num = 10)


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Regex(bot, settings))