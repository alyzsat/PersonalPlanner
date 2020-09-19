import configparser
import math
import logging
from datetime import datetime


class Settings:

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.options = {}
        self.config = configparser.ConfigParser()
        self.load_config_file()

    def current_theme(self) -> str:
        return self.options["theme"]

    def current_term(self) -> (str, int):
        return self.options["currentterm"]

    def show_completed(self) -> bool:
        return self.options["showcompleted"]

    def show_current(self) -> bool:
        return self.options["showcurrent"]

    def show_term_labels(self) -> bool:
        return self.options["showtermlabels"]

    def set_current_theme(self, theme: str):
        self.options["theme"] = theme

    def set_current_term(self, season: str, year: int):
        self.options["currentterm"] = (season, year)

    def set_show_completed(self, enable: bool):
        self.options["showcompleted"] = enable

    def set_show_current(self, enable: bool):
        self.options["showcurrent"] = enable

    def set_show_term_labels(self, enable: bool):
        self.options["showtermlabels"] = enable

    def set(self, options: dict):
        """Set multiple options at once"""
        for key, val in options.items():
            self.options[key] = val

    def reset_to_default(self):
        """Resets all settings to their default state"""
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        date = datetime.now().date()

        self.options = {
            "theme": "default",
            "currentterm": (seasons[math.floor(date.month / 4)], date.year),
            "showcurrent": False,
            "showcompleted": True,
            "showtermlabels": True
        }

    def save(self) -> None:
        """Save settings to config file"""
        for key, val in self.options.items():
            if type(val) is tuple:
                a, b = val
                self.config.set("Settings", key, f"{a}-{b}")
            else:
                self.config.set("Settings", key, str(val))

        with open(self.config_file, "w") as file:
            self.config.write(file)
            logging.info("Saved settings to config file")

    def load_config_file(self):
        """Read the config file and load the settings. If no config file is
        found, create a new config file nad save current settings
        """
        self.config.read(self.config_file)

        # If there is no config file found, create one
        if len(self.config.sections()) == 0:
            self.config.add_section("Settings")
            self.reset_to_default()
            self.save()

        else:
            for key, val in self.config["Settings"].items():
                if val == "True":
                    self.options[key] = True
                elif val == "False":
                    self.options[key] = False
                elif "-" in val:
                    a, b = val.split("-")
                    self.options[key] = (a, int(b))
                else:
                    self.options[key] = val

    def __str__(self):
        string = "Settings ===================\n"
        for key, val in self.options.items():
            string += f"  {key}: {val}\n"
        string += "\n\n"
        return string


