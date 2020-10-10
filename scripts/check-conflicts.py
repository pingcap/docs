import re
import sys
import os

lineNum = 0
flag = 0
pos = []
single = []
f = []

for filename in sys.argv[1:]:
    if os.path.isfile(filename):
        with open(filename,'r') as file:
            for line in file:
                lineNum += 1
                if re.match(r'<{7}.*\n', line):
                    flag = 1
                    single.append(lineNum)
                elif re.match(r'={7}\n', line) :
                    flag = 2
                elif re.match(r'>{7}', line) and flag==2:
                    single.append(lineNum)
                    pos.append(single)
                    single = []
                else:
                    continue
            if len(pos) :
                pos.append(filename)
                f.append(pos)
                pos = []

if len(f):
    for file in f:
        print("There are conflicts in "+ file[3] + ".")
        conflicts = file[0:3]
        for conflict in conflicts:
            print("CONFLICTS: line " + str(conflict[0]) + " to line " + str(conflict[1]))

print("They will cause website build failure.")
exit(1)


