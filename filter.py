#!/usr/bin/env python3
import math
import sys
import re
import collections

ignore_these = []
remove_this = [
    r'^(\[.*?\] ?)*',  # Apache prepend
    r', referer: http:\S+$',  # Apache append
    r'in \S+\.php on line \d+$', # PHP
]

def preprocess_conf_line(line):
    # Simplistic for now
    # Possible improvements: escaping, regex
    line = line.strip().partition('#')[0]
    return line

def read_conf(conf_file_name):
    with open(conf_file_name) as conf:
        for line in conf:
            processed_line = preprocess_conf_line(line)
            if len(processed_line) > 0:
                ignore_these.append(processed_line)

def remove_metadata(line):
    """
    Remove metadata added by outside programs (such as Apache and PHP).
    """
    for pattern in remove_this:
        line = re.sub(pattern, '', line)
    return line

def debug_print():
    # This was naively factored out, requires some modification to actually work
    try:
        print('bare line:   "%s"' % bare_line)
        print('ignore this: "%s"' % ignore_these[0])
        for i in range(0, len(bare_line)):
            if bare_line[i] != ignore_these[0][i]:
                print(i)
                break
    except IndexError:
        print("String too long at %d" % i, file=sys.stderr)

def filtered_lines(infile):
    for line in infile:
        bare_line = remove_metadata(line).strip()

        if bare_line not in ignore_these:
            yield bare_line

def main():
    try:
        read_conf('ignore.conf')
    except FileNotFoundError:
        print('ignore.conf not found. Outputting all log lines', file=sys.stderr)

    unique_lines = collections.defaultdict(int)
    with open(sys.argv[1]) as infile:
        for line in filtered_lines(infile):
            unique_lines[line] += 1

    highest_frequency = max(unique_lines.values())
    chars_needed = math.ceil(math.log10(highest_frequency))

    sorted_lines = sorted(unique_lines.items())

    for line, count in sorted_lines:
        print(("%"+ str(chars_needed) +"d occurrences:") % count, line)

if __name__ == '__main__':
    main()
