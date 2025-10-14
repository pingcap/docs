# This script enables you to update the "## Variable reference" section in `system-variable-reference.md` automatically according to the latest reference information of all system variables in TiDB documentation.
# Before running this script, you need to specify the local directory of the TiDB source documentation in the `docs_dir` variable.
# If a system variable name contains `_`, the script will add all references to this variable name to the reference index, except when the variable name is surrounded by `_` or `-` or other English letters in the referenced docs.
# If a system variable name does not contain `_`, the script will only count the link reference of this variable as valid references and add the valid references to the reference index.

import re
from pathlib import Path
import os

docs_dir = "/Users/grcai/Documents/GitHub/docs-cn" # Specify the local directory of the TiDB source documentation, which can be either English or Chinese
reference_section_titles = ["Variable reference", "变量索引"]
referenced_in_text = ["Referenced in:", "引用该变量的文档："]

def get_md_files_in_toc(toc_file):
    with open(toc_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'\[.*?\]\(/(?:[^)]+/)?([^/]+\.md)(?:#[^)]*)?\)', content)

def generate_var_link(variable_line):
    # Remove <span> tags but keep the content inside span
    variable_line = re.sub(r'\s*?<span.*?>(.*?)</span>\s*?', r' \1', variable_line).strip()
    # Remove backticks
    variable_line = re.sub(r'`', '', variable_line).strip()
    variable_line = variable_line.lstrip("#").strip().lower() # Remove leading "#" and trim spaces, convert to lowercase
    variable_line = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", variable_line)  # Remove special symbols but keep spaces
    variable_line = re.sub(r"\s+", "-", variable_line)  # Replace spaces with hyphens
    return variable_line

def extract_variables(content):
    variables = []
    for line in content.split('\n'):
        if line.startswith('### '):
            # Remove <span> tags
            clean_line = re.sub(r'<span.*?</span>', '', line).strip()

            # Extract variable name, match with or without backticks
            var_name = re.sub(r'^### `(.*?)`|^### (.+)', r'\1\2', clean_line).strip()

            if var_name:
                var_link = generate_var_link(line)  # Variable name for generating links
                variables.append((var_name, var_link))
    return variables

def find_references(variable_name, var_link, docs_dir, reference_paths_to_be_checked):
    references = []
    link_to_find = f"(/system-variables.md#{var_link})"

    for path in reference_paths_to_be_checked:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                if link_to_find in content:
                        title = extract_doc_title(content, path)
                        rel_path = str(path.relative_to(docs_dir))
                        references.append((title, rel_path))
                else:
                    if "_" in variable_name and variable_name in content:
                        if re.search(rf'(?<![A-Za-z_-]){re.escape(variable_name)}(?![A-Za-z_-])', content):
                            title = extract_doc_title(content, path)
                            rel_path = str(path.relative_to(docs_dir))
                            references.append((title, rel_path))
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            continue

    return references

