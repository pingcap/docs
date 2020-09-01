# from git import Repo
import git
import re

repo = git.Repo()
# modified_files = len(repo.index.diff(None))
# count_staged_files = len(repo.index.diff("HEAD"))
# print(modified_files, count_staged_files)

# reference: https://stackoverflow.com/questions/35761133/python-how-to-check-for-open-and-close-tags
def stack_tag(tag, stack):
    t = tag[1:-1] # 去掉左右括号
    #print(t)
    if t[0:1] != '/':
        # Add tag to stack
        stack.append(t)
        #print("TRACE open", stack)
    else:
        t = t[1:]
        if len(stack) == 0:
            #print("No blocks are open; tried to close", t)
            self_closed_tag = True # 这一行用来占位，实际上无效
        else:
            if stack[-1] == t:
                # Close the block
                stack.pop()
                #print("TRACE close", t, stack)
            else:
                #print("Tried to close", t, "but most recent open block is", stack[0])
                if t in stack:
                    stack.remove(t)
                    #print("Prior block closed; continuing")

    # if len(stack):
    #     print("Blocks still open at EOF:", stack)
    return stack


for item in repo.index.diff(None):
    # print(item.a_path)
    # filename = item.a_path
    filename = 'storage-engine/rocksdb-overview.md'
    if '.md' in filename:
        file = open(filename, "r" )
        content = file.read()
        result_findall = re.findall(r'<([^`>]*)>', content)
        if len(result_findall) == 0:
            print(filename, "has no tags!")
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
                elif content[pos[0]-1] == '`' and content[pos[1]] == '`':
                    # print(content[int(pos[0])-1:int(pos[1]+1)])
                    continue
                # 其余的 tag 都需要放入堆栈确认是否闭合
                else:
                    # print(tag)
                    stack_tag(tag, stack)

            if len(stack):
                stack = ['<' + i + '>' for i in stack]
                print(filename + ' has unclosed tags: ' + ','.join(stack) + '. Please use backticks `` to wrap them!')

