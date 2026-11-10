import os
from typing import Any
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from Bot_Configuration import Bot_Configuration

token = os.getenv("TOKEN")

# logging.debug(f"Token loaded: {token}")

class Scrappy(commands.Bot):    
        def __init__(self, **kwargs):
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

        async def dispatch_cog_event(
                self,
                event_name: str,
                *args: Any,
                **kwargs: Any
        ) -> None:
                """Call a custom event handler on every loaded cog."""
                for cog in self.cogs.values():
                        handler = getattr(cog, event_name, None)
                        if not callable(handler):
                                continue
                        try:
                                await handler(*args, **kwargs)
                        except Exception:
                                logger.exception(
                                        "Error executing %s in %s",
                                        event_name,
                                        cog.__class__.__name__,
                                )

        async def get_pre(self, bot: commands.Bot, message: discord.Message) -> str:
                guild = str(message.guild.id) if message.guild else None
                _prefix = os.getenv("PREFIX", "$")
                guild_prefix = None
                Database_int = self.get_cog("Database_interact")
                if Database_int:
                        total_guild = Database_int.get_database_item("guild_prefix")
                        if total_guild:
                                guild_prefix = total_guild.get(guild, None)
                if not guild_prefix:
                        prefix = '$' if (_prefix == "" or _prefix == None) else _prefix
                else:
                        prefix = guild_prefix
                return prefix

        async def setup_hook(self) -> None:
                logging.info("Initiating Setup Hook")
                for cog in self.preloads:
                        path = f"Cogs/{cog}.py"
                        if not os.path.exists(path):
                                logger.warning("Missing cog %s", cog)
                                continue
                        logger.info("Loading cog %s", cog)
                        try:
                                Cogloader = self.get_cog('Cogloader')
                                if Cogloader:
                                        await Cogloader._load_extension(progress_bar=True)
                                        self.load_extension(f"Cogs.{cog}")
                        except Exception:
                                logger.exception("Failed loading cog %s", cog)

                for file in Path("Cogs").glob("*.py"):
                        if file.stem == "__init__":
                                continue

                        try:
                                self.load_extension(f"Cogs.{file.stem}")
                                logging.info(f"Loaded {file.stem}")
                        except Exception as e:
                                logging.error(f"Failed loading {file.stem}: {e}")

                await self.tree.sync()

        async def on_ready(self):
                logging.info("Bot initializing")
                # Get Cogloader and load items

                try:
                        logging.info("Debug: {}".format("turned on" if self.debug else "turned off"))
                except AttributeError:
                        logging.info("Debug: turned off")

                logging.info("Bot is ready :)")

        async def on_typing(self, channel, user, when):
                for cog_name in self.cogs:
                        cog = self.get_cog(cog_name)
                        try:
                                # Initiates ontyping function if it exists
                                await cog.ontyping(channel, user, when)
                        except AttributeError:
                                continue

        async def on_message(self, message):  # Need to fix this
                # Post the context too
                context = await self.get_context(message)
                self.dispatch("message_context", message)
                if not message.guild:
                        # This wasn't said in a server, process commands, then return
                        await self.process_commands(message)
                        return
                if message.author.bot:
                        # We don't need other bots controlling things we do.
                        return
                try:
                        message.author.roles
                except AttributeError:
                        # Not a User
                        await self.process_commands(message)
                        return

                # Check if we need to ignore or delete the message, or respond or replace
                ignore = delete = False
                check = None
                responses: list[str] = []
                reactions: list[str] = []
                for cog in self.cogs.values():
                        try:
                                try:
                                        check = await cog.onmessage(message)
                                except TypeError as e:
                                        if self.debug:
                                                logging.debug(cog)
                                                logging.debug(type(message))
                                                logging.debug(message)
                                        logging.error('########## Big error :P #############')
                                        logging.error(e)
                        except AttributeError as e:
                                # Onto the next
                                logging.error("AttributeError in cog {}: {}".format(cog.__class__.__name__, e))
                                continue
                        if not isinstance(check, dict):
                                check = {}
                        if check.get("Delete", False):
                                delete = True
                        if check.get("Ignore", False):
                                ignore = True
                        if "Respond" in check:
                                responses.append(check["Respond"])
                        if "Reaction" in check:
                                reactions.extend(check["Reaction"])

                if delete:
                        # We need to delete the message - top priority
                        try:
                                await message.delete()
                        except discord.Forbidden:
                                logger.warning("Missing permissions to delete message %s", message.id)
                        except discord.NotFound:
                                pass
                if not ignore:
                        # We're processing commands here
                        for response in responses:
                                await message.channel.send(response)
                        for reaction in reactions:
                                await message.add_reaction(reaction)
                        await self.process_commands(message)

        async def on_guild_remove(self, guild: discord.Guild) -> None:
                await self.dispatch_cog_event("onguildremove", guild)

        async def on_member_join(self, member: discord.Member) -> None:
                await self.dispatch_cog_event("onmemberjoin", member)

        async def on_member_remove(self, member: discord.Member) -> None:
                await self.dispatch_cog_event("onmemberremove", member)

        async def on_raw_reaction_add(
                self,
                payload: discord.RawReactionActionEvent
        ) -> None:
                await self.dispatch_cog_event("onrawreactionadd", payload)


# async def on_command_error(self, ctx, error):
#       await ctx.reply(error)

bot = Scrappy()
if not token:
        raise RuntimeError("Discord token not found in environment")

logging.info("Starting bot...")
bot.run(token, reconnect=True)