def extract_doc_title(content, path):
    # Match level-1 heading that starts with # and has one or more spaces, trim trailing spaces
    match = re.search(r'^#\s+(.*?)\s*$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return Path(path).stem

def sort_references(references):
    non_release_notes = []
    release_notes = []

    # Separate Release Notes from non-Release Notes
    for title, path in references:
        if path.startswith("releases/release-"):
            release_notes.append((title, path))
        else:
            non_release_notes.append((title, path))

    # Sort non-Release Notes by path title alphabetically
    non_release_notes.sort(key=lambda x: x[0])

    # Sort Release Notes by version number in descending order
    def extract_version(path):
        match = re.search(r'release-(\d+\.\d+(?:\.\d+)?)', path)
        if match:
            return tuple(map(int, match.group(1).split('.')))
        return (0, 0, 0)  # Default version number as lowest

    release_notes.sort(key=lambda x: extract_version(x[1]), reverse=True)

    # Merge sorted results
    return non_release_notes + release_notes

def generate_reference_content(variables, docs_dir):
    content = [f"## {reference_section_title}\n\n"]
    unreferenced_variables = []  # Store unreferenced variables
    reference_paths_to_be_checked = []
    # Get reference_paths_to_be_checked list
    for path in Path(docs_dir).rglob('*.md'):
        if path.name in doc_md_list and path.name != reference_file and path.name != variables_file:
            reference_paths_to_be_checked.append(path)

    for var_name, var_link in sorted(variables):
        refs = find_references(var_name, var_link, docs_dir, reference_paths_to_be_checked)
        if not refs:
            # Record variables that are not referenced by other documents
            unreferenced_variables.append(var_name)
        else:
            pass

        refs.append((variables_file_title, f"system-variables.md#{var_link}"))
        sorted_refs = sort_references(refs) # Sort reference links

        content.append(f"### {var_name}\n\n")
        content.append(f"{referenced_in}\n\n")
        for title, path in sorted_refs:
            content.append(f"- [{title}](/{path})\n")
        content.append("\n")

    # Print unreferenced variables to console for reference
    if unreferenced_variables:
        print("\nUnreferenced Variables:")
        print(f"There are {len(unreferenced_variables)} variables that are not referenced in any documents other than system-variables.md:")
        for var in sorted(unreferenced_variables):
            print(f"{var}")
        print()

    return ''.join(content)

def update_reference_file_path(ref_file_path, new_content):
    try:
        with open(ref_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Warning: {ref_file_path} not found. Creating a new file.")
        content = ""

    start_pos = content.find(f'## {reference_section_title}')
    if start_pos == -1:
        print(f"Warning: '{reference_section_title}' section not found. Adding new section.")
        updated_content = content + "\n" + new_content
    else:
        next_section_pos = content.find('\n## ', start_pos + 1)
        if next_section_pos == -1:
            next_section_pos = len(content)
        updated_content = content[:start_pos] + new_content + content[next_section_pos:]

    updated_content = re.sub(
        rf'\[([^\]]+)\]\(/tidb-cloud/([^)]+)\.md\)',
        rf'[\1]({cloud_docs_dir}/\2)',
        updated_content
    )

    # Remove <span> tags
    updated_content = re.sub(r'\[([^]]*?\s*?<span.*?</span>\s*?[^]]*)\]\(([^)]*)\)', lambda m: f'[{re.sub(r"\s*?<span.*?</span>\s*?", "", m.group(1))}]({m.group(2)})', updated_content)

    updated_content = re.sub(r"What's New in TiDB 5.0", "TiDB 5.0 Release Notes", updated_content)

    # Replace the last two empty lines with one empty line
    updated_content = re.sub(r"\n\n$", "\n", updated_content)

    with open(ref_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def main():
    global doc_md_list

    if doc_language == "en":
        doc_md_list = list(set(get_md_files_in_toc(tidb_file) + get_md_files_in_toc(tidb_cloud_file)))
    else:
        doc_md_list = list(set(get_md_files_in_toc(tidb_file)))

    print("Start to generate reference information for system variables. It will take a few seconds...")

    try:
        # Read system variables
        with open(variables_file_path, 'r', encoding='utf-8') as f:
            variables = extract_variables(f.read())
        # Generate new reference content
        new_content = generate_reference_content(variables, docs_dir)
        # Update reference file
        update_reference_file_path(reference_file_path, new_content)
        print("Reference file updated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    variables_file = "system-variables.md"
    reference_file = "system-variable-reference.md"
    tidb_toc_file = "TOC.md"
    tidb_cloud_toc_file = "TOC-tidb-cloud.md"
    cloud_docs_dir = "https://docs.pingcap.com/tidbcloud"
    variables_file_path = os.path.abspath(os.path.join(docs_dir, variables_file))
    reference_file_path = os.path.abspath(os.path.join(docs_dir, reference_file))
    tidb_file = os.path.abspath(os.path.join(docs_dir, tidb_toc_file))
    tidb_cloud_file = os.path.abspath(os.path.join(docs_dir, tidb_cloud_toc_file))

    with open(variables_file_path, 'r', encoding='utf-8') as f:
        variables_file_title = extract_doc_title(f.read(), variables_file_path)

    if not re.search(r'[\u4e00-\u9fff]', variables_file_title): # Check if title contains no Chinese characters
        doc_language = "en"
        referenced_in = referenced_in_text[0]
        reference_section_title = reference_section_titles[0]
    else:
        doc_language = "zh"
        referenced_in = referenced_in_text[1]
        reference_section_title = reference_section_titles[1]

    main()
