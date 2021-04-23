import sys
import argparse

from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import ANSI
from simplify import minifiers
import os


def c_show(args):
    with open(args.file) as file:
        data = file.read()
    if '.' in args.file:  # If the filename has an extension
        lexer = get_lexer_for_filename(args.file)
    else:
        lexer = guess_lexer(data)
    print(ANSI(highlight(data, lexer, get_formatter_by_name('terminal16m'))))


def _minify(file, format, overwrite, output, prefix=""):
    try:
        if format is None:
            minifier = minifiers.get_minifier(file)
        else:
            minifier = minifiers.get_minifier(f"example.{format}")
    except Exception:
        print(f"Invalid extension for '{file}'")
        return
    try:
        with open(file) as fp:
            data = fp.read()
    except Exception:
        print(f"Skipping binary file '{file}'")
    len_before = len(data)
    data = minifier(data)
    len_after = len(data)
    output_file = file if overwrite else output
    try:
        percentage_of_reduction = round(100 - (len_after/len_before)*100, 2)
    except ZeroDivisionError:
        percentage_of_reduction = 0.0
    with open(output_file, "w") as fp:
        fp.write(data)
    print(f"{prefix}Applied {minifier.__name__.replace('_', ' ')} to '{file}' reduced by {percentage_of_reduction}%")


def c_minify(args):
    if args.recursive:
        print("Walking Directory Structure")
        all_files = []
        for root, _, files in os.walk(args.file):
            all_files.extend([os.path.join(root, x) for x in files])
        len_files = len(all_files)
        for x, counter in zip(all_files, range(len_files)):
            prefix = f"{counter+1}/{len_files}: "
            _minify(x, args.format, True, None, prefix)
    else:
        _minify(args.file, args.format, args.overwrite, args.output)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Simplify your developer needs with this tool for Python")
    commands = parser.add_subparsers(dest="command_")

    minify = commands.add_parser("minify", help="minify various types of file or a complete folder containing files")
    minify.add_argument("file", help="Input File/Folder")
    minify_output_group = minify.add_mutually_exclusive_group()
    minify_output_group.add_argument("output", nargs="?", help="Output File")
    minify_output_group.add_argument("-o", "--overwrite", action="store_true", help="Overwrite the input file")
    minify_output_group.add_argument("-r", "--recursive", action="store_true", help="Overwrite files but in recursive "
                                                                                    "manner in a folder")
    minify.add_argument(
        "-f", "--format",
        required=False,
        default=None,
        choices=[
            "json",
            "py",
            "js",
            "xml",
            "html",
            "css"],
        help="Override the format"
    )

    show = commands.add_parser("show", help="show a file highlighted")
    show.add_argument("file", help="file to show")

    args = parser.parse_args(args)

    if args.command_ == "show":
        c_show(args)
    elif args.command_ == "minify":
        c_minify(args)


if __name__ == '__main__':
    main()
