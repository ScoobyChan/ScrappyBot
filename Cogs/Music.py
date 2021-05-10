import os
import aiohttp

# Music Play
import asyncio
import aiohttp
import itertools
import datetime
import humanize
from async_timeout import timeout
import re
from youtubesearchpython import VideosSearch
import wavelink
import typing
import random
import time

import discord
from discord.ext import commands

# url_rx = re.compile(r'https?://(?:www\.)?.+')


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Music(bot, settings))

# Used as reference for help when queueing because it wouldnt go to next song *Bang*
# https://github.com/PythonistaGuild/Wavelink/blob/a5f1aa0d345a3ef527c0d2e57851201ce4ddad0f/examples/advanced.py#L90

# To make
# VoteSkip?
# Add colors to embeds

# DJ Perms
# Admin override

# Redo start.bat to load Bot and Lavalink
# Get bot to move from channel a to b

class Track(wavelink.Track):
	"""Wavelink Track object with a requester attribute."""

	__slots__ = ('requester')

	def __init__(self, *args, **kwargs):
		super().__init__(*args)

		self.requester = kwargs.get('requester')

class MusicPlayer(wavelink.Player):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.context: commands.Context = kwargs.get('context', None)

		self.queue = []
		self.tracknum = 0
		self.maxprev = 10 # Can change
		self.prev = None

		self.wait = False # Waiting
		self.update = False # Updating 

		self.sogns = None
		self.repeat_track = None
		self.repeat = None # single | queue
		self.auto_leave = True

	async def play_next(self):
		""" Plays the Song each time it is needed"""
		if self.is_playing or self.wait:
			return

		try:
			self.wait = True
			async with timeout(300):
				if self.repeat == 'single':	
					track = self.repeat_track
				else:				
					if self.tracknum >= (self.maxprev - 1):
						self.queue.pop(0)
						track = self.queue[self.tracknum]
					else: 
						if self.tracknum >= len(self.queue):
							if self.auto_leave:
								raise asyncio.TimeoutError
							else:
								return
						else:
							try:
								track = self.queue[self.tracknum]
							except IndexError:
								print(len(self.queue))
								print(self.tracknum)
								raise asyncio.TimeoutError
							
					# Get Couter
		except asyncio.TimeoutError:
			await self.teardown()
			return 
		
		channel = self.bot.get_channel(int(self.channel_id))
		qsize = len(self.queue)

		embed = discord.Embed(title=f'Music Controller | {channel.name}', colour=0xebb145)
		embed.description = f'Now Playing:\n**`{track.title}`**\n\n'
		if track.thumb:
			embed.set_thumbnail(url=track.thumb)

		embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(track.length))))
		embed.add_field(name='Queue Length', value=str(qsize))
		embed.add_field(name='Volume', value=f'**`{self.volume}%`**')
		embed.add_field(name='Requested By', value=track.requester.mention)
		embed.add_field(name='Video URL', value=f'[Click Here!]({track.uri})')

		await self.context.send(embed=embed, delete_after=30)
		
		await self.play(track)
		self.wait = False

		if self.repeat == 'queue':
			if self.tracknum >= len(self.queue)-1:
				self.tracknum = -1

	async def teardown(self):
		"""Kill  Player"""
		try:
			await self.destroy()
		except KeyError:
			pass

