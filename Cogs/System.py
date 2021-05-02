import json
import discord
import os
import platform
import sys
import sysconfig
import psutil
import cpuinfo

# https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python

from discord.ext import commands

class System(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def systeminfo(self, ctx):
		"""Displays the systems information"""

		res = f"[OS Type][{sys.platform}]"
		info = cpuinfo.get_cpu_info()
		res += f"\n[CPU][{psutil.cpu_count(logical=False)} Cores / {psutil.cpu_count()} Threads {info['brand']}]"
		res += f"\n[CPU Usage][%{str(psutil.cpu_percent())}]"
		vmem = psutil.virtual_memory()
		res += f"\n[Memory][Total Memory: {int(vmem[0]/2**30)}GB Used: {int(vmem[0]/2**30)-int(vmem[1]/2**30)}GB(%{vmem[2]}) Available: {int(vmem[1]/2**30)}GB]"
		if str(sys.platform) == 'linux': # Check Windows
			smem = psutil.swap_memory()
			res += f"\n[Swap Memory][Total Swap Memory: {int(smem[0]/2**30)}GB Used: {int(smem[2]/2**30)}GB(%{smem[3]}) Available: {int(smem[2]/2**30)}GB]"
		
		res += f"\n[Python Version][{sysconfig.get_python_version()}]"

		INFO = f"**{self.bot.user.name}**'s System Hardware:\n```md\n{res}\n```"
		
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		embed = discord.Embed(
			description = INFO,
			colour = col
		)
		await ctx.send(embed=embed)
		
def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(System(bot, settings))