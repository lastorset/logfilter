#!/bin/python3
import sys
import re

ignore_these = []
remove_this = [
    r'^(\[.*?\] ?)*',  # Apache prepend
    r', referer: http:\S+$',  # Apache append
    r'in \S+\.php on line \d+$', # PHP
]

def preprocess_line(line):
    # Simplistic for now
    # Possible improvements: escaping, regex
    line = line.strip().partition('#')[0]
    return line


def remove_metadata(line):
    """
    Remove metadata prepended by Apache and appended by PHP.
    """
    for pattern in remove_this:
        line = re.sub(pattern, '', line)
    return line

def read_conf(conf_file_name):
    with open(conf_file_name) as conf:
        for line in conf:
            processed_line = preprocess_line(line)
            if len(processed_line) > 0:
                ignore_these.append(processed_line)

def debug_print():
    try:
        print('bare line:   "%s"' % bare_line)
        print('ignore this: "%s"' % ignore_these[0])
        for i in range(0, len(bare_line)):
            if bare_line[i] != ignore_these[0][i]:
                print(i)
                break
    except IndexError:
        print("String too long at %d" % i, file=sys.stderr)

def filter_and_print(infile):
    for line in infile:
        bare_line = remove_metadata(line).strip()

        if bare_line not in ignore_these:
            print(bare_line)

def main():
    try:
        read_conf('ignore.conf')
    except FileNotFoundError:
        print('ignore.conf not found. Outputting all log lines', file=sys.stderr)

    with open(sys.argv[1]) as infile:
        filter_and_print(infile)

if __name__ == '__main__':
    main()
