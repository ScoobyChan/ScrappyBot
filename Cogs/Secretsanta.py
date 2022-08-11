import random
import discord
from discord.ext import commands
import logging
import os

log = 'Error'
if not os.path.exists(log):
	os.mkdir(log)

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Secretsanta(bot, settings))

class Secretsanta(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		# logging.basicConfig(filename=log+'/secret.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(message)s')

	@commands.command()
	async def secretsanta(self, ctx, *, p=None):
		"""[members]
		Usage: secretsanta 181338470520848384 @user @role username nickname
		Excludes Bots
		"""

		# Names, mentions, Roles?
		if not p:
			return

		p = p.split(' ')
		# print (p)
		people = []
		for pep in p:
			# print(pep)
			if pep.startswith('<@&') and pep.endswith('>'): # Role
				r = self.settings.Get(ctx, 'role', pep.strip('<@&>'))
				for m in ctx.guild.members:
					if r in m.roles:
						# print(m)
						# print(m.bot)
						if not m.id in people and not m.bot:
							people.append(m.id)

			else:
				x = self.settings.Get(ctx, 'user', pep.strip('<@!>'))
				if x:
					if not x.id in people:
						people.append(x.id) # User
		
		# print(people)
		if len(people) < 3:
			_m = ''
			for x in people:
				_m += ' - **{}**\n'.format(str(self.settings.Get(ctx, 'user', x).name))
			return await ctx.send('Not enough members. Needs to be more than 3 and can\'t include Bots\n{}'.format(_m))

		def secret(p):
			try:
				s = p
				used = []
				peps = {} # {xxxx:yyyy}
				_used = []
				for i in range(0, len(p)):
					while True:	
						t = random.choice(s)
						if not t in _used:
							_used.append(t)
							break

					peps[p[i]] = t

				# print(peps)

				for p in peps:
					used.append(int(p) == int(peps[p]))

				if not True in used:
					return peps
				else:
					return False

			except TypeError:
				return False

		while True:
			t = secret(people)
			if t != False:
				# print(t)
				break

		_m = ''
		for x in people:
			_m += ' - **{}**\n'.format(str(self.settings.Get(ctx, 'user', x).name))
		await ctx.send('Sending out people to: \n{}'.format(_m))

		for x in t:
			m = ctx.guild.get_member(int(x))
			p = ctx.guild.get_member(int(t[x]))

			# print(m, p)
			await m.send('Secret santa is ||%s||' % p)

