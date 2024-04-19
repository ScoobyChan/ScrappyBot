import yaml
import json
import os
import time

def DirectoryCheck():
	if os.path.exists('Bot.py'):
		if not os.path.exists('Json/'):
			os.mkdir('Json/')
		if not os.path.exists('Json/Servers'):
			os.mkdir('Json/Servers')

DirectoryCheck()


class Configuration:
	def __init__(self, bot):
		self.bot = bot
		self.bans = {
			'bantime':0,
			'bantimeadded':0,
			'banned':True,
			'Task':None,
			'BanUser':''
		}
		self.Tags = {
			'user':0,
			'data':'',
			'time':'',
			'user':0
		}
		self.Mute = {
			'MuteTime':0, 
			'MuteAdded':0,
			'MuteUser':0,
			'IsMuted':True, 
			'MuteTask':None,
		}

		self.TempRole = {
			'TempRoleTime':0, 
			'TempRoleAdded':0,
			'TempRoleUser':0,
			'TempRoleTask':None,
			'IsTemped':False, 
		}
		
		self.user = {
			'TimeZone':None,
			'XP':0,
			'XPReserve':0,
			'XPRole':0,
			'XPRoles':[],
			'VKCount':0,
			'test':'test'
		}
		
		self.server = {
			'NSFWOverride':False,
			'isLockedDown': True,
			'Lockdown':0,
			'AdminRole':0,
			'Logging':False,
			'LoggingType':[],
			'LogChannel':0,
			'IgnoredUsers':[],
			'DefaultRole':0,
			'DefaultChannel':0,
			'DisabledCommands':[],
			'DisabledCommandsAdminOverride':False,
			'UserRoles':[],
			'quoteChannel':0,
			'quoteEmote':'',
			'MuteRole':0,
			'MutedUsers':{},
			'TempRoleUsers':{},
			'TempRoles':[],
			'XPReserveLimit':-1,
			'XPReserveGain':1,
			'XPRoles':[],
			'XPReserveTime':300,
			'XPReserveAdminOverride':False,
			'XPEnable':False,
			'ReganAmount':100000,
			'XPTask':None,
			'XPType':'time',
			'FeedEnable':False,
			'BotState':'Alive',
			'ReportChannel':0,
			'Rules':'',
			'RulesRole':0,
			'RulesRoleTimeout':0,
			'RulesType':'',
			'RulesEmoji':'',
			'LinksRole':0,
			'ServerOwnerLock':False,
			'ServerAdminLock':False,
			'GoodByeMsg':'[[user]] has left [[server]]',
			'GoodByeChannel':0,
			'WelcomeMsg':'Welcome **[[user]]**([[userID]]) to [[server]]',
			'WelcomeChannel':0,
			'SuppressMention':False,
			'Users':{},
			'DJUsers':[],
			'BannedUsers':[],
			'KickedUsers':[],
			'VoteKickUser':[],
			'VoteKickCount':10,
			'VoteKickedWarningCount':5,
			'VoteKickedWarningMuteTime':60,
			'VoteKickedExpire':120,
			'CommandChannel':0,
			'HonkChannel':0,
			'HonkEnable':False,
			'NouChannel':0,
			'NouEnable':False,
			'LastLenny':0,
			'LastShrug':0,
			'ChannelContent':{},
			'MemStatChannel':0,
			'VcStatChannel':0,
			'Prefix':'$',
			'LocalTz':'utc',
			'TagLock':True,
			'TagRole':0,
			'Tags':{},
			'Music':[],
			'Volume':100,
			'AdminOverRide':False, # Admin includes anyone that has admin perms or server owner overrides disable command
			'TempBan':{}, # user, secs
			'DailyChannel':0,
			'DailyMsg':'',
			'DailyTask':None,
			'DailyTime':0,
			'BlockNumbers': [],
			'PhoneChannel': 0,
			'LockPhoneChannel':False,
			'LangFilter':[],
			'LangFilterUser':{},
			'LangFilterWarning':0,
			'LangFilterKick':0,
			'kcs':{},
			'tableflip': True,
			'Responses':{},
			'Triggers':{},
			'rpchannel': 0,
			'RoleplayProfiles':{},
		}

		self.Kcs = {
				'Name': None 
			}

		self.roleplay = {
				'Name': None,
				'Age': 0,
				'Picture': '', 
				'Description': ''
			}
		
		self.BotSettings = {
			'ratelimit': 10,
			'OwnerLock': False,
			'ErrorChannel':0,
			'SuggestionChannel':0,
			'BugreportsChannel':0,
			'Messages':0,
			'BlacklistedServers':[],
			'reboot': False,
			'gitcommit': 0,
			'PhoneBook': []
		}

		self.PhoneBook = {}

	def LoadConfigBot(self):
		try:	
			if not os.path.exists('Json/Settings.yaml'):
				with open('Json/Settings.yaml', 'w') as f:
					yaml.dump(self.BotSettings, f)
		except FileNotFoundError:
			DirectoryCheck()
			if not os.path.exists('Json/Settings.yaml'):
				with open('Json/Settings.yaml', 'w') as f:
					yaml.dump(self.BotSettings, f)

		with open('Json/Settings.yaml', 'r') as f:
			return yaml.load(f, Loader=yaml.FullLoader)

	def SaveConfigBot(self, data):
		with open('Json/Settings.yaml', 'w') as f:
			yaml.dump(data, f)

	def LoadConfigServer(self, server):
		try:
			if not os.path.exists('Json/Servers/'+str(server)+'.yaml'):
				with open('Json/Servers/'+str(server)+'.yaml', 'w') as f:
					yaml.dump(self.server, f)

		except FileNotFoundError:
			DirectoryCheck()
			if not os.path.exists('Json/Servers/'+str(server)+'.yaml'):
				with open('Json/Servers/'+str(server)+'.yaml', 'w') as f:
					yaml.dump(self.server, f)

		with open('Json/Servers/'+str(server)+'.yaml', 'r') as f:
			_json = yaml.load(f, Loader=yaml.FullLoader)
			# print(_json)
			return _json

	def SaveConfigServer(self, server, data):
		with open('Json/Servers/'+str(server)+'.yaml', 'w') as f:
			yaml.dump(data, f)

	def LoadConfigUser(self, guild, user):
		Server = self.LoadConfigServer(guild)
		User = Server.get('Users', {}).get(str(user), None)
		if not User:
			Server['Users'][str(user)] = self.user
			self.SaveConfigServer(guild, Server)

			User = Server.get('Users', {}).get(str(user), None)

		return User

	def SaveConfigUser(self, guild, user, data):
		Server = self.LoadConfigServer(guild)
		User = Server.get('Users', {}).get(str(user), None)
		if not User:
			Server['Users'][str(user)] = self.user
		else:
			Server['Users'][str(user)] = data
			
		self.SaveConfigServer(guild, Server)

	def UpdateJson(self, server=None):
		if not server:
			# print('Multiple Servers')
			for g in self.bot.guilds:
				self.Sync(g.id)
		else:
			# print('Single Servers')
			self.Sync(int(server))

	def Sync(self, server: int = 0):
		if isinstance(server, int):	# Fix issues with syncing
			for g in self.bot.guilds:
				if g.id == int(server):
					############# Server Config #############
					print('Checking Server: {0}({0.id})'.format(g))
					_Server = self.LoadConfigServer(server)
					
					for ser in self.server:
						if not ser in _Server:
							_Server[ser] = self.server[ser]
							print('Adding: ' + ser)

					while True:
						Comp = True
						try:
							for ser in _Server:
								if not ser in self.server:
									del _Server[ser]
									print('Removing: ' + ser)
						except RuntimeError as e:
							# input(e) # Used for debugging
							Comp = False

						if Comp == True:
							break

					self.SaveConfigServer(server, _Server)

					############# User Config #############
					for m in g.members:
						print('Checking User: {0}({0.id})'.format(m))
						User = self.LoadConfigUser(g.id, m.id)
						# print('Adding new items')
						for ser in self.user:
							try:
								User[ser]
							except KeyError:
								User[ser] = self.user[ser]
								print('Adding: ' + ser)

						self.SaveConfigUser(g.id, m.id, User)

						# print('Removing new items')
						User = self.LoadConfigUser(g.id, m.id)
						while True:	
							Comp = True
							try:
								for ser in User:
									if not ser in self.user:
										del User[ser]
										print('Removing: ' + ser)
							except RuntimeError as e:
								# input(e) # Used for debugging
								Comp = False

							if Comp == True:
								break

						self.SaveConfigUser(g.id, m.id, User)