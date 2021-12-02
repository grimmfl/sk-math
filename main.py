import sys
from string import digits
from typing import Dict
from compiler.executer import Executer
from compiler.top_down_parser import TopDownParser

VALID_INPUTS = digits + "*/+-^. "


def show_help():
    print("-f <FILEPATH> | Execute file")
    print("-h            | Help")


def config() -> Dict:
    switch = {
        "-f": None,
        "-h": show_help
    }
    for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("-"):
            if switch[sys.argv[i]] is None:
                switch[sys.argv[i]] = sys.argv[i + 1]
            else:
                switch[sys.argv[i]]()
    return switch


def file_to_text(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def run(text: str, parser: TopDownParser, executer: Executer):
    parsed = parser.parse(text)
    executer.execute(parsed)


if __name__ == "__main__":
    p = TopDownParser()
    e = Executer()
    if len(sys.argv) > 1:
        c: Dict = config()
        code = ""
        if c["-f"] is not None:
            if not(c["-f"].endswith(".skm")):
                raise Exception("File needs to have .skm ending.")
            code = file_to_text(c["-f"])
    else:
        p = TopDownParser()
        code = "var x, y, z\n" \
               "x = 4\n" \
               "y = 8\n" \
               "z = x * y + 8\n" \
               "out z"
        #editor = Editor()
        #code: str = ""
        #line_number = 1
        #while True:
        #    code += input(f"{line_number}  ") + "\n"
        #    line_number += 1

    run(code, p, e)
