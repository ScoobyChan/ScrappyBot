# https://developer.spotify.com/dashboard
# https://wavelink.readthedocs.io/en/latest/wavelink.html
# https://github.com/PythonistaGuild/Wavelink/blob/a5f1aa0d345a3ef527c0d2e57851201ce4ddad0f/examples/advanced.py#L90

from ast import If, Return
from timeit import repeat
import aiohttp

# Music Play
import asyncio
import aiohttp
import itertools
import datetime

from async_timeout import timeout
import re
from requests import options
from youtubesearchpython import VideosSearch
import wavelink
from wavelink.ext import spotify
import typing
import random
import time

import discord
from discord.ext import commands

import logging

# url_rx = re.compile(r'https?://(?:www\.)?.+')

# TO DO:
# - VoteSkip
# - DJ
# - Queuing
# - Remove from Queue
# - Save Queue
# - Dump queue
# - Clear queue
# - Skip
# - Previous
# - Volume
# - is_play
# - filter?
# - EQ
# - Karaoke
# - ChannelMix
# - repeat/single
# - seek
# - Lock channel
# - Admin override

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Music(bot, settings))


class Music(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

		self.music_node = []
		self.music_loaded = False
		self.spot = False

	###################
	#  COG LISTENERS  #
	###################

	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		if self.music_loaded == True:
			if self.bot.debug: print('unloading')
			self.music_loaded = False

			for task in self.music_node:
				if self.bot.debug: print('Removing task')
				task.cancel()

	@commands.Cog.listener()
	async def on_loaded_extension(self, ext):
		await self.bot.wait_until_ready()
		
		# Stops the loops from activating multiple times
		if self.music_loaded == False:
			if self.bot.debug: print("Initializing Music")	
			if self.bot.debug: print('Cog loaded')
			self.music_loaded = True
			self.music_node.append(self.bot.loop.create_task(self.start_nodes()))

	async def start_nodes(self):
		await self.bot.wait_until_ready()
		
		# host_ip = '127.0.0.1'
		host_ip = '192.168.1.4'

		# Initiate our nodes. For this example we will use one server.
		# Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)

		print('Starting')
		
		try:
			if self.bot.spotcli and self.bot.spotsec:
				self.spot = True
				node = await wavelink.NodePool.create_node(bot=self.bot, host=host_ip, port=2333, password=self.bot.wavepass, spotify_client=spotify.SpotifyClient(client_id=self.bot.spotcli, client_secret=self.bot.spotsec))	
			else:
				node = await wavelink.NodePool.create_node(bot=self.bot, host=host_ip, port=2333, password=self.bot.wavepass)
			
			if self.bot.debug: print(node.is_connected())
			node.is_connected()

		except aiohttp.client_exceptions.ClientConnectorError:
			raise discord.DiscordException("Lava link still down")

	@commands.Cog.listener()
	async def on_wavelink_node_ready(self, node: wavelink.Node):
		if node.is_connected(): print(f"Node {node.identifier} is ready!")

	@commands.Cog.listener()
	async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
		if self.bot.debug: 
			print('Now playing')
			print(player)
			print(track.title)

	@commands.Cog.listener()
	async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
		if self.bot.debug: 
			print(player)
			print(track.title)
			print(reason)
		
		await self._get_next_queue(player)

	@commands.Cog.listener()
	async def on_wavelink_track_stuck(self, player: wavelink.Player, track: wavelink.Track, threshold):
		if self.bot.debug: 
			print(player)
			print(track.title)
			print(threshold)
		
		await self._get_next_queue(player)

	@commands.Cog.listener()
	async def on_wavelink_track_exception(self, player: wavelink.Player, track: wavelink.Track, error):
		print(player)
		print(track.title)
		print(error)

	@commands.Cog.listener()
	async def on_voice_state_update(self, member: discord.Member, before, after):
		if member.bot: return

		player = wavelink.NodePool.get_node().get_player(member.guild)

		if not player: return

		print(player.channel)
		
		# if not player.channel or not player.ctx: wavelink.NodePool.get_node().players.pop(member.guild.id); return;

##################################
#####     Music Functions    ##### 
##################################

	async def _get_next_queue(self, player):
		print('Next in queue')

		await player.stop()		
		if player.queue.is_empty:
			ctx = getattr(player,"tracks_ctx",None)

			print('Track end', ctx.guild)

			if not ctx: return

			print('End of Playlist')
		
		if getattr(player,"repeat", False):
			current = player.queue.get()
			player.queue.pop(current)

		if not player.queue.is_empty: player.queue.pop()

		if not getattr(player,"shuffle", False):
			if len(player.queue) > 0:
				original_queue = player.queue.copy()
				player.queue.clear()
				while True:
					try:
						if len(original_queue) > 0:
							for x in original_queue:
								rand_choice = random.choice(original_queue)
								player.queue.put(rand_choice)
								original_queue.remove(rand_choice)
						else:
							break
					except:
						pass

		if player.queue.is_empty:
			ctx = getattr(player,"tracks_ctx",None)

			print('Track end', ctx.guild)

			if not ctx: return

			print('End of Playlist')

		await self._check_play(player)


	async def _check_play(self, player, track_num=None):
		print('Track')
		if not player or not player.is_connected(): return print('Player not found')

		if player.is_playing() or player.is_paused(): return print('Player not playing or paused')
		
		if player.queue.is_empty: return print('queue empty')

		track = player.queue.get()

		if hasattr(track,"ctx"): player.track_ctx = track.ctx

		print('Now playing')
		print(player.track_ctx.guild)

		await player.play(track)

	#################################
	#####   Testing Functions   #####
	#################################

	@commands.command()
	async def get_node(self, ctx):
		node = wavelink.NodePool.get_node()
		await ctx.send('Current node: {0}'.format(node))

	@commands.command()
	async def get_player(self, ctx):
		node = wavelink.NodePool.get_node()
		print(node)
		print(node.players)
		print(node.get_player(ctx.guild))	

	@commands.command()
	async def mtest(self, ctx):
		player: wavelink.Player = await self.con_(ctx)
		tracks = await wavelink.YouTubeTrack.search(query='hello - adele', return_first=True) 
		print('tracks found: ', str(tracks))
		await player.play(tracks)

		#player.queue.put(tracks)
		#player.track_ctx = ctx
		#print(player.queue)

	@commands.command()
	async def test_ctx(self, ctx):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		
		if not player or not player.is_connected():
			player: wavelink.Player = await self.con_(ctx)

		if not player: return print('Player still not found')

		print(getattr(player, 'tracks_ctx', None))
		
	########################################
	### Disconnect and Connect Functions ###
	########################################

	@commands.command(name='fdisconnect')
	async def fdiscon_(self, ctx, channel: typing.Union[discord.VoiceChannel, discord.StageChannel]=None):
		try:
			channel = channel or  ctx.author.voice.channel
		except AttributeError:
			return await ctx.send('No voice channel to connect to. Please either provide one or join one.')


		vc: wavelink.Player = ctx.voice_client

		if not vc:
			player = wavelink.Player(dj=ctx.author)
			vc: wavelink.Player = await channel.connect(cls=player)
		
		await asyncio.sleep(1)

	
		try:
			await vc.disconnect(force=True)
		except Exception as e:
			print(e)

		await ctx.send(f'Force Disconnecting from **`{channel.name}`**', delete_after=30)
		
	@commands.command(name='disconnect')
	async def discon_(self, ctx):
		vc: wavelink.Player = ctx.voice_client

		if vc:
			if vc.is_connected:
				try:
					await vc.disconnect()
				except AttributeError as e:
					print(e)
					pass
			await ctx.send(f'Bot disconnected', delete_after=30)
		else:
			await ctx.send('Bot already disconnected')

	@commands.command(name='connect')
	async def con_(self, ctx, channel: typing.Union[discord.VoiceChannel, discord.StageChannel]=None):
		vc: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		
		try:
			channel = channel or ctx.author.voice.channel
		except AttributeError:
			return await ctx.send('No voice channel to discconnect from. Please either provide one or join one.')

		if len(channel.members) >= channel.user_limit and not channel.user_limit == 0:
			raise commands.DisabledCommand('Can not Join channel **`{}`** as too many users in the channel all ready `({}/{})`'.format(str(channel), len(channel.members), channel.user_limit))

		if vc:
			# if self.bot.voice.channel == ctx.author.voice.channel:
			await vc.move_to(channel)
			print(vc)

			print(vc.channel)
			print(ctx.author.voice.channel)	
		else:
			# player = wavelink.Player(dj=ctx.author)
			vc: wavelink.Player = await channel.connect(cls=wavelink.Player) 

		await ctx.send(f'Connecting to **`{channel.name}`**', delete_after=30)
		vc.tracks_ctx = ctx
		return vc

	###############################
	#####    Play Functions    ####
	###############################

	@commands.group(pass_context=True)
	async def play(self, ctx):
		"""[Subcom][Object]
		Play API
		Run command to find subcommands
		"""
		options = ['Spotify - sp', 'Youtube - yt', 'SoundCloud - sc']

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		desc = '\n - '.join(options)

		if ctx.invoked_subcommand is None:
			embed=discord.Embed(title="Play Commands", description=desc, color=col)
			await ctx.send(embed=embed)

	@play.command(name='yt')
	async def _yt(self, ctx, *, search:str = None):
		print("Connect to channel")
	
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		print(player)
		if not player or not player.is_connected():
			player: wavelink.Player = await self.con_(ctx)

		if not player: return print('Player still not found')
		
		tracks = await wavelink.YouTubeTrack.search(query=search) 
		print(type(tracks))

		if isinstance(tracks, wavelink.tracks.YouTubePlaylist):
			final_track =  [x for x in tracks.tracks]

		elif isinstance(tracks, list):
			_titles = [x.title for x in tracks]
			_total_tracks = [x for x in tracks]

			fuz = self.bot.get_cog('FuzzySearch')
			if not fuz:
				final_track = await wavelink.YouTubeTrack.search(query=search, return_first=True) 
			else:
				_return = 0
				if len(_total_tracks) > 1:
					_return = await fuz.fuzSelect(ctx, 'Youtube', _titles)
				
				if _return == None: return await ctx.send('Nothing selected')

				final_track = [_total_tracks[_return]]

		for x in final_track:
			x.ctx = ctx
			await player.queue.put(x)
		
		await self._check_play(player)
				
	@play.command(name='sc')
	async def _sc(self, ctx, *, search:str = None):
		print("Connect to channel")
	
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		print(player)
		if not player or not player.is_connected():
			player: wavelink.Player = await self.con_(ctx)

		if not player:
			print('Player still not found')

		tracks = await wavelink.SoundCloudTrack.search(query=search)

		if isinstance(tracks, list):
			_titles = [x.title for x in tracks]
			_total_tracks = [x for x in tracks]

			fuz = self.bot.get_cog('FuzzySearch')
			if not fuz:
				final_track = await wavelink.SoundCloudTrack.search(query=search, return_first=True) 
			else:
				_return = 0
				if len(_total_tracks) > 1:
					_return = await fuz.fuzSelect(ctx, 'Soundcloud', _titles)
				
				if _return == None: return await ctx.send('Nothing selected')

				final_track = [_total_tracks[_return]]

		for x in final_track:
			x.ctx = ctx
			await player.queue.put(x)
		
		await self._check_play(player)

	@play.command(name='sp')
	async def _sp(self, ctx, *, search = None):
		print("Connect to channel")
	
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		print(player)
		if not player or not player.is_connected():
			player: wavelink.Player = await self.con_(ctx)

		if not player:
			print('Player still not found')

		tracks = []

		if 'playlist' in search:
			async for track in spotify.SpotifyTrack.iterator(query=search, type=spotify.SpotifySearchType.playlist, partial_tracks=True):
				print(track)
				tracks.append(track)

		if 'album' in search:
			async for track in spotify.SpotifyTrack.iterator(query=search, type=spotify.SpotifySearchType.album, partial_tracks=True):
				tracks.append(track)

		if 'track' in search:
			async for track in spotify.SpotifyTrack.search(query=search, type=spotify.SpotifySearchType.track, partial_tracks=True):
				tracks.append(track)

		print(tracks)
		print(player)
		print(player.queue)

		for x in tracks:
			print(x)
			x.ctx = ctx
			player.queue.put(x)
		
		print('added items')
		print(player.queue)
		await self._check_play(player)

	####################################
	#####   Additional Functions   #####
	####################################

	@commands.command()
	async def stop(self, ctx):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		await player.stop()

	@commands.command()
	async def skip(self, ctx):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		self._get_next_queue(player)

	@commands.command()
	async def resume(self, ctx):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		if player.is_playing(): return

		await player.resume()

	@commands.command()
	async def pause(self, ctx):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		if player.is_paused(): return

		await player.pause()

	@commands.command()
	async def seek(self, ctx, _time: str = 0):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		if player.is_paused(): return

		await player.seek(_time)

	@commands.command()
	async def repeat(self, ctx, _repeat = False):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		player.repeat = repeat

	@commands.command()
	async def stop(self, ctx, vol: int = 100):
		player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
		if not player or not player.is_connected():
			return print('Player still not found')

		await player.set_volume(vol)