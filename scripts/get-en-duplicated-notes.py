# This script compares an on-going release notes file with published release notes files.
# If the ongoing release notes file has a duplicate note with the published one, the script reports the note and replaces it with the published one.

import re, os
from tempfile import mkstemp
from shutil import move
from os import remove

ext_path = r'/Users/grcai/Documents/GitHub/qiancai/docs/releases'  # 已发布英文 release notes 文件夹
main_path = r'/Users/grcai/Documents/GitHub/qiancai/docs/releases/release-7.1.2.md'  # 当前正在准备的 release notes 文档路径

# Get the issue info of the existing release notes
def store_exst_rn(ext_path,main_path):

    exst_notes = []
    exst_issue_nums = []

    for maindir, subdir, files in os.walk(ext_path):
        for afile in files:
            file_path = (os.path.join(maindir, afile))
            if file_path.endswith('.md') and file_path != main_path: # Exclude duplicate notes that are in the current release file
                with open(file_path,'r', encoding='utf-8') as fp:
                    level1 = level2 = level3 = ""
                    for line in fp:
                        exst_issue_num = re.search(r'https://github.com/(pingcap|tikv)/[\w-]+/(issues|pull)/\d+', line)
                        authors = re.findall(r'@\[([^\]]+)\]', line) # Get the list of authors in this line
                        if exst_issue_num:
                            if exst_issue_num.group() not in exst_issue_nums:
                                note_level = level1 + level2 + level3
                                note_pair = [exst_issue_num.group(),line.strip(),afile, note_level, authors]
                                exst_issue_nums.append(exst_issue_num.group())
                                exst_notes.append(note_pair)
                            else:
                                continue
                        elif line.startswith("##"):
                            level1 = "> " + line.replace("##","").strip()
                            level2 = level3 = ""
                        elif (line.startswith ("+") or line.startswith ("-")) and (not authors):
                            level2 = "> " + line.replace("+","").replace("-","").strip()
                            level3 = ""
                        elif (line.startswith ("    +") or line.startswith ("    -")) and (not authors):
                            level3 = "> " + line.replace("    +","").replace("    -","").strip()
                        else:
                            continue
            else:
                pass

    if len(exst_issue_nums) != 0:
        return exst_notes
    else:
        return 0

def replace_zh_dup_with_en_dup(note_pairs, main_path):
    DupNum = 0
    NoteNum = 0
    target_file_path = mkstemp()[1]
    source_file_path = main_path
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            LineNum = 0
            for line in source_file:
                LineNum += 1
                original_release_file = re.search('release-\d+\.\d+\.\d+\.md', line)
                issue_num = re.search('https://github.com/(pingcap|tikv)/\w+/(issues|pull)/\d+', line)
                if issue_num and original_release_file:
                     NoteNum +=1
                     for note_pair in note_pairs:
                        if issue_num.group() == note_pair[0] and "(dup)" in line and original_release_file.group() == note_pair[2]:
                            print('A duplicated note is found in line ' + str(LineNum) + " from " + note_pair[2] + note_pair[1])
                            dup_note = '- (dup): {} {} {}'.format(note_pair[2], note_pair[3], note_pair[1]).strip()
                            newline = re.sub(r'- \(dup\): release-\d+\.\d+\.\d+\.md.*?\n',dup_note,line)
                            print('The duplicated note is replaced with ' + newline)
                            DupNum += 1
                        else:
                            continue
                        break
                target_file.write(newline)

    remove(source_file_path)
    move(target_file_path, source_file_path)
    DupRate = "%.0f%%" % (DupNum/NoteNum*100) #计算 release notes 重复率
    print (str(DupNum) + " duplicated notes are found in " + str(NoteNum) + " notes. The duplicated rate is " + str(DupRate) + ".")


if __name__ == "__main__":

    note_pairs = store_exst_rn(ext_path,main_path)
    replace_zh_dup_with_en_dup(note_pairs, main_path)
