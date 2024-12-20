import json
import os
import discord
from discord.ext import commands

# mongodb

def setup(bot) -> None:
	bot.add_cog(Json_interact(bot))

class Json_interact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = self.bot.settings

    def check_json(self):
        if not os.path.exists('settings_dict.json'): 
            with open('settings_dict.json', "w") as file:
                json.dump(self.settings, file)

        try:
            with open('settings_dict.json', 'r') as file:
                saved_settings = json.load(file) 
        except Exception as e:
            with open('settings_dict.json', 'r') as file:
                if file.read() == "":
                    with open('settings_dict.json', "w") as file:
                        json.dump(self.settings, file)

            with open('settings_dict.json', 'r') as file:
                saved_settings = json.load(file) 

        if len(saved_settings) == 0:
            with open('settings_dict.json', "w") as file:
                file.write(json.dumps(self.settings))

        if len(saved_settings) != len(self.settings):
            new_settings = {}
            for x in self.settings:
                if x in saved_settings:
                    new_settings[x] = saved_settings[x]
                else:
                    new_settings[x] = self.settings[x]
            
            with open('settings_dict.json', "w") as file:
                json.dump(self.settings, file)
            

    def interact_json(self, data_select, data_input=None, data_read="r"):
        # data_select: item to load
        # data_input: new data to save
        # data_read: Read = r | Write = w

        #Read: interact_json(bot_owners)
        #Write: interact_json("bot_owners", data_input=[123,1234], data_read="w")

        self.check_json()
        with open('settings_dict.json', 'r') as file:
            loaded_settings = json.load(file)

        if data_read == "r":
            return loaded_settings.get(data_select, self.settings[data_select])
        
        if data_read == "w":
            loaded_settings[data_select] = data_input

            with open('settings_dict.json', "w") as file:
                json.dump(loaded_settings, file)

            # data updated