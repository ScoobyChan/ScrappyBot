import discord
import time

class Bot_Configuration():
    def __init__(self):
        pass
       
    def preloads():
        preloads = ["Cogloader", "Database_interact"]
        return preloads
        
    def settings():
        settings = {
                "bot_owners": [],
                "bot_admins": [],
                "guild_owner":{},
                "guild_admins":{},
                "guild_prefix":{},
                "guild_honk_channel":{},
                "guild_nou_channel":{},
                "guild_honk_enable":{},
                "guild_nou_enable":{},
                "guild_lenny":{},
                "blacklisted_guilds":[],
                "ErrorChannel":0
        }
        return settings
    
    def res():
        res = time.localtime()
        return res
    
    def color():
        color = [
                discord.Color.teal(), 
                discord.Color.dark_teal(), 
                discord.Color.green(),
                discord.Color.dark_green(),
                discord.Color.blue(),
                discord.Color.dark_blue(),
                discord.Color.purple(),
                discord.Color.dark_purple(),
                discord.Color.magenta(),
                discord.Color.dark_magenta(),
                discord.Color.gold(),
                discord.Color.dark_gold(),
                discord.Color.orange(),
                discord.Color.dark_orange(),
                discord.Color.red(),
                discord.Color.dark_red(),
                discord.Color.lighter_grey(),
                discord.Color.dark_grey(),
                discord.Color.light_grey(),
                discord.Color.darker_grey(),
                discord.Color.blurple(),
                discord.Color.greyple()
        ]
        return color