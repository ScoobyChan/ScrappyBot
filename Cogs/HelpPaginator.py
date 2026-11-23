import discord
from discord.ext import commands


async def setup(bot: commands.Bot) -> None:
    bot.help_command = None
    await bot.add_cog(HelpCog(bot))


class HelpPaginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, categories: dict[str, list[commands.Command]]):
        super().__init__(timeout=180)

        self.ctx = ctx
        self.categories = categories
        self.category_names = list(categories.keys())

        self.current_category = 0
        self.current_page = 0

        self.add_item(CategorySelect(self))
        self._sync_button_states()

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    def get_commands(self) -> list[commands.Command]:
        category = self.category_names[self.current_category]
        return self.categories[category]

    def max_pages(self) -> int:
        cmds = self.get_commands()
        return max(1, (len(cmds) + 5) // 6)

    def _sync_button_states(self) -> None:
        self.previous.disabled = self.current_page == 0
        self.next.disabled = self.current_page >= self.max_pages() - 1

    async def update_message(self, interaction: discord.Interaction) -> None:
        embed = self.build_embed()
        self._sync_button_states()

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

    def build_embed(self) -> discord.Embed:
        category = self.category_names[self.current_category]
        commands_list = self.categories[category]

        start = self.current_page * 6
        end = start + 6

        embed = discord.Embed(
            title=f"📚 {category}",
            colour=discord.Colour.blurple()
        )

        for command in commands_list[start:end]:
            description = command.short_doc or "No description provided."
            embed.add_field(
                name=f"{self.ctx.clean_prefix}{command.qualified_name}",
                value=description,
                inline=False
            )

        embed.set_footer(
            text=f"Page {self.current_page + 1}/{self.max_pages()}"
        )

        return embed

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current_page == 0:
            return
        self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(
        emoji="🏠",
        style=discord.ButtonStyle.primary
    )
    async def home(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.current_category = 0
        self.current_page = 0
        await self.update_message(interaction)

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current_page >= self.max_pages() - 1:
            return
        self.current_page += 1
        await self.update_message(interaction)


class CategorySelect(discord.ui.Select):
    def __init__(self, paginator: HelpPaginator):
        self.paginator = paginator

        options = [
            discord.SelectOption(
                label=name,
                emoji="📁"
            )
            for name in paginator.category_names
        ]

        super().__init__(
            placeholder="Choose a category...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        self.paginator.current_category = (
            self.paginator.category_names.index(self.values[0])
        )
        self.paginator.current_page = 0

        await self.paginator.update_message(interaction)


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        categories: dict[str, list[commands.Command]] = {}

        for command in sorted(self.bot.commands, key=lambda item: item.qualified_name.lower()):
            if command.hidden or not command.enabled:
                continue

            try:
                can_run = await command.can_run(ctx)
            except (commands.CheckFailure, commands.CommandError):
                continue

            if not can_run:
                continue

            cog_name = command.cog.qualified_name if command.cog else "No Category"
            categories.setdefault(cog_name, []).append(command)

        sorted_categories = sorted(categories.items(), key=lambda item: item[0].lower())
        if len(sorted_categories) > 25:
            first_categories = sorted_categories[:24]
            other_commands = [
                command
                for _, commands_in_category in sorted_categories[24:]
                for command in commands_in_category
            ]
            sorted_categories = first_categories + [("Other", other_commands)]

        paginator = HelpPaginator(ctx, dict(sorted_categories))
        await ctx.send(embed=paginator.build_embed(), view=paginator)