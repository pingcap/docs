import re
import sys

# reference: https://stackoverflow.com/questions/35761133/python-how-to-check-for-open-and-close-tags
def stack_tag(tag, stack):
    t = tag[1:-1] # 去掉左右括号
    first_space = t.find(' ') # 比如 t = 'span class="label__title"'；t.find(' ') = 4；只需要将属性名传入堆栈
    #print(t)
    # print(t + ' 的第一个空格在 ' + str(first_space))
    if t[-1] == '/':
        self_closed_tag = True # 为自闭合标签。这一行用来占位，实际上无效
    elif t[0:1] != '/': # 为开放标签，将属性名传入堆栈
        # Add tag to stack
        if first_space == -1:
            stack.append(t)
            print("TRACE open", stack)
        else:
            stack.append(t[:first_space])
            print("TRACE open", stack)
    else: # </xxx>类标签
        if first_space != -1:
            t = t[1:first_space]
        else:
            t = t[1:]

        if len(stack) == 0:
            print("No blocks are open; tried to close", t)
            closed_tag = True # 这一行用来占位，实际上无效
        else:
            if stack[-1] == t:
                # Close the block
                stack.pop()
                print("TRACE close", t, stack)
            else:
                print("Tried to close", t, "but most recent open block is", stack[-1])
                if t in stack:
                    stack.remove(t)
                    print("Prior block closed; continuing")

    if len(stack):
        print("Blocks still open at EOF:", stack)
    return stack

def tag_is_wrapped(pos, content):
    # pos = (7429, 7433) # tag 的位置
    # content 为整篇文档字符串
    # 这个函数要找出 tag 附近两边是否有 `` 包裹
    tag_start = pos[0]
    tag_end = pos[1]
    content_previous = content[:tag_start][::-1] # reverse content_previous
    content_later = content[tag_end:]
    if content_previous.find('`') != -1 and content_later.find('`') != -1:
        # print(content_previous.find('`'), content_later.find('`'))
        # print(content_previous)
        # print(content_later)
        return True
    else:
        # print(content_previous.find('`'), content_later.find('`'))
        # print(content_previous)
        # print(content_later)
        return False


# print(sys.argv[1:])
for filename in sys.argv[1:]:
    print("Checking " + filename + "......\n")
    file = open(filename, "r" )
    content = file.read()
    file.close()
    result_findall = re.findall(r'<([^`>]*)>', content)
    if len(result_findall) == 0:
        print("=== REPORT == \n")
        print("The edited markdown file " + filename + " has no tags!\n")
        exit(0)
    else:
        result_finditer = re.finditer(r'<([^`>]*)>', content)
        stack = []
        for i in result_finditer: # i 本身也是可迭代对象，所以下面要使用 i.group()
            # print(i.group())
            # print(i.span())
            tag = i.group()
            pos = i.span() # (7429, 7433)
            # 首先筛去特殊 tag，比如 <!-- xxx -->
            if tag[:4] == '<!--' and tag[-3:] == '-->':
                continue
            # 再筛去带 `` 的 tag
            # elif content[pos[0]-1] == '`' and content[pos[1]] == '`':
            elif tag_is_wrapped(pos, content):
                # print(content[int(pos[0])-1:int(pos[1]+1)])
                print(tag, 'is wrapped by backticks!')
                continue

            # 其余的 tag 都需要放入堆栈确认是否闭合
            stack = stack_tag(tag, stack)

        if len(stack):
            stack = ['<' + i + '>' for i in stack]
            print("=== ERROR REPORT == \n")
            print(filename + ' has unclosed tags: ' + ','.join(stack) + '.\n Please use backticks `` to wrap them or close them!\n')
            exit(1)
        else:
            print("=== REPORT == \n")
            print("The edited markdown file has tags. But all tags are closed, congratulations!\n")
