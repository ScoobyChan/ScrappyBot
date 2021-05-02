import requests
import sys
import traceback
import urllib
import discord
from discord.ext import commands 

class Tinyurl:
	def __init__(self):
		self.URL = "http://tinyurl.com/api-create.php"	

	def shorten(self, url_long):
		try:
			url = self.URL + "?" \
				+ urllib.parse.urlencode({"url": url_long})
			res = requests.get(url)
			return res.text
		except Exception as e:
			raise