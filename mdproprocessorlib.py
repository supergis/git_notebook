#!/usr/bin/env python

"""One file markdown preprocessor"""
from __future__ import print_function
import re
import shlex

__version__ = "0.0.2"


# PPREPROCESSOR
#--------------
class Preprocessor(object):
    """Looks for matching strings and replaces them in the markdown file"""

    def __init__(self, mdfile, commandset=None):
        """mdfile: markdown file handle
        commandset: modify this to include only a subset of commands
        """
        self.data = mdfile.read()
        self.cmds = commandset if commandset is not None else CMDSET

    def iterppitems(self):
        """Iterates over all preprocessor ((start, stop), statement) tuples."""
        for match in re.finditer("<!--@(.*?)@-->", self.data, flags=re.DOTALL):
            yield match.span(), match.group(1)

    def process(self, remove_unkown=False):
        """processes the file and converts commands that it understands"""
        data = self.data
        reversed_output = []
        for (low, high), cmd in sorted(self.iterppitems(), reverse=True):
            ppcmd = shlex.split(cmd)
            cname, cargs = ppcmd[0] if ppcmd else None, ppcmd[1:]
            try:
                substitute = self.cmds[cname](*cargs)
            except KeyError:
                idx = low if not remove_unkown else high
                reversed_output.append(data[idx:])
            else:
                reversed_output.append(data[high:])
                reversed_output.append(substitute)
            data = data[:low]
        reversed_output.append(data)
        return "".join(reversed(reversed_output))


# PARSING FUNCTIONS
#-------------------
def includecode(language, filename):
    """includes a file"""
    with open(filename, 'r') as incf:
        data = incf.read()
    return ("~~~ {.%s}\n%s~~~\n") % (language, data)


def includecodesnippet(language, filename, snippet):
    """includes a part of a file sourrounded by
    # <name>
    ...
    # </name>
    """
    tagpattern = ('"""<%(tag)s>"""(.*?)"""</%(tag)s>"""'
                  '|#\s*<%(tag)s>(.*?)#\s*</%(tag)s>') % {'tag': snippet}
    try:
        with open(filename, 'r') as codefile:
            data = codefile.read()
    except IOError:
        output = "\n# File: '%s' not found.\n" % filename
    else:
        match = re.search(tagpattern, data, flags=re.DOTALL)
        if match is None:
            output = ("\n# File '%s':"
                      " Snippet '%s' not found.\n") % (filename, snippet)
        else:
            output = match.group(1) or match.group(2)
    return ("~~~ {.%s}%s~~~\n") % (language, output)


def optionalfigure(filename, caption):
    """includes a figure with caption"""
    return "![%s](%s)\n" % (caption, filename)

def optionaltext(text):
    """includes text"""
    return text

# PARSING DICT
#--------------
CMDSET = {'.INCLUDECODE': includecode,
          '.INCLUDECODESNIPPET': includecodesnippet,
          '.OPTIONALFIGURE': optionalfigure,
          '.OPTIONALTEXT': optionaltext}


if __name__ == "__main__":

    import argparse
    import inspect

    parser = argparse.ArgumentParser()
    parser.add_argument("mdfile", type=argparse.FileType('r'), nargs="?")
    parser.add_argument('--list', action='store_true', help="list commands")
    parser.add_argument('--version', action='store_true', help="print version")
    parser.add_argument('--without', type=str, action="append", default=[],
                                     help="don't parse command")
    parser.add_argument('--clean', action='store_true',
                                   help="remove unparsed tags")
    args = parser.parse_args()

    if args.version:
        print("mdpp-%s" % __version__)
    elif args.list:
        for cn, fun in CMDSET.items():
            print("<!--@", cn, " ".join(inspect.getargspec(fun).args), "@-->")
            print('   ', fun.__doc__)
    elif args.mdfile:
        for remove in args.without:
            CMDSET.pop(remove, None)
        print(Preprocessor(args.mdfile, commandset=CMDSET).process(args.clean))
    else:
        parser.print_help()
