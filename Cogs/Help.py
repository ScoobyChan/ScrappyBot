
from os import name
from typing import Optional, Set
import discord
from discord.ext import commands
from collections import Counter
from discord import app_commands
from discord import Embed

async def setup(bot: commands.Bot) -> None:
	# bot.remove_command("help")
	settings = bot.get_cog("Settings")
	await bot.add_cog(Help(bot, settings))

class HelpDropdown(discord.ui.Select):
	def __init__(self, help_command: "MyHelp", options: list[discord.SelectOption]):
		super().__init__(placeholder="Choose a Category...", min_values=1, max_values=1, options=options)
		self._help_command = help_command

	async def callback(self, interaction: discord.Interaction):
		embed = (
			await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
			if self.values[0] != self.options[0].value
			else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
		)
		await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
	def __init__(self, help_command: "MyHelp", options: list[discord.SelectOption], *, timeout: Optional[float] = 120.0):
		super().__init__(timeout=timeout)
		self.add_item(HelpDropdown(help_command, options))
		self._help_command = help_command
	
	async def on_timeout(self) -> None:
		self.clear_items()
		if await self._help_commandresponse: await self._help_command.response.edit(view=self)

	async def interation_check(self, interaction: discord.Interaction) -> bool:
		return self._help_command.context.author == interaction.user

class MyHelp(commands.MinimalHelpCommand):
	def get_command_signature(self, command):
		return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

	async def _cog_select_options(self) -> list[discord.SelectOption]:
		options: list[discord.SelectOption] = []
		options.append(discord.SelectOption(
			label="Home",
            emoji="🏠",
			description="Go back to main menu.",
		))

		for cog, command_set in self.get_bot_mapping().items():
			filtered = await self.filter_commands(command_set, sort=True)
			if not filtered: continue

			emoji = getattr(cog, "COG_EMOJI", None)
			options.append(discord.SelectOption(
				label=cog.qualified_name if cog else "No Category",
				emoji=emoji,
				description=cog.description[:100] if cog and cog.description else None,
			))

		return options

	async def _help_embed(self, 
					   title: str, 
					   description: Optional[str] = None , 
					   mapping: Optional[str] = None ,
					   command_set: Optional[Set[commands.Command]] = None,
					   set_author: bool = True
					   ) -> Embed:
		embed = Embed(title=title)
		if description:
			embed.description = description

		if set_author:
			avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
			embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)

		if command_set:
			filtered = await self.filter_commands(command_set, sort=True)

			for command in filtered:
				embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False )

		elif mapping:
			for cog, command_set in mapping.items():
				filtered = await self.filter_commands(command_set, sort=True)
				if not filtered: continue

				name = cog.qualified_name if cog else "No Category"
				cmd_list = "\u2002".join(
					f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
				)
				value = (
					f"{cog.description}\n{cmd_list}"
					if cog and cog.description
					else cmd_list
				)

				embed.add_field(name=name, value=value)
		
		embed.colour = self.context.author.top_role.colour or None
		return embed

	async def bot_help_embed(self, mapping: dict) -> Embed:
		return await self._help_embed(
			title='Bot commands',
			description=self.context.bot.description,
			mapping=mapping,
			set_author=True
		)

	async def send_bot_help(self, mapping: dict):
		embed = await self.bot_help_embed(mapping)
		options = await self._cog_select_options()
		await self.get_destination().send(embed=embed, view=HelpView(self, options))

	async def cog_help_embed(self, cog: commands.Cog ) -> Embed:
		if cog is None:
			return await self._help_embed(
				title='No Category',
				command_set=self.get_bot_mapping()[None]
			)
		
		emoji = getattr(cog, "COG_EMOJI", None)
		return await self._help_embed(
			title=f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name,
			description=cog.description,
			command_set=cog.get_commands(),
			set_author=True
		)

	async def send_cog_help(self, cog: commands.Cog):
		embed = await self.cog_help_embed(cog)
		await self.get_destination().send(embed=embed)

	async def send_command_help(self, command: commands.Command):
		embed = await self._help_embed(
			title=command.qualified_name,
			description=command.help,
			command_set=command.commands if isinstance(command, commands.Group) else None,
			set_author=True
		)
		await self.get_destination().send(embed=embed)

	send_group_help = send_command_help

class Help(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self._original_help = bot.help_command
		bot.help_command = MyHelp()
		bot.help_command.cog = self
		
	@commands.Cog.listener()
	async def on_unloaded_extension(self, ext):
		self.bot.help_command = self._original_help

	@commands.hybrid_command(name = "oldhelp", with_app_command = True, description = "Old help before improvement")
	@app_commands.guilds(discord.Object(id=477041170078498829))
	async def oldhelp(self, ctx):
		"""Old help before improvement"""
		await ctx.send('Help me :sob:')

	@commands.hybrid_command(name = "listcogs", with_app_command = True, description = "Lists cogs")
	@app_commands.guilds(discord.Object(id=477041170078498829))
	async def listcogs(self, ctx):
		"""Lists the different Cogs"""
		desc = [str(c) for c in self.bot.cogs.keys()]
		desc.remove('Settings')
		desc.sort()

		col = ctx.author.top_role.colour or self.settings.randomColor()

		embed = discord.Embed(
			title = 'Cogs',
			description = desc,
			colour = col
		)	
		await ctx.send(embed=embed)

	@commands.hybrid_command(name = "dumphelp", with_app_command = True, description = "Dumps help commands and cogs")
	@app_commands.guilds(discord.Object(id=477041170078498829))
	async def dumphelp(self, ctx):
		"""Puts all the help commands into a text file"""
		# remake this
		return