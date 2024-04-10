from typing_extensions import Self

import os
import time
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv, dotenv_values
load_dotenv()

token = os.getenv("TOKEN")

class Scrappy(commands.Bot):
        def __init__(self):
                intents = discord.Intents.none()
                intents.bans = True
                intents.dm_messages = True
                intents.dm_reactions = True
                intents.dm_typing = True
                intents.emojis = True
                intents.guild_messages = True
                intents.guild_reactions = True
                intents.guild_typing = True
                intents.guilds = True
                intents.integrations = True
                intents.invites = True
                intents.members = True
                intents.messages = True
                intents.presences = True
                intents.reactions = True
                intents.typing = True
                intents.voice_states = True
                intents.webhooks = True
                intents.message_content = True
                allowed_mentions = discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)

                super().__init__(command_prefix=self.get_pre, pm_help=None, description="I'm a really boy ...", game=" with Scooby Chan", case_insensitive=True, intents=intents, allowed_mentions=allowed_mentions)

        async def get_pre(self, bot, message):
                guild = message.guild.id
                set_cog = bot.get_cog('Settings')
                _prefix = os.getenv("PREFIX")
                prefix = '$' if _prefix == "" else _prefix
                return prefix

        async def on_ready(self):
                print("Bot initializing")
                if not bot.get_cog('Settings'):
                        if os.path.exists('Cogs/Settings.py'):
                                await bot.load_extension('Cogs.Settings')
                        else: 
                                print('Missing settings')

                if not bot.get_cog('CogLoader'):
                        # Occasionally this can fail
                        try:
                                await bot.load_extension('Cogs.Cogloader')
                                cog_loader = bot.get_cog('Cogloader')
                                await cog_loader._load_extension()

                                await bot.wait_until_ready()
                                cog_loader.loaded()

                        except Exception as e:
                                print('Cogloader already loaded')
                                print(e)

        async def on_typing(self, channel, user, when):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates ontyping function if it exists
                                await cog.ontyping(channel, user, when)
                        except AttributeError:
                                continue

        async def on_message(self, message): # Need to fix this
                # Post the context too
                context = await bot.get_context(message)
                bot.dispatch("message_context", context, message)

                if not message.guild:
                        # This wasn't said in a server, process commands, then return
                        await bot.process_commands(message)
                        return

                if message.author.bot:
                        # We don't need other bots controlling things we do.
                        return

                try:
                        message.author.roles
                except AttributeError:
                        # Not a User
                        await bot.process_commands(message)
                        return

                # Check if we need to ignore or delete the message
                # or respond or replace

                ignore = delete = react = respond = False
                x = False

                check = None

                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                try:
                                        check = await cog.onmessage(message)
                                except TypeError as e:
                                        if bot.debug: print(cog); print(type(message)); print(message)
                                        print('########## Big error :P #############')
                                        print(e)

                        except AttributeError:
                                # Onto the next
                                continue
                        # Make sure we have things formatted right

                        if not type(check) is dict:
                                check = {}
                        if check.get("Delete",False):
                                delete = True
                        if check.get("Ignore",False):
                                ignore = True
                        try: respond = check['Respond']
                        except KeyError: pass
                        try: react = check['Reaction']
                        except KeyError: pass

                if delete:
                        # We need to delete the message - top priority
                        await message.delete()

                if not ignore:
                        # We're processing commands here
                        if respond:
                                # We have something to say
                                await message.channel.send(respond)
                        if react:
                                # We have something to react with
                                for r in react:
                                        await message.add_reaction(r)
                        await bot.process_commands(message)

        async def on_guild_join(self, message):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates onmessage function if it exists
                                await cog.onguildjoin(message)
                        except AttributeError:
                                continue

        async def on_guild_remove(self, message):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates onmessage function if it exists
                                await cog.onguildremove(message)
                        except AttributeError:
                                continue

        async def on_member_join(self, message):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates onmessage function if it exists
                                await cog.onmemberjoin(message)
                        except AttributeError:
                                continue

        async def on_member_remove(self, message):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates onmessage function if it exists
                                await cog.onmemberremove(message)
                        except AttributeError:
                                continue

        async def on_raw_reaction_add(self, payload):
                for cog in bot.cogs:
                        cog = bot.get_cog(cog)
                        try:
                                # Initiates onmessage function if it exists
                                await cog.onrawreactionadd(payload)
                        except AttributeError:
                                continue

        async def on_command_error(self, ctx, error):
                await ctx.reply(error, ephemeral = True)

bot = Scrappy()
bot.res = time.localtime()
bot.debug = False

bot.color = [
        discord.Color.teal(), 
        discord.Color.dark_teal(), 
        discord.Color.green(),
        discord.Color.dark_green(),
        discord.Color.blue(),
        discord.Color.dark_blue(),
        discord.Color.purple(),
        discord.Color.dark_purple(),
        discord.Color.magenta(),
        discord.Color.dark_magenta(),
        discord.Color.gold(),
        discord.Color.dark_gold(),
        discord.Color.orange(),
        discord.Color.dark_orange(),
        discord.Color.red(),
        discord.Color.dark_red(),
        discord.Color.lighter_grey(),
        discord.Color.dark_grey(),
        discord.Color.light_grey(),
        discord.Color.darker_grey(),
        discord.Color.blurple(),
        discord.Color.greyple()
]

@bot.hybrid_command(name = "bhping", with_app_command = True, description = "Pings bot")
@app_commands.guilds(discord.Object(id=477041170078498829))
async def _bhping(ctx: commands.Context):
        """
        Ping response
        """ 
        await ctx.defer(ephemeral = True)
        await ctx.reply('Bot Ping')

bot.run(token, reconnect=True)