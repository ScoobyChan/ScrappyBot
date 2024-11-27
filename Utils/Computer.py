import random
import discord
from discord.ext import commands 

class computer():
	def text(self, ctx, List, member=None):
		m = random.choice(List)
		if member:
			m = m.replace('{}', member)

		return m