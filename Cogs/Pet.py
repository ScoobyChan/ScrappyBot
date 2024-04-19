# Credits CorpNewt for 
# https://github.com/corpnewt/CorpBot.py/blob/bc5c08e848a766d5c75920352b0a09bc4c04c2b2/Cogs/Actions.py

import random
import discord
from discord.ext import commands
from Utils import Member
from Utils import Computer

class Pet(commands.Cog):
	def __init__(self, bot, settings):
		"""Credits to CorpNewt for Computer and Member"""
		self.settings = settings
		self.bot = bot

	@commands.command()
	async def pet(self, ctx, member=None):
		"""
		[object]
		Pets an object}
		"""
			
		Bot = self.bot.user.id
		M = Member.member()
		C = Computer.computer()
		
		nothingList = [ 'you absentmindedly wave your hand in the air.',
						'you could have sworn there was a cat there!',
						'you remember that there are no cats here.',
						'you try to pet the cat, but miss because the cat is gone.']
		botList = [ 	'I may be electronic but I still appreciate pets.',
						'*purrrrrrrrrrrrrrr*.',
						'you electrocute yourself trying to pet a computer.']
		selfList = [	'you give yourself a nice pat on the head.',
						'too bad there\'s no one else to pet you.',
						'in lieu of anything else to pet, you pet yourself.',
						'your hair is warm and soft.']
		memberList = [  'you give *{}* a pat on the head.',
						'you rub your hand through *{}\'s* hair.',
						'*{}* smiles from your petting.',
						'you try to pet *{}*, but miss because they hid under the bed.',
						'*{}* purrs from your petting.',
						'you pet *{}* but they bite your hand',
						'you try to pet *{}* but they hiss and run away.']
		itemList = [	'you rub *{}* but it doesn\'t feel like a cat.',
						'you don\'t hear any purring from *{}*.',
						'you hurt your hand trying to pet *{}*.']

		if member:
			m = M.displayName(ctx, member)
			if m == None:
				msg = C.text(ctx, itemList, member)
			elif m.id == Bot:
				msg = C.text(ctx, botList, m.name)
			elif m.id == ctx.author.id:
				msg = C.text(ctx, selfList, m.name)
			else:
				msg = C.text(ctx, memberList, m.name)
		else:
			msg = C.text(ctx, nothingList)

		# print(msg)
		await ctx.send(msg)

async def setup(bot: commands.Bot) -> None:
	settings = bot.get_cog("Settings")
	await bot.add_cog(Pet(bot, settings))
