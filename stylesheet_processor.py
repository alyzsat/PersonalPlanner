# Created this script to automatically replace
# different parts of the theme easily
#
# This is where the theme colors are changed


class StyleSheetProcessor:
    def __init__(self):
        self.color_palette = {
            "background1": "#2e2e2e",   # black
            "background2": "#3d3d3d",   # dark gray
            "accent1": "#ffa600",       # yellow
            "accent2": "#fa8561",       # coral
            "accent3": "#E4572E",       # orange
            "text1": "#ffffff"
        }

    def run(self):
        raw_ss = open("assets/raw-stylesheet.qss", "r")
        ss = open("assets/stylesheet.qss", "w")

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