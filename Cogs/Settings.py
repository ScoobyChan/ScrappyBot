import json
import random
import asyncio
import os
import shutil
import requests

import discord
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter

import datetime
import re
import time

from Utils import Configuration, Utils

def setup(bot):
	bot.add_cog(Settings(bot))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
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
		_set = l.get(setting, 'not_found')
		if _set == 'not_found':
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

	def MuteConfig(self, guild, user, setting=None, passback=False):
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('MutedUsers', {}).get(str(user), None)
		if not _user:
			l['MutedUsers'][str(user)] = self.Conf.Mute
			self.Conf.SaveConfigServer(guild, l)
			return l.get('MutedUsers', {}).get(str(user), None)

		if passback == 'del':
			l['MutedUsers'].pop(str(user))
			self.Conf.SaveConfigServer(guild, l)
			return

		_set = l.get('MutedUsers', {}).get(str(user), {}).get(setting, 'not_found')
		if _set == 'not_found':
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set

		l['MutedUsers'][str(user)][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def TempConfig(self, guild, user, role, setting=None, passback=False):
		
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('TempRoleUsers', {}).get(f"{user}-{role}", None)
		if not _user:
			l['TempRoleUsers'][f"{user}-{role}"] = self.Conf.TempRole
			self.Conf.SaveConfigServer(guild, l)
			return l.get('TempRoleUsers', {}).get(f"{user}-{role}", {}).get(setting, None)

		_set = l.get('TempRoleUsers', {}).get(f"{user}-{role}", {}).get(setting, 'not_found')
		if _set == 'not_found' and not passback:
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if passback == 'del':
			print('Removing temprole')
			l['TempRoleUsers'].pop(f"{user}-{role}", None)
			self.Conf.SaveConfigServer(guild, l)
			return

		if not passback:
			return _set

		l['TempRoleUsers'][f"{user}-{role}"][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def BanConfig(self, guild, user, setting, passback=False):
		l = self.Conf.LoadConfigServer(guild)
		_user = l.get('TempBan', {}).get(str(user), None)
		if not _user:
			l['TempBan'][str(user)] = self.Conf.bans
			self.Conf.SaveConfigServer(guild, l)
			return l.get('TempBan', {}).get(str(user), None)

		_set = l.get('TempBan', {}).get(str(user), {}).get(setting, 'not_found')
		if _set == 'not_found':
			raise commands.DisabledCommand(f'Can not find {setting}')
			return False

		if not passback:
			return _set

		l['TempBan'][str(user)][setting] = passback
		self.Conf.SaveConfigServer(guild, l)

	def UserConfig(self, guild, user, setting, passback=None):
		l = self.Conf.LoadConfigUser(guild, user)
		_set = l.get(setting, 'not_found')
		
		if _set == 'not_found':
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
			
	def time_convert(self, _time):
		yr = wk = hrs = mins = secs = year = week = days = 0
		_time_ = ""
		
		if not isinstance(_time, int):
			_list = re.split('\s', _time)
        
			for x in _list:
				if re.search('y|year|yr|yrs|years', x, flags=re.IGNORECASE):
					days += int(re.sub('[years]', "",  x)) * 52 * 7
					# print(day)

				if re.search('w|wk|wks|week|weeks', x, flags=re.IGNORECASE):
					wk += int(re.sub('[weeks]', "",  x))

				if re.search('day|d|days', x, flags=re.IGNORECASE):
					days += int(re.sub('[days]', "",  x))
    
				if re.search('h|hr|hrs|hour|hours', x, flags=re.IGNORECASE):
					hrs += int(re.sub('[hours]', "",  x))
    
				if re.search('m|min|minutes|minute', x, flags=re.IGNORECASE):
					mins += int(re.sub('[minutes]', "",  x))
    
				if re.search('s|sec|secs|second|seconds', x, flags=re.IGNORECASE):
					secs += int(re.sub('[seconds]', "",  x))
    
			# print(yr, wk, days, hrs, mins, secs)
		
		else:
			secs = _time


		secs = int(secs)

		_time = datetime.timedelta(days=days, seconds=secs, minutes=mins, hours=hrs, weeks=wk)
		_secs = int(_time.total_seconds())

		if re.search('.*days.*', str(_time)): 
        
			days = int(re.split(" days, ", str(_time))[0])
    
			year = int(days/365)
			week = int((days%365)/7)
			days = int((days%365)%7)

			_time_ = re.split(" days, ", str(_time))

			# print(_time_[1])
		
		# print(_time)

		end_format = "{}{}{}{}".format("{} Years ".format(year) if year != 0 else "", "{} Weeks ".format(week) if week != 0 else "", "{} Days ".format(days) if days != 0 else "", _time if isinstance(_time_, str) else _time_[1])
		return(end_format, _secs)

	def randomColor(self):
		return random.choice(self.bot.color)

	def KcsConfig(self, guild, ID: str = None, passback=False):
		
		l = self.Conf.LoadConfigServer(guild)

		if not ID:
			return l.get('kcs', {})

		_user = l.get('kcs', {}).get(ID, None)
		if not _user:
			l['kcs'][ID] = self.Conf.Kcs
			l['kcs'][ID]['Name'] = passback
			self.Conf.SaveConfigServer(guild, l)
			return l.get('kcs', {}).get(ID, {})

		_set = l.get('kcs', {}).get(ID, 'not_found')
		if _set == 'not_found' and not passback:
			raise commands.DisabledCommand(f'Can not find {passback}')
			return False

		if passback == 'del':
			print('Removing temprole')
			l['kcs'].pop(ID, None)
			self.Conf.SaveConfigServer(guild, l)
			return

		l['kcs'][ID]["Name"] = passback
		self.Conf.SaveConfigServer(guild, l)