class Music(commands.Cog, wavelink.WavelinkMixin):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.maxList = 10

		if not hasattr(bot, 'wavelink'):
			self.bot.wavelink = wavelink.Client(bot=self.bot)

		self.music_node = []

	async def start_nodes(self):
		await self.bot.wait_until_ready()
		node = self.bot.wavelink.get_best_node()
		host_ip = '127.0.0.1'

		# Initiate our nodes. For this example we will use one server.
		# Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

		# print('Starting')
		if not node:
			try:	
				node = await self.bot.wavelink.initiate_node(host=host_ip,
					port=2333,
					rest_uri='http://{}:2333'.format(host_ip),
					password='{}'.format(self.bot.wavepass),
					identifier='Scappy Bot',
					region='sydney'
				)
			except aiohttp.client_exceptions.ClientConnectorError:
				raise discord.DiscordException("Lava link still down")

	@wavelink.WavelinkMixin.listener('on_track_stuck')
	@wavelink.WavelinkMixin.listener('on_track_end')
	@wavelink.WavelinkMixin.listener('on_track_exception')
	async def on_player_stop(self, node: wavelink.Node, payload):
		"""On song finish """
		payload.player.tracknum += 1
		await payload.player.play_next()

	@wavelink.WavelinkMixin.listener()
	async def on_websocket_closed(self, node: wavelink.node.Node, payload: wavelink.events.WebsocketClosed):
			payload.player
			if payload.player:
				await payload.player.teardown()
			# raise discord.DiscordException(node.identifier)


	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		# Cancel mutes
		for x in self.bot.guilds:
			player = self.bot.wavelink.players.get(x.id,None)
			if player: 
				await player.destroy()

		for x in self.music_node:
			x.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		self.music_node.append(self.bot.loop.create_task(self.start_nodes()))

	@commands.command(name='disconnect')
	async def disconnect_(self, ctx, *, channel: discord.VoiceChannel=None):
		"""Disconnets the bot"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		if not player.is_connected:
			raise discord.DiscordException('No channel to leave.')

		await ctx.send(f'Disconnecting from **`{channel.name}`**', delete_after=30)
		await player.teardown()

	@commands.command(name='connect')
	async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
		"""Connects the bot"""
		if not channel:
			try:
				# channel = self.settings.Get(ctx, 'channel', Name=734328996237410325)
				channel = ctx.author.voice.channel
			except AttributeError:
				raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

		if len(channel.members) >= channel.user_limit and not channel.user_limit == 0:
			raise commands.DisabledCommand('Can not Join channel **`{}`** as too many users in the channel all ready `({}/{})`'.format(str(channel), len(channel.members), channel.user_limit))

		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		await ctx.send(f'Connecting to **`{channel.name}`**', delete_after=30)
		await player.connect(channel.id)
		
	@commands.command()
	async def play(self, ctx, *, search: str = None):
		"""[search/url(soundcloud or youtube)]
		Plays music"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)

		if not search:
			if player.is_paused():
				# Resume song
				return await ctx.invoke(self.resume_)
			else:
				raise discord.DiscordException('No search provided. Please enter a search or url')


		search = search.replace('http:', 'https:')

		# msg = await ctx.send('Collecting Songs ...')
		videosSearch = VideosSearch(search, limit = 5)
		res = videosSearch.result()
		results = res.get('result', [])

		_res = {}
		_name = []

		num = 0
		for x in results:
			_res[x['title']] = num
			_name.append(x['title'])
			num += 1

		# print(_name)
		
		if not search.startswith('https://'):
			fuz = self.bot.get_cog('FuzzySearch')
			if not fuz: return
			
			_return = await fuz.fuzSelect(ctx, _name)
			if not _return: return
			search = results[_res[_return]]['link']

		tracks = await self.bot.wavelink.get_tracks(search)
		if not tracks: return await ctx.send('Track is either invalid or hidden from my view')

		if not player.is_connected:
			await ctx.invoke(self.connect_)

		if isinstance(tracks, wavelink.TrackPlaylist):
			for x in tracks.tracks:
				track = Track(x.id, x.info, requester=ctx.author)
				player.queue.append(track)

			await ctx.send(f'```ini\nAdded the playlist {tracks.data["playlistInfo"]["name"]}'
							f' with {len(tracks.tracks)} songs to the queue.\n```', delete_after=15)
		else:
			track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)
			player.queue.append(track)
			await ctx.send(f'Now Queueing **`{str(tracks[0])}`**')
			
		if not player.is_playing:
			await player.play_next()

	@commands.command()
	async def skip(self, ctx):
		"""Skips the song"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		await ctx.send(f'Skipping **`{player.current}`**')
		await player.stop() 
		# await player.destroy()

	@commands.command()
	async def prev(self, ctx):
		"""Goes to the previous song"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		await ctx.send(f'Playing Previous song **`{player.queue[player.tracknum-1] if player.tracknum > -1 else player.queue[0]}`**')
		
		if player.tracknum <= 0:
			player.tracknum = -1
		else:
			player.tracknum -= 2
		
		await player.stop() 

	@commands.command()
	async def start_queue(self, ctx):
		"""Plays from the start of the song"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		await ctx.send(f'Playing from the start of queue **`{player.queue[0]}`**')
		
		player.tracknum = -1
		await player.stop() 

	@commands.command()
	async def stop(self, ctx):
		"""Stops the music play and leaves if set to auto leave"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		await ctx.send(f'Stopping **`{player.current}`**')
		await player.teardown()
	
	@commands.command()
	async def repeat(self, ctx, rep=None):
		"""[off/single/queue]
		Might be working to check"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		accepted = ['off', 'single', 'queue']
		if not rep: return await ctx.send('Repeat set to: '.format(player.repeat))

		if not rep.lower() in accepted:
			return

		await ctx.send(f'Repeat{" turned off" if rep.lower() == "off" else f"ing single **`{player.current.title}`**" if rep.lower() == "single" else "ing Queue have fun :D"}')

		player.repeat = rep.lower()
		if player.repeat == 'single':
			player.repeat_track = player.current
		else:
			player.repeat_track = None

		if rep.lower() == 'off':
			player.repeat_track = None
			player.repeat = None

	@commands.command(alias=['vq', 'queue'])
	async def view_queue(self, ctx):
		"""Views the queue lined up"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		if len(player.queue) == 0:
			return await ctx.send('There are currently no more queued songs.')

		reacts = ['⏮️','◀️','▶️','⏭️']
		msg = await ctx.send('Gathering Queue')
		await asyncio.sleep(0.05)
		num = 0
		while True:
			# Grab up to 5 entries from the queue...
			fmt = '\n'.join(f'└─ **`{track.title}`** | {str(datetime.timedelta(milliseconds=int(track.length)))}' for track in player.queue[num+player.tracknum:(num + self.maxList + player.tracknum)])
			embed = discord.Embed(title=f'Upcoming - Next {len(player.queue) - player.tracknum}', description=fmt)
			await msg.edit(content=None, embed=embed)

			if (len(player.queue) - player.tracknum) > 10:
				try:	
					for r in reacts:
						await msg.add_reaction(r)

					def check(reaction: discord.Reaction, adder: discord.User) -> bool:
						return adder == ctx.message.author and reaction.message.id == msg.id

					reaction, adder = await self.bot.wait_for('reaction_add', timeout=30, check=check)
					if reaction.emoji == reacts[0]:
						num = 0

					if reaction.emoji == reacts[1]:
						if not num <= 0:
							num -= 10

					if reaction.emoji == reacts[2]:
						if not num >= len(player.queue)  - player.tracknum:
							num += 10

					if reaction.emoji == reacts[3]:
						num = len(player.queue) - player.tracknum

				except asyncio.exceptions.TimeoutError:
					break
			else:
				break
		
		if (len(player.queue) - player.tracknum) > 10:
			for r in reacts:
				await msg.remove_reaction(r, self.bot.user)

		return

	@commands.command(alias='np')
	async def now_playing(self, ctx):
		"""Shows whats currently playing"""
		channel = ctx.channel

		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		track = player.current
		qsize = len(player.queue)

		embed = discord.Embed(title=f'Music Controller | {channel.name}', colour=0xebb145)
		embed.description = f'Now Playing:\n**`{track.title}`**\n\n'
		if track.thumb:
			embed.set_thumbnail(url=track.thumb)

		# res = time.ctime(datetime.timedelta(milliseconds=int(track.length)))
		# res.tm_hour if  len(res.tm_hour) > 0 else '0' + str(res.tm_hour)}:{res.tm_min if  len(res.tm_min) > 0 else '0' + str(res.tm_min)}:{res.tm_sec if  len(res.tm_sec) > 0 else '0' + str(res.tm_sec)
		
		

		embed.add_field(name='Duration', value=f"{datetime.timedelta(milliseconds=int(track.length))}")
		embed.add_field(name='Queue Length', value=str(qsize))
		embed.add_field(name='Volume', value=f'**`{player.volume}%`**')
		embed.add_field(name='Requested By', value=track.requester.mention)
		embed.add_field(name='Video URL', value=f'[Click Here!]({track.uri})')

		await ctx.send(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def musictest(self, ctx, *, playlist):
		"""Used for testing the music player"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)

		tracks = await self.bot.wavelink.get_tracks(playlist)
		print(tracks)

		return
		if not player.is_connected:
			await ctx.invoke(self.connect_)

		# await ctx.send(f'Added {str(tracks[0])} to the queue.')
		# await player.play(tracks[0])

		if player.is_playing:
			await ctx.send(f'Now Queueing **`{str(tracks[0])}`**')

		track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)
		await player.queue.append(track)

		if not player.is_playing:
			await player.play_next()

	@commands.command()
	async def volume(self, ctx, vol: int = None):
		"""[0 to 1000 (100 good range)]
		Sets the Volume for the bot music function"""

		# To do
		# Check greater 0 less than 1000
		# Max 1000
		# Min 0 
		# Add warning for above 150

		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		if not vol:
			return await ctx.send(f'The Volume is {player.volume}%')

		if vol > 1000 or vol < 0:
			return await ctx.send(f'The Volume is {"greater" if vol > 1000 else "less"} than {vol}')

		if vol > 150:
			msg = await ctx.send('Sound is quite loud you sure you want to contine?')

			reacts = ['✅', '❌']
			for r in reacts:
				await msg.add_reaction(r)

			def check(reaction: discord.Reaction, adder: discord.User) -> bool:
				return reaction.message.id == msg.id and adder == ctx.author

			try:
				reaction, adder = await self.bot.wait_for('reaction_add', timeout=20, check=check)
			except asyncio.exceptions.TimeoutError:
				return await msg.delete()
				
			if reaction.emoji == '✅':
				choice = "Yes"

			if reaction.emoji == '❌':
				choice = "No"

			for r in reacts:
				await msg.remove_reaction(r, self.bot.user)

			if choice == "No":
				return

		# Get Song
		await ctx.send(f'Setting Volume to **`{vol}`**')
		await player.set_volume(vol)

	@commands.command()
	async def remove_track(self, ctx, track: str):
		"""Removes a track from the queue"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		_track = -1
		found = False
		for x in player.queue:
			_track += 1
			if track.lower() in x.title.lower():
				found = True
				await ctx.send(f'Removing track: **`{x.title}`**')
				break

		if found:
			player.queue.pop(_track)
		else:
			await ctx.send(f'Track: **`{track}`** not found')

	@commands.command()
	async def clear_queue(self, ctx):
		"""Clears the current Queue"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		for x in player.queue:
			player.queue.remove(x)

		await player.stop()
		await ctx.send(f'{ctx.guild.name} queue cleared by **`{ctx.author.name}`**')

	@commands.command()
	async def auto_leave(self, ctx):
		"""Sets the auto leave to True or False"""
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		if player.auto_leave:
			player.auto_leave = False
		else:
			player.auto_leave = True

		await ctx.send(f'Auto leave set to {player.auto_leave} by **`{ctx.author.name}`**')

	@commands.command()
	async def load_queue(self, ctx):
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)

		_queue = self.settings.ServerSettings(ctx.guild.id, 'Music')
		for q in _queue:
			player.queue.append(q)

		if not player.is_connected:
			await ctx.invoke(self.connect_)

		if not player.is_playing:
			await player.play_next()

		await ctx.send('Loaded the saved saved queue')

	@commands.command()
	async def save_queue(self, ctx):
		player: MusicPlayer = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=MusicPlayer, context=ctx)
		
		self.settings.ServerSettings(ctx.guild.id, 'Music', player.queue)
		await ctx.send('Saving the current queue to playlist')