#!/usr/bin/env python

import shlex, sys

"""A command line looks like the following:
[<name>=<value>, [, <name>=<value>...] <binary> [<arg> [, <arg>...]

There's a subtlety that things looking like -o someObject.o should NOT
be separated into individual arguments.
"""

def pretty(line, is_sorted=False):
    binary = ''
    single_arg = ''
    arguments = []
    envs = []

    for arg in shlex.split(line):
        if not binary:
            if '=' in arg:
                envs.append(arg)
            else:
                binary = arg

        elif single_arg:
            if arg.startswith('-'):
                arguments.append(single_arg)
                arguments.append(arg)
            else:
                arguments.append(single_arg + ' ' + arg)
            single_arg = ''

        elif arg.startswith('-') and not arg.startswith('--'):
            single_arg = arg

        else:
            arguments.append(arg)

    single_arg and arguments.append(single_arg)

    if is_sorted:
        envs.sort()
        arguments.sort()

    assert binary, 'No binary found in line "' + line + '"'

    command = ' \\\n'.join(envs + [binary])
    return ' \\\n  '.join([command] + arguments)

if __name__ == '__main__':
    print(pretty(' '.join(sys.argv[1:]), 'sort' in sys.argv[0]))
