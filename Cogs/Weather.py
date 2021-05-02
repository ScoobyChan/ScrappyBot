import requests
import urllib.request
import json
import time
import discord
from discord.ext import commands
from geopy.geocoders import Nominatim


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Weather(bot, settings))

class Weather(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.geoloc = Nominatim(user_agent="ScrappyBot")

	def c_to_k(self, c):
		return int(c + 273.15)

	def c_to_f(self, c):
		return int((c * 9/5) + 32)

	def f_to_k(self, c):
		return int((c - 32) * 5/9 + 273.15)

	def f_to_c(self, c):
		return int((c - 32) * 5/9)

	def k_to_c(self, c):
		return int(c - 273.15)

	def k_to_f(self, c):
		return int((c - 273.15) * 9/5 + 32)

	@commands.command()
	async def weather(self, ctx, *, location):
		location = self.geoloc.geocode(location)
		# print(location)

		f = requests.get("http://api.openweathermap.org/data/2.5/forecast?appid={}&lat={}&lon={}".format(self.bot.OWM, location.latitude, location.longitude))
		t = f.json()
		# print(t.get('cod', None))

		# Used for testing
		# with open('Json/NY.json') as t:
		# 	t = json.load(t)

		# If Key is denied
		if t.get('cod', None) == 401:
			# Message Bot owner
			print(t.get('message', 'Invalid Key'))
			return await ctx.send(json.get('message', 'Invalid Key'))
		
	
		City = t.get('city', {})
		List = t.get('list', {})[0]
		Temp = List.get('main',{})
		Weather = List.get('weather',{})[0]
		Wind = List.get('wind',{})

		Temps = {}
		Temps['temp'] = 'Temperature {}°C({}°F)'.format(self.k_to_c(Temp['temp']), self.k_to_f(Temp['temp']))
		Temps['temp_min'] = '{}°C({}°F)'.format(self.k_to_c(Temp['temp_min']), self.k_to_f(Temp['temp_min']))
		Temps['temp_max'] = '{}°C({}°F)'.format(self.k_to_c(Temp['temp_max']), self.k_to_f(Temp['temp_min']))
		Temps['feels_like'] = 'Temperature {}°C({}°F)'.format(self.k_to_c(Temp['feels_like']), self.k_to_f(Temp['feels_like']))

		# print(Temps)

		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		Sunset = time.gmtime(int(City.get('sunset', 0)))
		Sunrise = time.gmtime(int(City.get('sunrise', 0)))

		embed=discord.Embed(title="{}/{}".format(City.get('name', None), City.get('country', None)), description="longitude {}/latitude {}".format(City.get('coord', {}).get('lon', None), City.get('coord', {}).get('lat', None)), color=col)
		embed.add_field(name="Temp", value='{}'.format(Temps.get('temp', None)), inline=True)
		embed.add_field(name="Min/Max Temp", value='Min {}/Max {}'.format(Temps.get('temp_min', None), Temps.get('temp_max', None)), inline=True)
		embed.add_field(name=Weather.get('main', None), value=Weather.get('description', None), inline=True)
		embed.add_field(name="Country Population", value=City.get('population', None), inline=True)
		embed.add_field(name="Sun rise (UTC)", value='{}:{}:{}'.format(Sunrise[3], Sunrise[4], Sunrise[5]), inline=True)
		embed.add_field(name="Sun set (UTC)", value='{}:{}:{}'.format(Sunset[3], Sunset[4], Sunset[5]), inline=True)
		embed.add_field(name="Feels like Temp", value='{}'.format(Temps.get('feels_like', None)), inline=True)
		embed.add_field(name="Pressure(Millibars) at Sea level/Ground level", value='{}mb/{}mb'.format(Temp.get('sea_level', None), Temp.get('grnd_level', None)), inline=True)
		embed.add_field(name="Humidity", value='{}%'.format(Temp.get('humidity', None)), inline=True)
		embed.set_footer(text="Time for weather: {}".format(List.get('dt_txt', None)))
		await ctx.send(embed=embed)

	@commands.command()
	async def convtemp(self, ctx, f, t, *, number):
		"""[from][to][number"""
		kfc = ['k', 'f', 'c', 'kelvin', 'fahrenheit', 'celsius']
		if f.lower() in kfc:
			return ctx.send("have not specified a **from** unit(k/f/c or kelvin/fahrenheit/celsius")

		if t.lower() in kfc:
			return ctx.send("have not specified **to** unit(k/f/c or kelvin/fahrenheit/celsius")

		if f.lower() == ('f' or 'fahrenheit'):
			if t.lower() == ('k' or 'kelvin'):
				res = self.f_to_k(number)
			if t.lower() == ('c' or 'celsius'):
				res = self.f_to_c(number)

		if f.lower() == ('k' or 'kelvin'):
			if t.lower() == ('f' or 'fahrenheit'):
				res = self.k_to_f(number)
			if t.lower() == ('c' or 'celsius'):
				res = self.k_to_c(number)

		if f.lower() == ('c' or 'celsius'):
			if t.lower() == ('f' or 'fahrenheit'):
				res = self.c_to_f(number)
			if t.lower() == ('k' or 'kelvin'):
				res = self.c_to_k(number)

		await ctx.send("{}°{} to °{} is: {}".format(number, f, t, res))