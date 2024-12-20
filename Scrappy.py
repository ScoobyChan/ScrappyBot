from typing_extensions import Self
import os
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

from Bot_Configuration import Bot_Configuration

token = os.getenv("token")

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

                self.preloads = Bot_Configuration.preloads()
                self.settings = Bot_Configuration.settings()
                self.res = Bot_Configuration.res()
                self.color = Bot_Configuration.color()

        async def get_pre(self, bot, message):
                guild = str(message.guild.id)
                _prefix = os.getenv("prefix")

                guild_prefix = None
                Database_int = bot.get_cog("Database_interact")
                if Database_int:
                        total_guild = Database_int.get_database_item("guild_prefix")
                        if total_guild: 
                                guild_prefix = total_guild.get(guild, None)

                if not guild_prefix:
                        prefix = '$' if (_prefix == "" or _prefix == None) else _prefix
                else:
                        prefix = guild_prefix
                        
                return prefix

        async def on_ready(self):
                print("Bot initializing")
                # Check does Cogs exist
                if os.path.exists("Cogs"):
                        for x in self.preloads:
                                if not bot.get_cog(x):
                                        if os.path.exists('Cogs/{}.py'.format(x)):
                                                print("Loading: {}".format(x))
                                                cog = 'Cogs.{}'.format(x)
                                                bot.load_extension(cog)
                                                bot.dispatch("loaded_extension", bot.extensions.get(cog))
                                        else: 
                                                print('Missing {}'.format(x))
                        
                bot.preloads = self.preloads
                await bot.wait_until_ready()
                # Get Cogloader and load items

                Cogloader = bot.get_cog('Cogloader')
                if Cogloader: await Cogloader._load_extension(progress_bar=True)

                try:
                        print("Debug: {}".format("turned on" if bot.debug else "turned off"))
                except AttributeError:
                        print("Debug: turned off")
                print("Bot is ready :)")

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

        # async def on_command_error(self, ctx, error):
        #         await ctx.reply(error)

bot = Scrappy()
bot.run(token, reconnect=True)