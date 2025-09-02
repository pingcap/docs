import re
import os
import sys
import json
from urllib.request import urlopen, Request
from google import genai

repo_owner = "qiancai"
repo_name = "docs"
en_branch = "release-8.5"
zh_branch = "i18n-zh-release-8.5"
toc_file_names = ["TOC-tidb-cloud-starter.md", "TOC-tidb-cloud-essential.md", "TOC-tidb-cloud.md"]

# ========== AI Configuration ==========
model_name = "gemini-2.0-flash"
genai_token = os.getenv("GEMINI_API_TOKEN")
if not genai_token:
    print("Error: GEMINI_API_TOKEN environment variable must be set")
    sys.exit(1)

client = genai.Client(api_key=genai_token)

def read_file_from_repo(file_path):
    """Read a file from the current repository"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def write_file_to_repo(file_path, content):
    """Write content to a file in the current repository"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False

def extract_commit_from_target_file(target_file):
    """Extract the EN commit SHA from the target TOC file comment"""
    try:
        content = read_file_from_repo(target_file)
        if not content:
            return None
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if i > 10:  # Only check first 10 lines
                break
            
            # Look for the pattern: <!--EN commit: COMMIT_SHA-->
            if "EN commit:" in line:
                # Extract commit SHA using regex
                match = re.search(r'EN commit:\s*([a-f0-9]{40})', line)
                if match:
                    commit_sha = match.group(1)
                    print(f"Found earlier EN commit in target file: {commit_sha}")
                    return commit_sha
        
        print("[ERROR] No EN commit comment found in target file")
        return None
        
    except Exception as e:
        print(f"Error reading target file for commit extraction: {e}")
        return None

def get_latest_commit_sha(repo_owner, repo_name, branch, toc_file_name):
    """Get the latest commit SHA for a specific file on GitHub"""
    try:
        # Use GitHub API to get commits for the specific file
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        params = f"?sha={branch}&path={toc_file_name}&per_page=1"
        full_url = url + params
        headers = {
            "User-Agent": "tidb-docs-sync/1.0",
            "Accept": "application/vnd.github.v3+json",
        }
        gh_token = os.getenv("GITHUB_TOKEN")
        if gh_token:
            headers["Authorization"] = f"Bearer {gh_token}"
        req = Request(full_url, headers=headers)
        
        with urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
        if data and len(data) > 0:
            latest_commit = data[0]['sha']
            
            print(f"Latest commit: {latest_commit}")
            
            return latest_commit
        else:
            print("No commits found for the specified file")
            return None
            
    except Exception as e:
        print(f"Error fetching latest commit: {e}")
        return None

def get_github_compare_diff(base_commit, head_commit):
    """Fetch unified diff from GitHub compare endpoint (.diff) for the repo {repo_owner}/{repo_name}"""
    try:
        url = f"https://github.com/{repo_owner}/{repo_name}/compare/{base_commit}...{head_commit}.diff"
        print(f"Fetching compare diff from: {url}")
        headers = {
            "User-Agent": "tidb-docs-sync/1.0",
            "Accept": "application/vnd.github.v3.diff",
        }
        gh_token = os.getenv("GITHUB_TOKEN")
        if gh_token:
            headers["Authorization"] = f"Bearer {gh_token}"
        req = Request(url, headers=headers)
        with urlopen(req, timeout=20) as resp:
            content_bytes = resp.read()
            # GitHub serves UTF-8
            return content_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error fetching GitHub compare diff: {e}")
        return None

