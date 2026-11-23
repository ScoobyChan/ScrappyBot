import discord
from discord.ext import commands


class Help(commands.Cog):
    """Modern help command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Shows all commands or information about a specific command."
    )
    async def help(self, ctx: commands.Context, *, command_name: str = None):
        if command_name is None:
            await self.send_bot_help(ctx)
        else:
            await self.send_command_help(ctx, command_name)

    async def send_bot_help(self, ctx):
        embed = discord.Embed(
            title=f"{self.bot.user.name} Help",
            description="Available command categories",
            colour=discord.Colour.blurple()
        )

        for cog_name, cog in self.bot.cogs.items():
            commands_list = []

            for command in cog.get_commands():
                if command.hidden:
                    continue

                try:
                    if await command.can_run(ctx):
                        commands_list.append(f"`{command.name}`")
                except commands.CheckFailure:
                    pass

            if commands_list:
                embed.add_field(
                    name=f"📁 {cog_name}",
                    value=" ".join(commands_list),
                    inline=False
                )

        embed.set_footer(
            text=f"Use {ctx.clean_prefix}help <command> for more information"
        )

        await ctx.send(embed=embed)

    async def send_command_help(self, ctx, command_name: str):
        command = self.bot.get_command(command_name)

        if not command:
            return await ctx.send(
                f"❌ Command `{command_name}` not found."
            )

        embed = discord.Embed(
            title=f"📖 {command.qualified_name}",
            colour=discord.Colour.green()
        )

        embed.add_field(
            name="Description",
            value=command.help or command.description or "No description provided.",
            inline=False
        )

        usage = (
            f"{ctx.clean_prefix}{command.qualified_name} "
            f"{command.signature}"
        )

        embed.add_field(
            name="Usage",
            value=f"```{usage}```",
            inline=False
        )

        if command.aliases:
            embed.add_field(
                name="Aliases",
                value=", ".join(f"`{a}`" for a in command.aliases),
                inline=False
            )

        cog_name = command.cog_name or "No Category"

        embed.add_field(
            name="Category",
            value=cog_name,
            inline=False
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))