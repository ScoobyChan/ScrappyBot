import json
import os

settings = {
    "bot_owners": [],
    "bot_admins": [],
    "guild_owner":{},
    "guild_admins":{},
    "blacklisted_guilds":[]
}

print(1)
if not os.path.exists('settings_dict.json'): 
	file = open('settings_dict.json', "w")
	file.write(json.loads(settings))
	file.close()

print(2)

# Compare dictionaries
file = open('settings_dict.json', 'r')
saved_settings = json.dumps(file.read()) 
current_settings = json.dumps(settings)


if len(current_settings) != len(saved_settings):
    print(3)
    print(saved_settings)