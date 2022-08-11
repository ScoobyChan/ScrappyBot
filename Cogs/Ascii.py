import asyncio
import os
import discord
#ascii text
from art import *
# Ascii Image
from PIL import Image
import requests
from discord.ext import commands

if not os.path.exists('images/'):
	os.mkdir('images/')

# Add Support to printavi
class Ascii(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command()
	async def asciiFun(self, ctx, msg: str=None):
		"""Ascii fun"""
		if msg == None:
			return await ctx.send('No text given. i.e. coffee')
		
		output=art(msg)
		await ctx.send(output)

	@commands.command()
	async def ascii(self, ctx, msg: str=None):
		"""Ascii pics"""
		if not msg:
			return await ctx.send('No Input Given')

		d = self.server.Get(ctx, 'user', msg)
		if d:
			msg = str(d.avatar_url)

		image = False
		try:
			f = open('images/image.jpg','wb')
			f.write(requests.get(msg).content)
			f.close()
			image = True
		except:
			output=text2art(msg, 'small', chr_ignore=True)

		if image == True:
			# pass the image as command line argument
			img = Image.open('images/image.jpg')

			# resize the image
			width, height = img.size
			aspect_ratio = height/width
			new_width = 57
			new_height = aspect_ratio * new_width * 0.55
			img = img.resize((new_width, int(new_height)))
			# new size of image
			# print(img.size)

			# convert image to greyscale format
			img = img.convert('L')

			pixels = img.getdata()

			# replace each pixel with a character from array
			chars = ["B","S","#","&","@","$","%","*","!",":","."]
			new_pixels = [chars[pixel//25] for pixel in pixels]
			new_pixels = ''.join(new_pixels)

			# split string of chars into multiple strings of length equal to new width and create a list
			new_pixels_count = len(new_pixels)
			ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
			output = "\n".join(ascii_image)

		# await ctx.send('**ASCII TIME**\n```\n'+output+'\n```')
		if ctx.author.top_role.colour:
			col = ctx.author.top_role.colour
		else:
			col =self.server.randomColor()

		embed = discord.Embed(
			description = '**ASCII TIME**\n```\n'+output+'\n```',
			colour = col
		)
		await ctx.send(embed=embed)

def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Ascii(bot, settings))