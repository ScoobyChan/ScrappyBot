from __future__ import annotations

import discord
import wavelink

from discord.ext import commands
from collections import deque
import random
import logging


logger = logging.getLogger(__name__)


class MusicPlayer:
    def __init__(self):
        self.queue = deque()
        self.loop = False
        self.shuffle = False
        self.autoplay = True

    def get_next_track(self):
        if not self.queue:
            return None

        if self.shuffle:
            track = random.choice(list(self.queue))
            self.queue.remove(track)
            return track

        return self.queue.popleft()


class Music(commands.Cog):
    """Modern Music System"""

    def __init__(self, bot):
        self.bot = bot
        self.players: dict[int, MusicPlayer] = {}

    def get_player(self, guild_id: int):
        if guild_id not in self.players:
            self.players[guild_id] = MusicPlayer()

        return self.players[guild_id]

    async def get_voice_client(
        self,
        ctx: commands.Context
    ) -> wavelink.Player:

        if not ctx.author.voice:
            logger.warning(
                "Voice join rejected: guild=%s user=%s is not connected to a voice channel",
                ctx.guild.id if ctx.guild else None,
                ctx.author.id,
            )
            raise commands.CommandError(
                "You must be connected to a voice channel."
            )

        player: wavelink.Player
        voice_channel = ctx.author.voice.channel

        if not ctx.voice_client:
            logger.info(
                "Joining voice channel: guild=%s channel=%s user=%s",
                ctx.guild.id if ctx.guild else None,
                getattr(voice_channel, "id", None),
                ctx.author.id,
            )
            try:
                player = await voice_channel.connect(cls=wavelink.Player)
            except Exception:
                logger.exception(
                    "Failed to join voice channel: guild=%s channel=%s user=%s",
                    ctx.guild.id if ctx.guild else None,
                    getattr(voice_channel, "id", None),
                    ctx.author.id,
                )
                raise

        else:
            player = ctx.voice_client
            logger.debug(
                "Using existing voice client: guild=%s channel=%s user=%s",
                ctx.guild.id if ctx.guild else None,
                getattr(player.channel, "id", None),
                ctx.author.id,
            )

        return player

    @commands.hybrid_command()
    async def play(self, ctx, *, query: str):

        player = await self.get_voice_client(ctx)

        guild_id = ctx.guild.id if ctx.guild else None
        logger.info(
            "Music play requested: guild=%s user=%s query=%r",
            guild_id,
            ctx.author.id,
            query,
        )

        try:
            tracks = await wavelink.Playable.search(query)
        except Exception:
            logger.exception(
                "Track search failed: guild=%s user=%s query=%r",
                guild_id,
                ctx.author.id,
                query,
            )
            raise

        if not tracks:
            logger.warning(
                "No tracks found: guild=%s user=%s query=%r",
                guild_id,
                ctx.author.id,
                query,
            )
            return await ctx.send("No results found.")

        #
        # Playlist
        #
        if isinstance(tracks, wavelink.Playlist):

            player_data = self.get_player(ctx.guild.id)

            for track in tracks.tracks:
                player_data.queue.append(track)

            embed = discord.Embed(
                title="📑 Playlist Added",
                description=tracks.name,
                colour=discord.Colour.green()
            )

            embed.add_field(
                name="Tracks",
                value=len(tracks.tracks)
            )

            await ctx.send(embed=embed)

            if not player.playing:
                next_track = player_data.queue.popleft()
                logger.info(
                    "Starting playlist: guild=%s tracks=%s first_track=%r",
                    guild_id,
                    len(tracks.tracks),
                    getattr(next_track, "title", str(next_track)),
                )
                try:
                    await player.play(next_track)
                except Exception:
                    logger.exception(
                        "Failed to start playlist track: guild=%s track=%r",
                        guild_id,
                        getattr(next_track, "title", str(next_track)),
                    )
                    raise

            return

        #
        # Single Track
        #
        track = tracks[0]

        if player.playing:
            self.get_player(ctx.guild.id).queue.append(track)
            logger.info(
                "Track queued: guild=%s track=%r queue_size=%s",
                guild_id,
                track.title,
                len(self.get_player(ctx.guild.id).queue),
            )

            return await ctx.send(
                f"✅ Queued **{track.title}**"
            )

        logger.info(
            "Starting track: guild=%s track=%r author=%r",
            guild_id,
            track.title,
            track.author,
        )
        try:
            await player.play(track)
        except Exception:
            logger.exception(
                "Failed to start track: guild=%s track=%r author=%r",
                guild_id,
                track.title,
                track.author,
            )
            raise

        await ctx.send(
            f"🎵 Now playing **{track.title}**"
        )

    @commands.hybrid_command()
    async def skip(self, ctx):
        """Skip current track"""

        player: wavelink.Player = ctx.voice_client

        if not player:
            return await ctx.send("Not connected.")

        await player.skip()

        await ctx.send("⏭️ Skipped.")

    @commands.hybrid_command()
    async def pause(self, ctx):
        """Pause music"""

        player = ctx.voice_client

        if player:
            await player.pause(True)

        await ctx.send("⏸️ Paused.")

    @commands.hybrid_command()
    async def resume(self, ctx):
        """Resume music"""

        player = ctx.voice_client

        if player:
            await player.pause(False)

        await ctx.send("▶️ Resumed.")

    @commands.hybrid_command()
    async def stop(self, ctx):
        """Stop playback"""

        player = ctx.voice_client

        if not player:
            return

        guild_player = self.get_player(ctx.guild.id)

        guild_player.queue.clear()

        await player.disconnect()

        await ctx.send("🛑 Disconnected.")

    @commands.hybrid_command()
    async def shuffle(self, ctx):

        player_state = self.get_player(ctx.guild.id)

        player_state.shuffle = not player_state.shuffle

        embed = discord.Embed(
            title="🔀 Shuffle",
            description=(
                "Enabled"
                if player_state.shuffle
                else "Disabled"
            ),
            colour=discord.Colour.blurple()
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def shufflequeue(self, ctx):

        player_state = self.get_player(ctx.guild.id)

        items = list(player_state.queue)

        if len(items) < 2:
            return await ctx.send(
                "Need at least two songs."
            )

        random.shuffle(items)

        player_state.queue.clear()
        player_state.queue.extend(items)

        await ctx.send(
            "🔀 Queue shuffled."
        )

    @commands.hybrid_command()
    async def autoplay(self, ctx):

        player_state = self.get_player(ctx.guild.id)

        player_state.autoplay = (
            not player_state.autoplay
        )

        await ctx.send(
            f"📻 Autoplay {'Enabled' if player_state.autoplay else 'Disabled'}"
        )

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self,
        payload: wavelink.TrackEndEventPayload
    ):

        player = payload.player
        logger.info(
            "Track ended: guild=%s track=%r reason=%r",
            player.guild.id,
            getattr(payload.track, "title", str(payload.track)),
            getattr(payload, "reason", None),
        )

        state = self.get_player(
            player.guild.id
        )

        #
        # Loop current song
        #
        if state.loop:
            try:
                await player.play(payload.track)
                logger.info("Looping track: guild=%s", player.guild.id)
            except Exception:
                logger.exception(
                    "Failed to loop track: guild=%s track=%r",
                    player.guild.id,
                    getattr(payload.track, "title", str(payload.track)),
                )
            return

        #
        # Queue tracks
        #
        next_track = state.get_next_track()

        if next_track:
            try:
                await player.play(next_track)
                logger.info(
                    "Started queued track after track end: guild=%s track=%r",
                    player.guild.id,
                    getattr(next_track, "title", str(next_track)),
                )
            except Exception:
                logger.exception(
                    "Failed to start queued track: guild=%s track=%r",
                    player.guild.id,
                    getattr(next_track, "title", str(next_track)),
                )
            return

        #
        # Autoplay
        #
        if state.autoplay:

            try:
                recommendations = await (
                    wavelink.Playable.search(
                        payload.track.title
                    )
                )

                if recommendations:
                    recommendation = recommendations[0]
                    try:
                        await player.play(recommendation)
                        logger.info(
                            "Started autoplay track: guild=%s track=%r",
                            player.guild.id,
                            getattr(recommendation, "title", str(recommendation)),
                        )
                    except Exception:
                        logger.exception(
                            "Failed to start autoplay track: guild=%s track=%r",
                            player.guild.id,
                            getattr(recommendation, "title", str(recommendation)),
                        )
                else:
                    logger.warning(
                        "Autoplay found no recommendations: guild=%s source_track=%r",
                        player.guild.id,
                        getattr(payload.track, "title", str(payload.track)),
                    )

            except Exception:
                logger.exception(
                    "Autoplay recommendation search failed: guild=%s source_track=%r",
                    player.guild.id,
                    getattr(payload.track, "title", str(payload.track)),
                )

    @commands.hybrid_command()
    async def volume(
        self,
        ctx,
        volume: commands.Range[int, 1, 100]
    ):
        """Set volume"""

        player: wavelink.Player = ctx.voice_client

        if not player:
            return

        await player.set_volume(volume)

        await ctx.send(
            f"🔊 Volume set to **{volume}%**"
        )

    @commands.hybrid_command()
    async def nowplaying(self, ctx):
        """Show current track"""

        player: wavelink.Player = ctx.voice_client

        if not player or not player.current:
            return await ctx.send(
                "Nothing is playing."
            )

        track = player.current

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track.title}**",
            colour=discord.Colour.blurple()
        )

        embed.add_field(
            name="Artist",
            value=track.author
        )

        embed.add_field(
            name="Length",
            value=f"{track.length // 1000}s"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def queue(self, ctx):
        """Show queue"""

        guild_player = self.get_player(
            ctx.guild.id
        )

        if not guild_player.queue:
            return await ctx.send(
                "Queue is empty."
            )

        embed = discord.Embed(
            title="📜 Queue",
            colour=discord.Colour.blurple()
        )

        for i, track in enumerate(
            guild_player.queue,
            start=1
        ):
            embed.add_field(
                name=f"{i}. {track.title}",
                value=track.author,
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self,
        payload: wavelink.TrackEndEventPayload
    ):

        player = payload.player
        logger.info(
            "Track-end fallback listener: guild=%s track=%r reason=%r",
            player.guild.id,
            getattr(payload.track, "title", str(payload.track)),
            getattr(payload, "reason", None),
        )

        guild_player = self.get_player(
            player.guild.id
        )

        if guild_player.loop:
            try:
                await player.play(payload.track)
            except Exception:
                logger.exception(
                    "Fallback loop playback failed: guild=%s track=%r",
                    player.guild.id,
                    getattr(payload.track, "title", str(payload.track)),
                )
            return

        if guild_player.queue:
            next_track = guild_player.queue.popleft()
            try:
                await player.play(next_track)
            except Exception:
                logger.exception(
                    "Fallback queue playback failed: guild=%s track=%r",
                    player.guild.id,
                    getattr(next_track, "title", str(next_track)),
                )

    @commands.hybrid_command()
    async def loop(self, ctx):

        guild_player = self.get_player(
            ctx.guild.id
        )

        guild_player.loop = not guild_player.loop

        await ctx.send(
            f"🔁 Loop {'enabled' if guild_player.loop else 'disabled'}"
        )

    

class QueueView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=120)

        self.pages = pages
        self.page = 0

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(self, interaction, button):
        self.page = max(self.page - 1, 0)

        await interaction.response.edit_message(
            embed=self.pages[self.page],
            view=self
        )

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def next(self, interaction, button):
        self.page = min(
            self.page + 1,
            len(self.pages) - 1
        )

        await interaction.response.edit_message(
            embed=self.pages[self.page],
            view=self
        )

