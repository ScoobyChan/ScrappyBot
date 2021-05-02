import sys
import socket
import os
import platform
import time
import asyncio
import discord
from datetime import tzinfo, timedelta, datetime, date
from pytz import timezone
from discord.ext import commands

from Utils import Utils

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.Utils = Utils.Utils()

	@commands.command()
	async def botinfo(self, ctx):
		serID = f'{ctx.guild.id}'
		uID = f'{ctx.author.id}'
		c = None
		tz = 'UTC'

		try:
			tz = tz.split(':')
			int(tz[0])
			i = True
		except Exception as e:
			i = False

		totalguilds = len(self.bot.guilds)
		totalmember = 0
		indivtotalmember = []
		
		for g in self.bot.guilds:
			for m in g.members:
				if not m in indivtotalmember:
					indivtotalmember.append(m)

				totalmember += 1
				if m.id == self.bot.user.id:
					pos = m.top_role.position
					jtime = str(m.joined_at)
					j = datetime.fromisoformat(jtime)

		b = self.bot.user
		commlen = 0
		cogLen = 0
		for c in self.bot.cogs:
			cogLen += 1	
			cog = self.bot.get_cog(c)
			commands = cog.get_commands()
			commlen += len([c.name for c in commands])

		status_text = ":green_heart:"
		if b.status == discord.Status.offline:
			status_text = ":black_heart:"
		elif b.status == discord.Status.dnd:
			status_text = ":heart:"
		elif b.status == discord.Status.idle:
			status_text = ":yellow_heart:"
		else:
			status_text = ":green_heart:"

		
		time = str(b.created_at)
		d = datetime.fromisoformat(time)

		if i:
			d += timedelta(hours=int(tz[0]), minutes=int(tz[1]), seconds=int(tz[2]))
		else:
			tz = ''.join(tz)
			d = d.replace(tzinfo=timezone(tz))
		
		created_at = d.strftime("%a, %d %b %Y %H:%M %p %Z")
		info = await bot.application_info()
		BO = "{0}({0.id})".format(info.owner)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.DM.randomColor()

		embed=discord.Embed(title=f"{b.name}", color=col)
		embed.set_thumbnail(url=f"{b.avatar_url}")
		embed.add_field(name="\u200b", value="Current Bot Information", inline=False)
		embed.add_field(name="Bot Owner", value=BO, inline=False)
		embed.add_field(name="Members", value=f"{totalmember}/({len(indivtotalmember)} individual members)", inline=True)
		embed.add_field(name="Servers", value=f"{totalguilds}", inline=True)
		embed.add_field(name="Commands", value=f"{commlen} (Total Cogs {cogLen})", inline=True)
		embed.add_field(name="Created", value=f"{created_at}", inline=True)
		if self.bot.shard_count:
			embed.add_field(name="Shard Count", value=f"{self.bot.shard_count}", inline=True)
		embed.add_field(name="Joined at", value=f"{j}", inline=True)
		embed.add_field(name="Status", value=f"{status_text}", inline=True)
		embed.add_field(name="Prefixes", value=f"{ctx.prefix}", inline=True)
		embed.set_footer(text=f"Bot ID: {b.id} Bot Name {b.name}")
		await ctx.send(embed=embed)

	@commands.command()
	async def serverinfo(self, ctx, server=None):
		serID = f'{ctx.guild.id}'
		uID = f'{ctx.author.id}'
		c = None
		tz = 'UTC'

		if not server:
			c = ctx.guild
		else:
			for g in self.bot.guilds:
				if str(g) == str(server) or str(g.id) == str(server) or str(g.name) == str(server):
					c = g
					break
			if not c:
				return await ctx.send(f'I can not find that Server: **{server}**')

		time = str(c.created_at)
		d = datetime.fromisoformat(time)
		
		for m in c.members:
			if m.id == self.bot.user.id:
				jtime = str(m.joined_at)
				j = datetime.fromisoformat(jtime)

				pos = m.top_role.position
				jtime = str(m.joined_at)
				j = datetime.fromisoformat(jtime)
				break

		try:
			tz = tz.split(':')
			int(tz[0])
			i = True
		except Exception as e:
			# print(e)
			i = False

		if i:
			print(tz)
			d += timedelta(hours=int(tz[0]), minutes=int(tz[1]), seconds=int(tz[2]))
			j += timedelta(hours=int(tz[0]), minutes=int(tz[1]), seconds=int(tz[2]))
		else:
			tz = ''.join(tz)
			d = d.replace(tzinfo=timezone(tz))
			j = j.replace(tzinfo=timezone(tz))
		
		created_at = d.strftime("%a, %d %b %Y %H:%M %p %Z")
		j = j.strftime("%a, %d %b %Y %H:%M %p %Z")

		om = tm = ro = vc = tc = cat = b = bo = 0
		for user in c.members:
			if user.bot:
				b += 1

			tm += 1
			if str(user.status) != 'offline':
				om += 1
				if user.bot:
					bo += 1

		for r in c.roles:
			ro += 1

		for ch in c.channels:
			if str(ch.type) == 'text':
				tc += 1
			elif str(ch.type) == 'voice':
				vc += 1
			else:
				cat += 1

		if tm > 1000: 
			CL = "Very"
		elif tm > 100:
			CL = "Yes"
		else:
			CL = "No"

		em = 0
		# emo = emo1 = emo2 = ''
		emo = []
		startem = 0 
		endem = 20
		for e in c.emojis:
			emo.append(str(e))

			# if em > 40:
			# 	emo2 += str(e)
			# elif em > 20:
			# 	emo1 += str(e)
			# else:
			# 	emo += str(e)

		

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.DM.randomColor()

		embed=discord.Embed(title=f"{c.name}", color=col)
		embed.set_thumbnail(url=f"{c.icon_url}")
		embed.add_field(name="\u200b", value=f"Created at: {created_at}", inline=False)
		embed.add_field(name=f"Members({c.member_count})", value=f"Online Members: {om}/{tm} (%{int((om/tm)*100)})\nOnline Bots: {bo}/{b} (%{int((bo/b)*100)})", inline=True)
		embed.add_field(name="Roles", value=f"{ro}", inline=True)
		embed.add_field(name="Channels", value=f"TextChannel: {tc}\nVoiceChannel: {vc}\nCategories: {cat}", inline=True)
		embed.add_field(name="Default Role", value=f"{c.default_role}", inline=False)
		# embed.add_field(name="Nitro Boosts", value=f"{}", inline=True)
		
		embed.add_field(name="Owner", value=f"{c.owner}", inline=True)
		embed.add_field(name="AFK Channel", value=f"{c.afk_channel}", inline=True)
		embed.add_field(name="Voice Region", value=f"{c.region}", inline=True)
		embed.add_field(name="Considered Large", value=f"{CL}", inline=True)
		if self.bot.shard_count:
			embed.add_field(name="Shard ID", value=f"{c.shard_id}/{self.bot.shard_count}", inline=True)
		embed.add_field(name="Join At", value=f"{j}", inline=True)
		embed.add_field(name="Population Rank", value=f"{pos}", inline=False)

		while True:
			embed.add_field(name="Emoji\'s {}".format('Continued' if startem > 20 else ""), value=''.join(emo[startem:endem]), inline=True)
			
			endem += 20
			startem += 20

			if endem >= len(emo):
				break

		embed.set_footer(text="Server ID: {0.id} // Server Name: {0.name}".format(c))
		await ctx.send(embed=embed)

	@commands.command()
	async def serverlist(self, ctx, servers: int = 10, reverse: bool = True):
		"""[server list count][bottom to top]"""
		# Fix list menu
		msg = await ctx.send('Gathering Servers....')
		if servers > 50:
			servers = 50

		reacts = ['⏮️','◀️','▶️','⏭️']

		def UserCount(elem):
			return elem[1]

		g = _guilds = []
		for _g in self.bot.guilds:
			_guilds.append((_g.name, len(_g.members)))

		guild = _guilds.sort(key=UserCount, reverse=reverse)
		await asyncio.sleep(0.05)

		num = strt = 0
		end = servers
		servers = 10
		end = servers

		while True:
			if end > len(_guilds):
				break
			
			_list = [x for x  in _guilds[strt:end]]
			g.append(_list)
			strt += servers
			end += servers

		# print(g)
		col = ctx.author.top_role.colour
		try:	
			while True:
				desc = '\n'.join([f"**{name}** \n- Members: `{count}`" for name, count in g[num]])

				embed = self.Utils.embed({"title":f"List of Servers I'm - {num+1}/{len(g)}", "desc":desc, "color":col})		
				await msg.edit(content=None, embed=embed)
				if len(g) > 1:
					try:	
						for r in reacts:
							await msg.add_reaction(r)

						def check(reaction: discord.Reaction, adder: discord.User) -> bool:
							return adder == ctx.message.author and reaction.message.id == msg.id

						reaction, adder = await self.bot.wait_for('reaction_add', timeout=30, check=check)
						if reaction.emoji == reacts[0]:
							num = 0

						if reaction.emoji == reacts[1]:
							if not num == 0:
								num -= 1

						if reaction.emoji == reacts[2]:
							if not num >= len(g) - 1:
								num += 1
								
						if reaction.emoji == reacts[3]:
							num = len(g) - 1

					except asyncio.exceptions.TimeoutError:
						break

			
				if len(g) > 1:	
					for r in reacts:
						await msg.remove_reaction(r, self.bot.user)

		except ValueError:
			desc = '\n'.join([f"**{name}** \n- Members: `{count}`" for name, count in g])
			embed = self.Utils.embed({"title":f"List of Servers I'm", "desc":desc, "color":col})		
			await msg.edit(content=None, embed=embed)

	@commands.command()
	async def online(self, ctx):
		bof	= 0
		for user in c.members:
			if not user.bot and str(user.status) != 'offline':
				bof += 1

		await ctx.send('Users online: {}'.format(bof))

	@commands.command()
	async def offline(self, ctx):
		bof	= 0
		for user in c.members:
			if not user.bot and str(user.status) == 'offline':
				bof += 1

		await ctx.send('Users offline: {}'.format(bof))

	@commands.command()
	async def botonline(self, ctx):
		bof	= 0
		for user in c.members:
			if user.bot and str(user.status) != 'offline':
				bof += 1

		await ctx.send('bots online: {}'.format(bof))

	@commands.command()
	async def botoffline(self, ctx):
		bof	= 0
		for user in c.members:
			if user.bot and str(user.status) == 'offline':
				bof += 1

		await ctx.send('bots offline: {}'.format(bof))

def setup(bot):
	bot.add_cog(Info(bot))