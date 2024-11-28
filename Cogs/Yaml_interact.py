import yaml
import os
import discord

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Yaml_interact(bot))

class Yaml_interact():
    def __init__(self, bot):
		self.bot = bot
        self.settings = self.bot.settings
    
    def check_yaml(self):
        if not os.path.exists('settings_dict.yaml'): 
            with open('settings_dict.yaml', 'w') as file:
                outputs = yaml.dump(self.settings, file)

        with open('settings_dict.yaml', 'r') as file:
            try:
                saved_settings = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)

        if len(saved_settings) == 0:
            with open('settings_dict.yaml', 'w') as file:
                outputs = yaml.dump(self.settings, file)
            

        if len(saved_settings) != len(self.settings):
            new_settings = {}
            for x in settings:
                if x in saved_settings:
                    new_settings[x] = saved_settings[x]
                else:
                    new_settings[x] = self.settings[x]

            with open('settings_dict.yaml', 'w') as file:
                outputs = yaml.dump(new_settings, file)

    def interact_yaml(self, data_select, data_input=None, data_read="r"):
        # data_select: item to load
        # data_input: new data to save
        # data_read: Read = r | Write = w

        #Read: interact_yaml(bot_owners)
        #Write: interact_yaml("bot_owners", data_input=[123,1234], data_read="w")

        self.check_yaml()
        with open('settings_dict.yaml', 'r') as file:
            try:
                loaded_settings = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        
        if data_read == "r":
            return loaded_settings.get(data_select, None)
        
        if data_read == "w":
            loaded_settings[data_select] = data_input

            with open('settings_dict.yaml', 'w') as file:
                outputs = yaml.dump(loaded_settings, file)