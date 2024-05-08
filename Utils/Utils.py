import os
import json
import requests
import urllib.request
import urllib.parse
import random
import bs4
import discord
import sys

class Utils():
	def title(self, title):
		num =len(title)
		space = num + 8
		print(f'#####{"#"*space}#####')
		print(f"  #####{' '*space}#####")
		print(f"    #####    {title}    #####")
		print(f"  #####{' '*space}#####")
		print(f'#####{"#"*space}#####')
		
	def clear(self):
		if not 'win' in sys.platform:
			os.system('clear')
		else:
			os.system('cls')
			
	def JsonReader(self, location):
		if os.path.exists(location):
			# Check if not a file
			with open(location) as t:
				t = json.load(t)
		else:
			# Not a file must be a website or doesn't exist
			try:
				with urllib.request.urlopen(location) as url:
					t = json.loads(url.read().decode())
			except urllib.error.HTTPError:
				f = requests.get(location)
				t = f.json()

		return t

	def ImgurSearch(self, search):
		try:
			encoded_query = urllib.parse.quote(search)
			url = f'https://imgur.com/search?q={encoded_query}'
			while not url.endswith('#'):
				req = urllib.request.Request(url)
				page = urllib.request.urlopen(req)
				bs = bs4.BeautifulSoup(page,"html.parser")
				# print(page.read().decode())
				return "https:"+str(random.choice(bs.find_all('img')).get('src'))

		except urllib.error.HTTPError as err:
			return err

	def GiphySearch(self, api_key, search):
		API = "http://api.giphy.com/v1/gifs/search?q={}&api_key={}&limit=100&rating=R".format(search, api_key)
		data = self.JsonReader(API)
		if data.get('message', None):
			return data.get('message', None)

		data = data['data']
		data = random.choice(data)
		return data['images']['downsized']['url']
		# return data['url']

	def urlchecker(self, url):
		try:	
			requests.get(url)
			return True
		except requests.exceptions.MissingSchema:
			return False

	def embed(self, embed):
		title = embed.get('title', None)
		url = embed.get('url', None)
		desc = embed.get('desc', None)
		color = embed.get('color', None)
		thumb = embed.get('thumbnail', None)
		footer = embed.get('footer', None)
		field = embed.get('fields', []) # [("Name", "Value"),("Name", "Value"),("Name", "Value")]
		author = embed.get('author', {})  # {"name":name, "link":link, "icon":icon}

		if not color:
			random.choice([
				discord.Color.teal(),
				discord.Color.dark_teal(),
				discord.Color.green(),
				discord.Color.dark_green(),
				discord.Color.blue(),
				discord.Color.dark_blue(),
				discord.Color.purple(),
				discord.Color.dark_purple(),
				discord.Color.magenta(),
				discord.Color.dark_magenta(),
				discord.Color.gold(),
				discord.Color.dark_gold(),
				discord.Color.orange(),
				discord.Color.dark_orange(),
				discord.Color.red(),
				discord.Color.dark_red(),
				discord.Color.lighter_grey(),
				discord.Color.dark_grey(),
				discord.Color.light_grey(),
				discord.Color.darker_grey(),
				discord.Color.blurple(),
				discord.Color.greyple()
			])

		embed=discord.Embed(title=title, url=url, description=desc, color=color)
		
		if len(author) > 0: 
			embed.set_author(name=author.get("name", None), url=author.get("link", None), icon_url=author.get("icon", None))
		
		if thumb: embed.set_thumbnail(url=thumb)
		
		if len(field) > 0:	
			for x in field:
				embed.add_field(name=x[0], value=x[1], inline=True)

		if footer: embed.set_footer(text=footer)

		return embed

	def progressbar(self, percentage):
		perc = percentage*100
		return f'[{"#"*int(int(perc) // 5)}{"-"*(20 - int(int(perc) // 5))}] {str(int(perc))[:4] if not int(str(int(perc))[:3]) == 100 else "100"}%'
		

