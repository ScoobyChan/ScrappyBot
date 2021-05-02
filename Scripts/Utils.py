import os
import urllib.parse
import sys
import requests

class Utils:
	def __init__(self):
		pass

	def clear(self):
		if not 'win' in sys.platform:
			os.system('clear')
		else:
			os.system('cls')

	def title(self, title):
		num =len(title)
		space = num + 8
		print(f'#####{"#"*space}#####')
		print(f"  #####{' '*space}#####")
		print(f"    #####    {title}    #####")
		print(f"  #####{' '*space}#####")
		print(f'#####{"#"*space}#####')

	def shorten(url_long):
		URL = "http://tinyurl.com/api-create.php"	
		try:
			url = URL + "?" \
				+ urllib.parse.urlencode({"url": url_long})
			res = requests.get(url)
			return res.text
		except Exception as e:
			raise


# Utils().title('Hello Everybody')