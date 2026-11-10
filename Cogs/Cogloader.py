import os
import sys
import datetime
import time
import discord
from discord.ext import commands
import traceback
import random
from progress.bar import Bar

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup(bot: commands.Bot) -> None:
        bot.add_cog(Cogloader(bot))

start_time = time.time()

class Cogloader(commands.Cog):
        def __init__(self, bot):
                self.bot = bot
                self.bot.start_time = discord.utils.utcnow()

        def loaded(self) -> None:
                logger.info('Loaded {} {}'.format(len(self.bot.cogs), 'Cog' if len(self.bot.cogs) < 2 else 'Cogs'))
                logger.info('Logged in as:{0} (ID: {0.id})\n'.format(self.bot.user))
                logger.info('{}/{}/{}, {}:{}:{}\n'.format(self.bot.start_time.day if len(str(self.bot.start_time.day)) > 1 else ('0' + str(self.bot.start_time.day)), self.bot.start_time.month if len(str(self.bot.start_time.month)) > 1 else ('0' + str(self.bot.start_time.month)), self.bot.start_time.year, self.bot.start_time.hour if len(str(self.bot.start_time.hour)) > 1 else ('0' + str(self.bot.start_time.hour)), self.bot.start_time.minute if len(str(self.bot.start_time.minute)) > 1 else ('0' + str(self.bot.start_time.minute)), self.bot.start_time.second if len(str(self.bot.start_time.second)) > 1 else ('0' + str(self.bot.start_time.second))))
                logger.info("Invite Link:\nhttps://discord.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n".format(self.bot.user.id))

        async def _load_extension(self, sel_cog=None, progress_bar=None) -> None:
                # Find cogs to load
                directory = "Cogs"
                if not os.path.exists(directory): return
                cog_list = os.listdir(directory)

                if '__pycache__' in cog_list: cog_list.remove('__pycache__')

                # Check if any are loaded already
                current_loaded = set(self.bot.extensions.keys())

                if sel_cog:
                        sel_cog = sel_cog if sel_cog.endswith('.py') else "{}.py".format(sel_cog)
                        if sel_cog in cog_list:
                                to_be_loaded = [sel_cog]
                        else:
                                return
                else:
                        to_be_loaded = cog_list

                bar = None
                if progress_bar: bar = Bar('Loading Modules', fill="*", max=len(to_be_loaded))

                for loading in to_be_loaded:
                        if loading.endswith(".py"): loading = loading[:len(loading)-3] 
                        if not loading in current_loaded:
                                cog = '{}.{}'.format(directory, loading)
                                try:
                                        if not self.bot.get_cog(loading):
                                                self.bot.load_extension(cog)
                                                self.bot.dispatch("loaded_extension", self.bot.extensions.get(cog))
                                                logger.info('Loaded {}'.format(loading))
                                except Exception as error:
                                        logger.error('{} cannot be loaded. [{}]'.format(loading, error))
                                        logger.error(str("".join(traceback.format_exception(type(error), error, error.__traceback__))))

                        if bar: bar.next()
                if bar: bar.finish()

        async def _unload_extension(self, sel_cog=None) -> None:
                directory = "Cogs"
                if not os.path.exists(directory): return

                if sel_cog: 
                        sel_cog = sel_cog if sel_cog.endswith('.py') else "{}.py".format(sel_cog)
                        if sel_cog in self.bot.extensions:
                                to_be_unloaded = [sel_cog]
                        else:
                                return
                else:
                        to_be_unloaded = list(self.bot.extensions.keys())

                for preload in self.bot.preloads:
                        if preload in to_be_unloaded:
                                to_be_unloaded.remove(preload)

                for c in to_be_unloaded:
                        cog = '{}.{}'.format(directory, c)
                        try:
                                if self.bot.get_cog(c):
                                        self.bot.dispatch("unloaded_extension", self.bot.extensions.get(cog))
                                        self.bot.unload_extension(cog)
                        except Exception as error:
                                logger.error('{} cannot be unloaded. [{}]'.format(c, error))

        @commands.command(aliases=['r'])
        @commands.is_owner()
        async def reload(self, ctx, args: str = None) -> None:
                """
                reloads bot
                """
                msg = await ctx.send('Reloading Cogs')
                
                self.reload_lock = asyncio.Lock()
                async with self.reload_lock:
                        await self._unload_extension(args)
                        await self._load_extension(args)
                await self._unload_extension(args)
                await self._load_extension(args)

                await msg.edit(content='Cogs Successfully reloaded')

        @commands.command(aliases=['l'])
        @commands.is_owner()
        async def load(self, ctx, args: str = None) -> None:
                """
                [cog]
                loads a cog or all of them
                """
                await self._load_extension(args)
                await ctx.send('Cogs Successfully loaded')

        @commands.command(aliases=['unl'])
        @commands.is_owner()
        async def unload(self, ctx, args: str = None) -> None:
                """
                [unloads cog]
                """
                await self._unload_extension(args)
                await ctx.send('Cogs Successfully unloaded')

        @commands.command(aliases=['cc'])
        @commands.is_owner()
        async def clearCon(self, ctx):
                """
                clears the console
                """
                await ctx.message.delete()
                if not 'win' in sys.platform:
                        os.system('clear')
                else:
                        os.system('cls')

        @commands.command()
        @commands.is_owner()
        async def ClearCache(self, ctx) -> None:
                """
                Clears the Cache
                """
                cache_dir = Path("Cogs/__pycache__")
                await self._unload_extension()
                if cache_dir.exists():
                        for o in os.listdir(cache_dir):
                                if not o.startswith('CogLoader') and not o.startswith('Settings') and not o.startswith('BotControl'):
                                        os.remove(cache_dir)

                #  self._load_extension()

                await ctx.send('Cache has been removed')

        @commands.command()
        @commands.is_owner()
        async def Cogloaded(self, ctx) -> None:
                """
                Shows Cogs loaded
                """
                await ctx.send('{}'.format([str(c) for c in self.bot.extensions.keys()]))

        @commands.command()
        async def uptime(self, ctx) -> None:
                """
                prints uptime of bot
                """
                current_time = time.time()
                difference = int(round(current_time - self.bot.start_time.timestamp()))
                text = str(datetime.timedelta(seconds=difference))

                col = ctx.author.top_role.colour or random.choice(self.bot.color)

                embed = discord.Embed(title=text, color=col)
                await ctx.send(embed=embed)