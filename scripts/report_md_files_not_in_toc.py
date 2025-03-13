# This script reports the .md files that are not in the TOC files of TiDB and TiDB Cloud documentation.
# It excludes the files in the doc-templates, resource, .github, .vaunt, and .git folders.
# It also excludes the files in the exclude_files list.

import re, os

doc_location = r'/Users/grcai/Documents/GitHub/docs' # Specify the location of your doc source files
exclude_folders = ["doc-templates", "resource", ".github", ".vaunt", ".git"]
exclude_files = ["_docHome.md", "CONTRIBUTING.md", "README.md", "TOC.md", "_index.md", "TOC-tidb-cloud.md"]


def get_toc_files(toc_path):
    files = []
    with open(toc_path, 'r', encoding='utf-8') as fp:
        for line in fp:
            match = re.search(r'[-a-z0-9.]+\.md', line)
            if match:
                files.append(match.group())
    return files

def get_file_not_in_toc(ext_path, toc_files):
    for maindir, subdir, files in os.walk(ext_path):
        for afile in files:
            filepath = os.path.join(maindir, afile)
            if afile.endswith('.md') and not any(folder in maindir for folder in exclude_folders) and afile not in exclude_files:
                if afile not in toc_files:
                    ref_path = filepath.replace(doc_location, "")
                    print(ref_path)

if __name__ == '__main__':

    toc_name = r'TOC.md'
    cloud_toc_name = r'TOC-tidb-cloud.md'
    tidb_toc_path = os.path.join(doc_location, toc_name)
    cloud_toc_path = os.path.join(doc_location, cloud_toc_name)

    toc_files = get_toc_files(tidb_toc_path)

    if os.path.exists(cloud_toc_path):
        cloud_toc_files = get_toc_files(cloud_toc_path)
        toc_files.extend(cloud_toc_files)

    print ("\nFiles not in TOC:")
    get_file_not_in_toc(doc_location, toc_files)
