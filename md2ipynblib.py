#!/usr/bin/env python

"""Very simple markdown to IPython notebook converter.
Just run ./md2ipynb test.md test.ipynb
Note: Only toplevel python code is put in a code cell.
      '~~~ {.python}'
       ...
      '~~~'
"""
import json
import re


class NBStructure(dict):

    def __init__(self, name):
        """returns and empty ipynb notebook structure"""
        super(NBStructure, self).__init__()
        self.update((("metadata", {}),
                     ("nbformat", 3),
                     ("nbformat_minor", 0),
                     ("worksheets", [])))
        self["metadata"].update((("name", name),))
        self["worksheets"].append({})
        self["worksheets"][0].update((("cells", []),
                                      ("metadata", {})))

    def addcell(self, cell):
        """Add a cell to the notebook"""
        self["worksheets"][0]["cells"].append(cell)


class NBCodeCell(dict):
    def __init__(self):
        """returns an empty ipynb code cell"""
        super(NBCodeCell, self).__init__()
        self.update((("cell_type", "code"),
                     ("language", "python"),
                     ("collapsed", False),
                     ("prompt_number", 0),
                     ("metadata", {}),
                     ("input", []),
                     ("outputs", [])))

    def load(self, string):
        """load code string into cell"""
        for line in string.split("\n"):
            self["input"].append(line + "\n")
        return self


class NBMarkdownCell(dict):

    def __init__(self):
        """returns an empty ipynb markdown cell"""
        super(NBMarkdownCell, self).__init__()
        self.update((("cell_type", "markdown"),
                     ("metadata", {}),
                     ("source", [])))

    def load(self, string):
        """load markdown string into cell"""
        for line in string.split("\n"):
            self["source"].append(line + "\n")
        return self


class IPyNB(object):

    def __init__(self, mdfile, name):
        """Ipython notebook abstraction"""
        self.base = NBStructure(name)
        data = mdfile.read()
        self.load(data)

    def load(self, string):
        """loads markdown and python from string data"""
        segments = re.split("(~~~ {.python}.*?~~~)", string, flags=re.DOTALL)
        for segment in segments:
            if segment.startswith('~~~ {.python}') and segment.endswith('~~~'):
                newcell = NBCodeCell().load(segment[13:-3].strip())
            else:
                newcell = NBMarkdownCell().load(segment.strip('\n'))
            self.base.addcell(newcell)

    def write(self, outfile):
        """write ipynb file"""
        outfile.write(json.dumps(self.base, indent=1, sort_keys=True))

if __name__ == "__main__":

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="converts markdown to ipynb")
    parser.add_argument("mdfile", type=argparse.FileType('r'), help="md input file")
    parser.add_argument('--out', type=argparse.FileType('w'),
                        help="ipynb output file", default=sys.stdout)
    parser.add_argument('--name', type=str, help="ipynb name")
    args = parser.parse_args()

    name = args.out.name if args.name is None else args.name
    nb = IPyNB(args.mdfile, name)
    nb.write(args.out)
