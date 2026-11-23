import discord
from discord.ext import commands


class HelpPaginator(discord.ui.View):
    def __init__(self, ctx, categories):
        super().__init__(timeout=180)

        self.ctx = ctx
        self.categories = categories
        self.category_names = list(categories.keys())

        self.current_category = 0
        self.current_page = 0

        self.add_item(CategorySelect(self))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.ctx.author.id

    def get_commands(self):
        category = self.category_names[self.current_category]
        return self.categories[category]

    def max_pages(self):
        cmds = self.get_commands()
        return max(1, (len(cmds) + 5) // 6)

    async def update_message(self, interaction):
        embed = self.build_embed()

        self.previous.disabled = self.current_page == 0
        self.next.disabled = self.current_page >= self.max_pages() - 1

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

    def build_embed(self):
        category = self.category_names[self.current_category]
        commands_list = self.categories[category]

        start = self.current_page * 6
        end = start + 6

        embed = discord.Embed(
            title=f"📚 {category}",
            colour=discord.Colour.blurple()
        )

        for command in commands_list[start:end]:
            embed.add_field(
                name=f"/{command.qualified_name}",
                value=command.help or "No description provided.",
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
        self.current_page += 1
        await self.update_message(interaction)


class CategorySelect(discord.ui.Select):
    def __init__(self, paginator):
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

    async def callback(self, interaction: discord.Interaction):
        self.paginator.current_category = (
            self.paginator.category_names.index(self.values[0])
        )
        self.paginator.current_page = 0

        await self.paginator.update_message(interaction)