#!/usr/bin/env python3

import sys

import sarif_utils


def main():
    results = []

    for filename in sys.argv[1:]:
        with open(filename, "r") as f:
            for line_number, line in enumerate(f):
                column_number = line.find("Hello world!")
                if column_number != -1:
                    results.append(
                        sarif_utils.to_result(
                            path=filename,
                            line_number=line_number + 1,
                            column_number=column_number + 1,
                            rule_id="missing_comma",
                            message="Hello world! should have a comma",
                            length=len("Hello world!"),
                            replacement="Hello, world!",
                            replacement_message="Add a comma",
                        )
                    )

    sarif_utils.print_sarif_log(results=results, tool_name="hello_world_linter")


if __name__ == "__main__":
    main()