class MusicControls(discord.ui.View):

    @discord.ui.button(
        emoji="⏯️",
        style=discord.ButtonStyle.primary
    )
    async def play_pause(self,
                         interaction,
                         button):

        player = interaction.guild.voice_client

        if player.paused:
            await player.pause(False)
        else:
            await player.pause(True)

        await interaction.response.defer()

    @discord.ui.button(
        emoji="⏭️",
        style=discord.ButtonStyle.secondary
    )
    async def skip(self,
                   interaction,
                   button):

        await interaction.guild.voice_client.skip()
        await interaction.response.defer()

    @discord.ui.button(
        emoji="🔀",
        style=discord.ButtonStyle.success
    )
    async def shuffle(self,
                      interaction,
                      button):

        cog = interaction.client.get_cog(
            "Music"
        )

        state = cog.get_player(
            interaction.guild.id
        )

        state.shuffle = not state.shuffle

        await interaction.response.send_message(
            f"Shuffle {'ON' if state.shuffle else 'OFF'}",
            ephemeral=True
        )

    @discord.ui.button(
        emoji="🔁",
        style=discord.ButtonStyle.success
    )
    async def loop(self,
                   interaction,
                   button):

        cog = interaction.client.get_cog(
            "Music"
        )

        state = cog.get_player(
            interaction.guild.id
        )

        state.loop = not state.loop

        await interaction.response.send_message(
            f"Loop {'ON' if state.loop else 'OFF'}",
            ephemeral=True
        )

    @discord.ui.button(
        emoji="🛑",
        style=discord.ButtonStyle.danger
    )
    async def stop(self,
                   interaction,
                   button):

        await interaction.guild.voice_client.disconnect()
        await interaction.response.defer()
    


async def setup(bot):
    await bot.add_cog(Music(bot))