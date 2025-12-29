from glob import glob
import re


def sort_glob(pattern):

    return sorted(glob(pattern), key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', x)])
