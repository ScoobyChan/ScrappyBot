import time
import typing
import discord
from discord.ext import commands
import re
import shutil
import time
import os
from unittest import result
import requests
from bs4 import BeautifulSoup

# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html?highlight=bot%20owner

class Github(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		self.User = 'ScoobyChan'
		self.Repo = 'ScrappyBot'

		self.URL = 'https://github.com/{}/{}/commits/main'.format(self.User, self.Repo)

	def github_commit_total(self, URL):	
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")

		x = re.findall('/{}/{}/commit/.+[a-z0-9].>.+[a-z0-9].<'.format(self.User, self.Repo), str(soup))
		x.pop()

		if len(x) < 1: return print('No commits found')

		total_commits = []
		total_urls = []

		for y in x:
			url = 'https://github.com{}'.format(y.split('"')[0])
			commit = y.split('"')[0].split('/')[len(y.split('"')[0].split('/')) - 1]
			total_commits.append(commit)
			total_urls.append(url)

		return (total_commits, total_urls)

	def github_commit_latest(self, URL):	
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")

		x = re.findall('/{}/{}/commit/.+[a-z0-9].>.+[a-z0-9].<'.format(self.User, self.Repo), str(soup))
		x.pop()

		if len(x) < 1: return print('No commits found')
		
		url = 'https://github.com{}'.format(x[0].split('"')[0])
		commit = x[0].split('"')[0].split('/')[len(x[0].split('"')[0].split('/')) - 1]
		return (commit, url)

	def get_commit_information(self, URL):
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")

		_files_changed_total_count = 0
		_lines_added = 0
		_lines_removed = 0

		x = re.findall('>.+[0-9].changed files', str(soup))
		if len(x) > 0: _files_changed_total_count = x[0].split('>')[1]
		
		x = re.findall('>.+[0-9].additions', str(soup))
		if len(x) > 0: _lines_added = x[0].split('>')[1]

		x = re.findall('>.+[0-9].deletions', str(soup))
		if len(x) > 0: _lines_removed = x[0].split('>')[1]

		
		x = re.findall('hidden...>.+[a-z0-9].<', str(soup))
		_files = []
		if len(x) > 0:
			for v in x:
				if not re.match('You.signed.*another.tab.or.window', v.split('>')[1].split('<')[0]): 
					_files.append(v.split('>')[1].split('<')[0])
		
		return (_files, _files_changed_total_count, _lines_added, _lines_removed)

	async def update_git(self, url):
		dry = False
		_require_reboot = False

		num = 1

		total_commits, total_urls = self.github_commit_total(url)
		for x in total_urls:
			if '0ab38042193e808be4ab2201e8e8c03ea58b61e2' in x:
				break
			else:
				num += 1

		_files = []

		for x in total_urls[num:]:
			_files_to_get, _fctc, _la, _ld = self.get_commit_information(x)
			for f in _files_to_get:
				if not f in _files:
					_files.append(f)

		if 'Bot.py' in _files or 'Perms.py' in _files or 'Cogloader.py' in _files:
			print('reboot required')
			_require_reboot = True
		
		# os.system('git clone {}'.format(url))

		t = str(int(time.time()))

		if not os.path.exists('temp-{}'.format(t)) and not dry: os.mkdir('temp-{}'.format(t))
		for x in _files:
			if dry:
				print(x)
				if len(x.split('/')) > 1:
					print(x.split('/')[0])
				print(self.Repo+'/'+x)
			
			else:
				try:
					shutil.move(x, t)
				except:
					pass
				
				try:
					shutil.move(self.Repo+'/'+x, x)
				except:
					pass
				
				try:
					shutil.rmtree(self.Repo)
				except:
					pass

		cg_load = self.bot.get_cog('Cogloader')
		if _require_reboot:
			print('reboot') # To work on
			bc = self.bot.get_cog('BotControl')
			if bc: await bc.reboot(self.ctx)

		await cg_load.reload(self.ctx)
	
	@commands.command()
	@commands.is_owner()
	async def update(self, ctx):
		"""
		Joined user
		"""
		self.ctx = ctx
		msg = await ctx.send('Updating from Github')
		
		_commit = self.settings.BotConfig('gitcommit')
		commit, url = self.github_commit_latest(self.URL)
		_files, _fctc, _la, _ld = self.get_commit_information(url)
		
		if commit == _commit: 
			return await ctx.send('Bot already up to date')
		
		self.settings.BotConfig('gitcommit', commit)

		await self.update_git(url)
		
		await msg.edit(content='Updated\n{}'.format(_files))

	@commands.command()
	async def check_update(self, ctx):
		"""
		Joined user
		"""

		_commit = self.settings.BotConfig('gitcommit')

		commit, url = self.github_commit_latest(self.URL)
		
		await ctx.send('Latest commit is {}, current commit is {}'.format(commit, _commit))


def setup(bot):
	settings = bot.get_cog("Settings")
	bot.add_cog(Github(bot, settings))