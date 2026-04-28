# Copyright 2021 PingCAP, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# MIT License

# Copyright (c) 2021 Charlotte Liu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# This file is originally hosted at https://github.com/CharLotteiu/pingcap-docs-checks/blob/main/check-tags.py.

import re
import sys
import os

TAG_PATTERN = re.compile(r'</?[A-Za-z][A-Za-z0-9:-]*(?:\s[^>\n]*)?/?>')

# reference: https://stackoverflow.com/questions/35761133/python-how-to-check-for-open-and-close-tags
def stack_tag(tag, stack):
    t = tag[1:-1]
    first_space = t.find(' ')
    #print(t)
    if t[-1:] == '/':
        pass
    elif t[:1] != '/':
        # Add tag to stack
        if first_space == -1:
            stack.append(t)
            # print("TRACE open", stack)
        else:
            stack.append(t[:first_space])
            # print("TRACE open", stack)
    else:
        if first_space != -1:
            t = t[1:first_space]
        else:
            t = t[1:]

        if len(stack) != 0 and stack[-1] == t:
            # Close the block
            stack.pop()
            # print("TRACE close", t, stack)

    # if len(stack):
    #     print("Blocks still open at EOF:", stack)
    return stack

def filter_frontmatter(content):
    # if there is frontmatter, remove it
    return re.sub(r'\A---\n.*?\n---\n', '', content, count=1, flags=re.DOTALL)

def filter_html_comments(content):
    return re.sub(r'<!--[\s\S]*?-->', '', content)

def filter_backticks(content, filename):
    # Remove fenced code blocks and inline code spans before checking tags.
    # Markdown supports code spans wrapped by one or more backticks.
    content = filter_fenced_code_blocks(content, filename)
    return filter_inline_code_spans(content)

def filter_fenced_code_blocks(content, filename):
    fence_pattern = re.compile(r'(?m)^[ \t]*(?P<fence>`{3,}|~{3,})[^\n]*\n?')
    result = []
    pos = 0

    while True:
        opener = fence_pattern.search(content, pos)
        if opener is None:
            result.append(content[pos:])
            break

        result.append(content[pos:opener.start()])
        fence_char = opener.group('fence')[0]
        closing_pattern = re.compile(
            r'(?m)^[ \t]*' + re.escape(fence_char) + r'{3,}[ \t]*$'
        )
        closer = closing_pattern.search(content, opener.end())
        if closer is None:
            print(filename, ": Some of your code blocks ``` ``` are not closed. Please close them.")
            exit(1)

        code_block = content[opener.start():closer.end()]
        result.append('\n' * code_block.count('\n'))
        pos = closer.end()

    return ''.join(result)

def filter_inline_code_spans(content):
    result = []
    pos = 0
    opener_pattern = re.compile(r'`+')

    while True:
        opener = opener_pattern.search(content, pos)
        if opener is None:
            result.append(content[pos:])
            break

        result.append(content[pos:opener.start()])
        ticks = opener.group()
        closer_pattern = re.compile(r'(?<!`)' + re.escape(ticks) + r'(?!`)')
        closer = closer_pattern.search(content, opener.end())
        if closer is None:
            # Keep unmatched backticks as normal text so this script only checks tags.
            result.append(content[opener.start():opener.end()])
            pos = opener.end()
            continue

        code_span = content[opener.start():closer.end()]
        result.append('\n' * code_span.count('\n'))
        pos = closer.end()

    return ''.join(result)

status_code = 0

# print(sys.argv[1:])
for filename in sys.argv[1:]:
    # print("Checking " + filename + "......\n")
    if os.path.isfile(filename):
        file = open(filename, "r", encoding='utf-8')
        content = file.read()
        file.close()

        content = filter_frontmatter(content)
        content = filter_backticks(content, filename)
        content = filter_html_comments(content)
        # print(content)
        if TAG_PATTERN.search(content) is None:
            # print("The edited markdown file " + filename + " has no tags!\n")
            continue
        else:
            result_finditer = TAG_PATTERN.finditer(content)
            stack = []
            for i in result_finditer:
                # print(i.group(), i.span())
                tag = i.group()
                pos = i.span()

                if tag[:4] == '<!--' and tag[-3:] == '-->':
                    continue
                elif content[pos[0]-2:pos[0]] == '{{' and content[pos[1]:pos[1]+2] == '}}':
                    # print(tag) # filter copyable shortcodes
                    continue
                elif tag[:5] == '<http': # or tag[:4] == '<ftp'
                    # filter urls
                    continue

                stack = stack_tag(tag, stack)

            if len(stack):
                stack = ['<' + i + '>' for i in stack]
                print("ERROR: " + filename + ' has unclosed tags: ' + ', '.join(stack) + '.\n')
                status_code = 1

if status_code:
    print("HINT: Unclosed tags will cause website build failure. Please fix the reported unclosed tags. You can use backticks `` to wrap them or close them. Thanks.")
    exit(1)
