import json
import time
import random
import asyncio
import os
import shutil

import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter

from Utils import Configuration, Utils

def setup(bot):
	bot.add_cog(Settings(bot))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.jsonfile = 'Json/Setting.json'
		self.Conf = Configuration.Configuration(bot)
		self.Utils = Utils.Utils()
		self.test = 'test'

	def Search(self, to_search, data):
		num = len(to_search)
		numlen = 0
		backup = []
		while True:
			_data = []
			for d in data:
				# print(d)
				if d.startswith(to_search[:numlen]):
					_data.append(d)

			# print(_data)
			if len(_data) == 0:
				break
			elif len(_data) < 4:
				backup = _data
				break
			elif len(to_search) == numlen:
				break
			else:
				numlen += 1
				backup = _data

		return (backup)

	def PhoneBook(self, number=None, server=None):
		l = self.Conf.LoadPhoneBook()
		if not number:
			return l

		if number and not server:
			n = l.get(number, None)
			if not n:
				return None
			else:
				# print('return n')
				return (n)

		if number and server:
			exist = l.get(number, None)	
			if not exist:
				# check if server exists
				for n in l:
					if l[n] == server:
						return (n, l[n])

				l[number] = server
				self.Conf.SavePhoneBook(l)
				return True
			else:
				return False
	
	def BotConfig(self, setting, passback=None):
		l = self.Conf.LoadConfigBot()
		_set = l.get(setting, None)
		if _set == None:
			raise commands.DisabledCommand(f'Can not find {setting}')

		if not passback:
			return _set

		l[setting] = passback

		self.Conf.SaveConfigBot(l)
	
	def ServerConfig(self, guild, setting, passback=None):
		l = self.Conf.LoadConfigServer(guild)
		try:
			_set = l[setting]
		except KeyError:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		except TypeError:
			return

		if not passback:
			return _set


		l[setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def MuteConfig(self, guild, user, setting, passback=False):
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('MutedUsers', {}).get(str(user), None)
		if not _user:
			l['MutedUsers'][str(user)] = self.Conf.Mute
			self.Conf.SaveConfigServer(guild, l)
			return l.get('MutedUsers', {}).get(str(user), None)

		_set = l.get('MutedUsers', {}).get(str(user), {}).get(setting, None)
		if _set == None:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set

		l['MutedUsers'][str(user)][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def TempConfig(self, guild, user, setting, passback=False):
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('TempRoleUsers', {}).get(str(user), None)
		if not _user:
			l['TempRoleUsers'][str(user)] = self.Conf.TempRole
			self.Conf.SaveConfigServer(guild, l)
			return l.get('TempRoleUsers', {}).get(str(user), None)

		_set = l.get('TempRoleUsers', {}).get(str(user), {}).get(setting, None)
		if _set == None:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set

		l['TempRoleUsers'][str(user)][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def BanConfig(self, guild, user, setting, passback=False):
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('TempBan', {}).get(str(user), None)
		if not _user:
			l['TempBan'][str(user)] = self.Conf.bans
			self.Conf.SaveConfigServer(guild, l)
			return l.get('TempBan', {}).get(str(user), None)

		_set = l.get('TempBan', {}).get(str(user), {}).get(setting, None)
		if _set == None:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set

		l['TempBan'][str(user)][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def UserConfig(self, guild, user, setting, passback=None):
		l = self.Conf.LoadConfigUser(guild, user)
		_set = l.get(setting, None)
		
		if _set == None:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set


		l[setting] = passback
		self.Conf.SaveConfigUser(guild, user, l)

	def server_owner(ctx):
		return ctx.message.author.id == ctx.guild.owner_id

	def Get(self, ctx=None, Type=None, Name=None):
		if Type.lower() == 'g':
			Name = str(Name).strip('<>#@!&')
			for g in self.bot.guilds:
				try:
					if g.id  == int(Name):
						return g
				except:
					continue
			
		if Type.lower() == 'channel':
			try:
				Name = str(Name).strip('<>#@!&')
				return discord.utils.get(self.bot.get_all_channels(), id=int(Name))
			except ValueError:
				return discord.utils.get(self.bot.get_all_channels(), name=Name)

		if Type.lower() == 'user':
			for m in ctx.guild.members:
				if m == Name:
					return m
			try:
				Name = str(Name).strip('<>#@!&')
				for m in ctx.guild.members:
					if m.id == int(Name):
						return m
			except ValueError:
				pass

			for m in ctx.guild.members:
				if Name == m.nick:
					return m

			# try:
			# 	return discord.utils.get(self.bot.get_all_members(), id=int(Name))
			# except ValueError:
			# 	return discord.utils.get(self.bot.get_all_members(), name=Name)


		if Type.lower() == 'role':
			try:
				Name = str(Name).strip('<>#@!&')
				return discord.utils.get(ctx.guild.roles, id=int(Name))
			except ValueError:
				return discord.utils.get(ctx.guild.roles, name=Name)

	# Clean Up
	def Time(self, _time):
		try:
			t = int(_time)
		except:
			_time = _time.split()
			t = 0
			for d in _time:
				if d[:1].lower() == 'd':
					try:
						t += (int(d[1:]) * 24 * 60 * 60)
						break
					except ValueError:
						pass

			for d in _time:
				if d[:1].lower() == 'h':
					try:
						t += (int(d[1:]) * 60 * 60)
						break
					except ValueError:
						pass

			for d in _time:
				if d[:1].lower() == 'm':
					try:
						t += (int(d[1:]) * 60)
						break
					except ValueError:
						pass

			for d in _time:
				if d[:1].lower() == 's':
					try:
						t += int(d[1:])
						break
					except ValueError:
						pass

		total = t
		days = 0
		while True:
			if t < 0:
				t += (24 * 60 * 60)
				days -= 1
				break
			else:
				t -= (24 * 60 * 60)
				days += 1

		hours = 0
		while True:
			if t < 0:
				t += (60 * 60)
				hours -= 1
				break
			else:
				t -= (60 * 60)
				hours += 1

		mins = 0
		while True:
			if t < 0:
				t += (60)
				mins -= 1
				break
			else:
				t -= (60)
				mins += 1

		seconds = t

		__time = "" if not days == 0 else 'Days {}, '.format(days), "" if not hours == 0 else 'Hours {}, '.format(hours), "" if not mins == 0 else 'Minutes {}, '.format(mins), "" if not seconds == 0 else 'Seconds {}, '.format(seconds)

		return (total, __time)

	def randomColor(self):
		return random.choice(self.bot.color)