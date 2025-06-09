#!/bin/python3
import sys
from difflib import unified_diff

print("Checking alphabetic sorting of glossary.md")

with open("glossary.md") as fh:
    # Extract the lines that start with ### into itemsA (unsorted)
    itemsA = ""
    for line in fh.readlines():
        if line.startswith("###"):
            itemsA += line
    fh.seek(0)

    # Extract the lines that start with ### into itemsB (sorted)
    itemsB = ""
    for line in sorted(fh.readlines(), key=str.casefold):
        if line.startswith("###"):
            itemsB += line

    if itemsA == itemsB:
        print("result: OK")
        sys.exit(0)

    print("result: differences found, see diff for details")
    # diff itemsA and itemsB
    diff = unified_diff(
        itemsA.splitlines(keepends=True),
        itemsB.splitlines(keepends=True),
        fromfile="before",
        tofile="after",
    )
    sys.stdout.writelines(diff)
    sys.exit(1)
