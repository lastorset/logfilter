#!/bin/python3
import sys
import re

ignore_these = []

def preprocess_line(line):
    # Simplistic for now
    # Possible improvements: escaping, regex
    line = line.strip().partition('#')[0]
    return line


def remove_metadata(line):
    """
    Remove metadata prepended by Apache.
    """
    return re.sub(r'^(\[.*?\] ?)*', '', line)

try:
    with open('ignore.conf') as conf:
        for line in conf:
            processed_line = preprocess_line(line)
            if len(processed_line) > 0:
                ignore_these.append(processed_line)
except FileNotFoundError:
    print('ignore.conf not found. Outputting all log lines', file=sys.stderr)

with open(sys.argv[1]) as infile:
    for line in infile:
        bare_line = remove_metadata(line.strip())
        if bare_line not in ignore_these:
            print(bare_line)
