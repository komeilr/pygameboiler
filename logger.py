import logging

l = logging.Logger("debug")
h = logging.StreamHandler()
f = logging.Formatter(fmt="[{filename}:{lineno}] {msg}", style="{")

h.setFormatter(f)
l.addHandler(h)
