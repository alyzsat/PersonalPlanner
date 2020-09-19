# Created this script to automatically replace
# different parts of the theme easily
#
# This is where the theme colors are changed
import json


class StyleSheetProcessor:
    def __init__(self, theme_name: str):
        with open(f"personalplanner/assets/themes/{theme_name}.txt", "r") as theme:
            self.color_palette = json.load(theme)

    def run(self):
        raw_ss = open("personalplanner/assets/raw-stylesheet.qss", "r")
        ss = open("personalplanner/assets/stylesheet.qss", "w")

        keys = list(self.color_palette.keys())  # For consistent order
        last_key = keys[-1]

        for line in raw_ss.readlines():
            for key in keys:
                if key in line:
                    ss.write(self.replace(line, key))
                    break
                elif key == last_key:
                    ss.write(line)

        raw_ss.close()
        ss.close()

    # This assumes that there is only one key on each line
    def replace(self, string: str, k: str) -> str:
        """Replaces the key word with the corresponding value"""
        split_line = string.split("@" + k)
        return self.color_palette[k].join(split_line)
