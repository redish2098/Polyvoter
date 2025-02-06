import enum
import json
import os.path

import nextcord

settings_file = "settings.json"

class Setting:
    def __init__(self, name : str, description : str, default : any, value_type : type):
        self.name = name
        self.description = description
        self.default = default
        self.value_type = value_type

    @staticmethod
    def get_settings():
        if not os.path.isfile(settings_file):
            with open(settings_file, "w") as f:
                f.write("{}")
        settings = json.load(open(settings_file, "r"))
        return settings

    @staticmethod
    def save_settings(value : dict[str, any]):
        assert type(value) is dict
        with open(settings_file, "w") as f:
            f.write(json.dumps(value))


    def get(self):
        settings = self.get_settings()
        if self.name not in settings:
            return self.default
        else:
            return settings[self.name]

    def set(self,  value : any):
        settings = self.get_settings()
        settings[self.name] = value
        self.save_settings(settings)




settings : list[Setting] = [
    Setting("channel", "set the channel for voting","", nextcord.TextChannel),
    Setting("voting", "enable users to vote on submissions",False, bool),
    Setting("submitting", "enable users to submit to the channel",False, bool),
    Setting("enabled", "turn the bot on or off",False, bool)
]