#!/usr/bin/env python3
# #
# @copyright Copyright (C) 2022 SpyroSoft Solutions S.A. All rights reserved.
# #

import os
import sys
from argparse import ArgumentParser

text_to_search = ["tbd", "todo", "TODO", "fixme"]
file_extensions = (".py", ".md", ".txt", ".sh", "Dockerfile")


def option_parser_init():
    parser = ArgumentParser(
        epilog="The scripts checks if copyright info in files is correct."
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        action="append",
        dest="exclude",
        help="Exclude directory",
    )

    parser.add_argument(
        "-C",
        "--workdir",
        action="append",
        nargs="+",
        dest="workdirs",
        required=True,
        help="Root repository directory",
    )
    return parser.parse_known_args()


def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, "r", encoding="utf-8") as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((file_name, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results


def process(path, exclude_dir):
    todo_count = 0
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            fname = os.path.join(root, f)
            if exclude_dir:
                if fname.find(exclude_dir[0]) != -1:
                    continue
            if fname.endswith(file_extensions):
                result = search_multiple_strings_in_file(fname, text_to_search)

                for res in result:
                    print(res)
                    todo_count += 1
    return todo_count


def main():
    (args, unknown_args) = option_parser_init()

    todo_count = 0
    for workdir in args.workdirs:
        todo_count += process(workdir[0], args.exclude)

    if todo_count > 0:
        sys.exit(f"There are still {todo_count} TODO to handle")
    else:
        print("There are no TODOs left to do.")


if __name__ == "__main__":
    main()
