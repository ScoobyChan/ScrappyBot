
import asyncio
import os
import json
import urllib.request
import requests
import discord
import aiohttp
import random
from discord.ext import commands

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Health(bot, settings))

class Health(commands.Cog):
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self._Country = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Diamond Princess', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'MS Zaandam', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan*', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'West Bank and Gaza', 'Yemen', 'Zambia', 'Zimbabwe', 'US', 'Global']

	@commands.command()
	async def covid(self, ctx, Country=None):
		"""[Coountry]
		Produces info on covid for a country or as a whole"""
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.settings.randomColor()

		if not Country in self.Country or not Country:
			for ms in self._Country:
				desc += '\n - '+ms
				
			embed=discord.Embed(title="Covid Country list", description=desc, color=col)
			return await ctx.send(embed=embed)

		with urllib.request.urlopen('https://covid-api.mmediagroup.fr/v1/cases?country={}'.format(Country)) as url:
			data = json.loads(url.read().decode())
			data = data['all']
			
			embed=discord.Embed(title="Covid Stats", color=col)
			embed.add_field(name="Isolation", value=data['iso'], inline=True)
			embed.add_field(name="Confirmed Cases", value=data['confirmed'], inline=True)
			embed.add_field(name="Recovered Cases", value=data['recovered'], inline=True)
			embed.add_field(name="Number of Deaths", value=data['deaths'], inline=True)
			embed.add_field(name="Country", value="{}({})".format(data['country'], data['abbreviation']), inline=True)
			embed.add_field(name="Continent", value=data['continent'], inline=True)
			embed.add_field(name="Capital City", value=data['capital_city'], inline=True)
			embed.add_field(name="Location", value=data['location'], inline=True)
			embed.set_footer(text="Updated: {}".format(data['updated']))
			await ctx.send(embed=embed)