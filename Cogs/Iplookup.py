import discord
from discord.ext import commands
import urllib.parse
import requests
import json


class Iplookup(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def iplookup(self, ctx, *, ip_address:str):
		"""
		[Game to search]
		Searchs for steam games
		"""
		ip_address_full = f"http://ip-api.com/json/{ip_address}"
		response = requests.get(ip_address_full)
		html_content = response.content
		string_data = html_content.decode('utf-8')
		json_data = json.loads(string_data)
		
		details = (f'IP Address Lookup ({ip_address})\n'
			 f' - Status: {json_data.get("status", "")}\n'
			 f' - country: {json_data.get("country", "")}\n'
			 f' - countryCode: {json_data.get("countryCode", "")}\n'
			 f' - Region: {json_data.get("region", "")}\n'
			 f' - Region Name: {json_data.get("regionName", "")}\n'
			 f' - City: {json_data.get("city", "")}\n'
			 f' - Latitude: {json_data.get("lat", "")}\n'
			 f' - Longitude: {json_data.get("lon", "")}\n'
			 f' - Timezone: {json_data.get("timezone", "")}\n'
			 f' - Internet Service Provider (ISP): {json_data.get("isp", "")}\n'
			 f' - Organisation: {json_data.get("org", "")}\n')
		
		await ctx.send(details)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Iplookup(bot, settings))