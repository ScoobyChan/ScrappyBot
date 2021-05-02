import os
import sys
import subprocess
import discord
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Scripttest(bot, settings))


class Scripttest(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def python(self, ctx, *, script):
		"""Script
		Tests the python script and sends the results back for it"""
		if not os.path.exists('Script') and os.path.exists('Bot.py'):
			os.mkdir('Script')

		f= open(f"Script/script.py","w+")
		f.write(script)
		f.close() 

		# check os type
		
		scr = subprocess.run(['python3' if sys.platform != 'win32' else 'python', 'Script/script.py'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
		msg = 'Script input:\n```python\n{}\n```\nScript output:\n```python\n{}\n```'.format(script, scr.stdout if scr.stdout else scr.stderr)
		
		# await ctx.send(msg)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			title = 'Python Script Checker',
			description = msg,
			colour = col
		)
		await ctx.send(embed=embed)