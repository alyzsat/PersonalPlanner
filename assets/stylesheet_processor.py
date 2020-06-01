# Created this script to automatically replace
# different parts of the theme easily
#
# This is where the theme colors are changed

color_palette = {
    "background1": "#2e2e2e",   # black
    "background2": "#4d4d4d",   # dark gray
    "accent1": "#ffa600",       # yellow
    "accent2": "#fa8561",       # coral
    "accent3": "#E4572E"        # orange
}


# This assumes that there is only one key on each line
def replace(string: str, k: str, v: str) -> str:
    """Replaces the key word with the corresponding value"""
    split_line = string.split("@"+k)
    return v.join(split_line)


raw_ss = open("raw-stylesheet.qss", "r")
ss = open("stylesheet.qss", "w")
items = list(color_palette.items())  # For consistent order
last_key = items[-1][0]

for line in raw_ss.readlines():
    for key, val in items:
        if key in line:
            ss.write(replace(line, key, val))
            break
        elif key == last_key:
            ss.write(line)

raw_ss.close()
ss.close()

print("Done")