def parse_github_diff_for_file(diff_text, target_rel_path):
    """Parse the multi-file unified diff and return hunks for the specified file.

    Returns a list of hunks: {old_start, old_count, new_start, new_count, lines}
    where lines are the raw hunk lines starting with ' ', '+', or '-'.
    """
    if not diff_text:
        return []

    lines = diff_text.splitlines()
    hunks = []
    collecting_for_file = False
    current_hunk = None
    current_file_path = None

    # Normalize target path to compare by suffix
    target_suffix = target_rel_path.strip("/")

    for line in lines:
        if line.startswith("diff --git "):
            # finalize any open hunk
            if current_hunk is not None and collecting_for_file:
                hunks.append(current_hunk)
            current_hunk = None
            collecting_for_file = False
            current_file_path = None
            continue

        if line.startswith("+++ "):
            path = line[4:].strip()
            # Expected formats: 'b/path/to/file' or '/dev/null'
            if path == "/dev/null":
                current_file_path = None
                collecting_for_file = False
            else:
                # strip the leading 'a/' or 'b/'
                if path.startswith("a/") or path.startswith("b/"):
                    path_clean = path[2:]
                else:
                    path_clean = path
                current_file_path = path_clean
                collecting_for_file = path_clean.endswith(target_suffix)
            continue

        if not collecting_for_file:
            continue

        # Within the target file section, parse hunks
        if line.startswith("@@ "):
            # finalize previous hunk
            if current_hunk is not None:
                hunks.append(current_hunk)

            m = re.match(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", line)
            if not m:
                continue
            old_start = int(m.group(1))
            old_count = int(m.group(2)) if m.group(2) else 1
            new_start = int(m.group(3))
            new_count = int(m.group(4)) if m.group(4) else 1

            current_hunk = {
                "old_start": old_start,
                "old_count": old_count,
                "new_start": new_start,
                "new_count": new_count,
                "lines": [],
            }
            continue

        # Collect hunk body lines
        if current_hunk is not None and (line.startswith(" ") or line.startswith("+") or line.startswith("-")):
            current_hunk["lines"].append(line)

    # finalize last hunk if any
    if current_hunk is not None and collecting_for_file:
        hunks.append(current_hunk)

    return hunks

def apply_hunks_by_line_numbers(target_file, hunks, earlier_commit, latest_commit):
    """Apply unified-diff hunks to target file strictly by old line numbers.

    Only change the lines marked as deletions ('-') and additions ('+').
    Context lines (' ') are used for positioning but are left untouched in the target.
    """
    try:
        content = read_file_from_repo(target_file)
        if not content:
            return False, {}
        lines = content.splitlines()

        modified = list(lines)
        line_offset_delta = 0
        modified_lines = {}

        for hunk_index, hunk in enumerate(hunks):
            cursor = hunk["old_start"] - 1 + line_offset_delta

            if cursor < 0:
                print(f"Hunk {hunk_index+1}: start cursor {cursor} adjusted to 0")
                cursor = 0
            if cursor > len(modified):
                print(f"Hunk {hunk_index+1}: start cursor {cursor} beyond EOF {len(modified)}; clamping to EOF")
                cursor = len(modified)

            #print(f"Applying hunk {hunk_index+1} at approx line {cursor+1}")

            for raw in hunk["lines"]:
                if not raw:
                    continue
                marker = raw[0]
                text = raw[1:]

                if marker == ' ':  # context: advance cursor, keep original content
                    cursor += 1
                elif marker == '-':  # deletion: remove line at cursor
                    if cursor < len(modified):
                        deleted = modified.pop(cursor)
                        line_offset_delta -= 1
                    else:
                        print(f"Hunk {hunk_index+1}: deletion cursor {cursor} at/after EOF; skipping deletion")
                elif marker == '+':  # addition: insert line at cursor
                    modified.insert(cursor, text)
                    modified_lines[cursor+1] = text
                    #print(f"Inserted line at line {cursor+1}: {text}")
                    cursor += 1
                    line_offset_delta += 1
                else:
                    # Unknown marker; ignore
                    pass

        # replace the earlier commit with the latest commit
        for i, line in enumerate(modified):
            if "EN commit:" in line and earlier_commit in line:
                modified[i] = line.replace(earlier_commit, latest_commit)
                break
        modified_content = "\n".join(modified) + "\n"

        success = write_file_to_repo(target_file, modified_content)
        if not success:
            return False, {}

        print(f"Successfully applied {len(hunks)} hunks to {target_file}")
        return True, modified_lines
    except Exception as e:
        print(f"Error applying hunks: {e}")
        return False, {}

def sync_toc_files_using_github_compare(commit1, commit2, source_file, target_file):
    """Sync by fetching compare diff from GitHub and applying hunks by line numbers."""
    print(f"Fetching GitHub compare diff between {commit1} and {commit2}...")
    diff_text = get_github_compare_diff(commit1, commit2)
    if not diff_text:
        print("No diff content retrieved from GitHub")
        return False, {}

    print("Parsing diff for target file hunks...")
    hunks = parse_github_diff_for_file(diff_text, source_file)
    if not hunks:
        print(f"No hunks found for file: {source_file}")
        return False, {}

    print(f"Found {len(hunks)} hunks for {source_file}. Applying to {target_file} by line numbers...")
    sync_status, modified_lines = apply_hunks_by_line_numbers(target_file, hunks, commit1, commit2)
    return sync_status, modified_lines

def create_bilingual_comparison(target_toc_file):
    """Create bilingual comparison list from TOC files"""
    bilingual_list = []
    
    # Read both files
    zh_content = read_file_from_repo(target_toc_file)
    en_content = read_file_from_repo("en_toc_content.md")
    
    if not zh_content or not en_content:
        return []
    
    zh_lines = zh_content.splitlines(True)
    en_lines = en_content.splitlines(True)
    
    # Process from line 4 onwards (index 3)
    start_line = 3  # 0-based index for line 4
    
    # Ensure both files have the same number of lines
    min_lines = min(len(zh_lines), len(en_lines))
    
    print(f"Processing {min_lines - start_line} lines starting from line {start_line + 1}")
    
    for i in range(start_line, min_lines):
        zh_line = zh_lines[i].rstrip('\n\r')
        en_line = en_lines[i].rstrip('\n\r')
        
        # Skip empty lines
        if not zh_line.strip() and not en_line.strip():
            continue
            
        # Clean the lines consistently using the same pattern as replace function
        zh_toc_pattern = re.match(r'^\s*-\s', zh_line)
        en_toc_pattern = re.match(r'^\s*-\s', en_line)
        
        zh_cleaned = zh_line[zh_toc_pattern.end():].rstrip() if zh_toc_pattern else zh_line.rstrip()
        en_cleaned = en_line[en_toc_pattern.end():].rstrip() if en_toc_pattern else en_line.rstrip()
        
        # Only add non-empty cleaned lines
        if zh_cleaned.strip() and en_cleaned.strip():
            bilingual_list.append([zh_cleaned, en_cleaned, i + 1])
            #print(f"Bilingual items: Line {i + 1}: '{en_cleaned}' -> '{zh_cleaned}'")
    
    print(f"Created bilingual list with {len(bilingual_list)} entries")
    return bilingual_list

def replace_content_with_translation(bilingual_list, modified_lines, target_toc_file):
    """Replace English content with existing Chinese translations, return unmatched lines"""
    # Read the target file
    content = read_file_from_repo(target_toc_file)
    if not content:
        return modified_lines
    target_lines = content.splitlines(True)
    
    replaced_count = 0
    matched_lines = set()
    
    print(f"Found {len(modified_lines)} modified lines to process.")
    print(f"Modified lines: {list(modified_lines.keys())}")
    
    # Process each modified line
    for line_number in modified_lines.keys():
        line_index = line_number - 1  # Convert to 0-based
        
        if 0 <= line_index < len(target_lines):
            line_content = target_lines[line_index].rstrip('\n\r')
            
            # Clean the line content for matching
            toc_pattern = re.match(r'^\s*-\s', line_content)
            if toc_pattern:
                prefix = toc_pattern.group(0)
                cleaned_content = line_content[toc_pattern.end():].rstrip()
            else:
                prefix = ''
                cleaned_content = line_content.rstrip()
            
            # Try to find exact match in bilingual list
            for j, entry in enumerate(bilingual_list):
                zh_text, en_text = entry[0], entry[1]
                
                if cleaned_content == en_text:
                    # Found match! Replace with Chinese translation
                    new_line = prefix + zh_text
                    target_lines[line_index] = new_line + '\n'
                    replaced_count += 1
                    matched_lines.add(line_number)
                    
                    #print(f"Matched line {line_number}: '{en_text}' -> '{zh_text}'")
                    break
    
    # Write back the updated content
    if replaced_count > 0:
        updated_content = ''.join(target_lines)
        write_file_to_repo(target_toc_file, updated_content)
        print(f"Applied {replaced_count} existing translations.")
    
    # Return unmatched lines for AI translation
    unmatched_lines = {k: v for k, v in modified_lines.items() if k not in matched_lines}
    print(f"Lines needing AI translation: {len(unmatched_lines)}")
    
    return unmatched_lines

def translate_content(modified_lines, target_file):
    """Translate English content to Chinese using Gemini API with JSON format"""
    if not modified_lines:
        print("No content to translate.")
        return {}
    
    print(f"Translating {len(modified_lines)} lines using Gemini API...")
    
    # Read the target file to get original formatted lines
    content = read_file_from_repo(target_file)
    if not content:
        return {}
    target_lines = content.splitlines(True)
    
    # Create JSON input with original formatted lines
    translation_json = {}
    for line_num in modified_lines.keys():
        line_index = line_num - 1
        if 0 <= line_index < len(target_lines):
            original_line = target_lines[line_index]
            translation_json[str(line_num)] = original_line
    
    if not translation_json:
        print("No valid content to translate after processing.")
        return {}
    
    # Create JSON string for the prompt
    json_input = json.dumps(translation_json, ensure_ascii=False, indent=2)
    print(f"Translation JSON input: {json_input}")
    
    # Create translation prompt
    prompt = f"""Please translate the following TOC (Table of Contents) entries from English to Chinese.
These are navigation items for TiDB Cloud documentation with original formatting.

IMPORTANT: 
1. Return the result in the EXACT SAME JSON format with the same keys (line numbers)
2. Keep ALL original formatting: indentation, spaces, dashes, brackets, etc.
3. Only translate the English text content to Chinese, preserve everything else exactly
4. Maintain technical terms appropriately (like "TiDB Cloud", "HTAP", "CLI", etc.)

Input JSON:
{json_input}

Return only the JSON with Chinese translations that preserve all original formatting."""
    
    try:
        print("Sending translation request to Gemini API...")
        response = client.models.generate_content(
            model=model_name, contents=prompt
        )
        
        if response.text:
            # Extract JSON from response
            response_text = response.text.strip()
            print(f"Translation JSON response: {response_text}")
            
            # Try to find and parse JSON from the response
            try:
                # Remove any markdown code blocks if present
                if '```json' in response_text:
                    start = response_text.find('```json') + 7
                    end = response_text.find('```', start)
                    json_text = response_text[start:end].strip()
                elif '```' in response_text:
                    start = response_text.find('```') + 3
                    end = response_text.find('```', start)
                    json_text = response_text[start:end].strip()
                else:
                    json_text = response_text
                
                # Parse the JSON
                translated_json = json.loads(json_text)
                
                # Convert back to integer keys and return
                zh_modified_lines = {}
                for line_num_str, translated_text in translated_json.items():
                    line_num = int(line_num_str)
                    zh_modified_lines[line_num] = translated_text
                    original_text = modified_lines.get(line_num, "")
                    #print(f"Line {line_num}: '{original_text}' -> '{translated_text}'")
                
                print(f"Translation completed. Processed {len(zh_modified_lines)} lines.")
                return zh_modified_lines
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Response was: {response_text}")
                # Fallback: return original content
                return {line_num: content for line_num, content in modified_lines.items()}
        else:
            print("Error: Empty response from Gemini API")
            return {line_num: content for line_num, content in modified_lines.items()}
                
    except Exception as e:
        print(f"Error during translation: {e}")
        # Fallback: return original content
        return {line_num: content for line_num, content in modified_lines.items()}

def update_toc_file(zh_modified_lines, target_file):
    """Apply translated content to specific lines in the target TOC file"""
    if not zh_modified_lines:
        print("No translated content to apply.")
        return
    
    print(f"Applying {len(zh_modified_lines)} translated lines to {target_file}...")
    
    try:
        # Read the target file
        content = read_file_from_repo(target_file)
        if not content:
            print(f"Error: Could not read target file {target_file}")
            return
        target_lines = content.splitlines(True)
        
        # Apply translations to specific lines
        applied_count = 0
        for line_num, translated_content in zh_modified_lines.items():
            # Convert to 0-based index
            line_index = line_num - 1
            
            if 0 <= line_index < len(target_lines):
                # AI has already provided the complete formatted line, use it directly
                target_lines[line_index] = translated_content
                applied_count += 1
            else:
                print(f"Warning: Line number {line_num} is out of range (file has {len(target_lines)} lines)")
        
        # Write the updated content back to the file
        updated_content = ''.join(target_lines)
        write_file_to_repo(target_file, updated_content)
        
        print(f"\nSuccessfully applied {applied_count} translations to {target_file}")
        
    except Exception as e:
        print(f"Error updating TOC file: {e}")
        raise

def cleanup_temp_files():
    """Clean up temporary files"""
    try:
        if os.path.exists("en_toc_content.md"):
            os.remove("en_toc_content.md")
            print("Cleaned up temporary file: en_toc_content.md")
    except Exception as e:
        print(f"Warning: Could not clean up temporary files: {e}")

if __name__ == "__main__":

    for toc_file_name in toc_file_names:

        target_toc_file = toc_file_name

        print("-" * 50)
        print(f"Processing {toc_file_name}...")

        print("Extracting EN commit SHA from target file...")
        earlier_commit = extract_commit_from_target_file(target_toc_file)

        print("Fetching latest commit SHA for TOC file...")
        latest_commit = get_latest_commit_sha(repo_owner, repo_name, en_branch, toc_file_name)

        # If earlier_commit is different from latest_commit, sync the TOC file.
        if earlier_commit and latest_commit and earlier_commit != latest_commit:
            # Download the EN TOC content from the earlier commit for comparison
            en_toc_path = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{earlier_commit}/{toc_file_name}"
            print(f"Downloading EN TOC content from: {en_toc_path}")
            en_toc_content = urlopen(en_toc_path).read().decode("utf-8")
            
            # Write en_toc_content to a file for bilingual comparison
            write_file_to_repo("en_toc_content.md", en_toc_content)

            print("Creating bilingual comparison...")
            bilingual_list = create_bilingual_comparison(target_toc_file)
            
            print("Running TOC sync using GitHub compare diff...")
            sync_status, modified_lines = sync_toc_files_using_github_compare(
                earlier_commit,
                latest_commit,
                toc_file_name,
                target_toc_file,
            )
            
            if sync_status:
                print("TOC file sync completed successfully!")
                
                # Match with existing bilingual translations
                unmatched_lines = replace_content_with_translation(bilingual_list, modified_lines, target_toc_file)
                
                # Use AI to translate remaining unmatched lines
                if unmatched_lines:
                    print(f"Using AI to translate {len(unmatched_lines)} unmatched lines...")
                    zh_modified_lines = translate_content(unmatched_lines, target_toc_file)
                    update_toc_file(zh_modified_lines, target_toc_file)
                    print("AI translations have been applied successfully!")
                else:
                    print("All lines were matched with existing translations. No AI translation needed.")
            else:
                print("TOC file sync failed!")
        else:
            if earlier_commit == latest_commit:
                print(f"Earlier commit is the same as latest commit. No sync needed for {toc_file_name}.")
            else:
                print(f"Skipping sync for {toc_file_name} due to missing commit information. Check logs for errors.")
    
    # Clean up temporary files
    cleanup_temp_files()
    print("Script execution completed.")
